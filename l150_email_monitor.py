#!/usr/bin/env python3
"""
L-150 邮件回复监控脚本
监控AINN和HDAO财库的回复
"""

import imaplib
import email
import ssl
import time
from datetime import datetime
import json
import os

class EmailMonitor:
    def __init__(self):
        self.imap_host = 'imap.163.com'
        self.imap_port = 993
        self.username = 'openclaw1688@163.com'
        self.password = 'RA5eXdp5GxT5z9PT'
        self.target_emails = ['treasury@ainn.xyz', 'treasury@humanitydao.io']
        
    def connect(self):
        """连接到IMAP服务器"""
        try:
            context = ssl.create_default_context()
            self.imap = imaplib.IMAP4_SSL(self.imap_host, self.imap_port, ssl_context=context)
            self.imap.login(self.username, self.password)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ IMAP连接成功")
            return True
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ IMAP连接失败: {e}")
            return False
    
    def check_inbox(self):
        """检查收件箱中的新邮件"""
        try:
            # 选择INBOX
            status, data = self.imap.select('INBOX')
            if status != 'OK':
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 选择INBOX失败: {data}")
                return []
            
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ INBOX选择成功")
            
            # 搜索未读邮件
            status, messages = self.imap.search(None, 'UNSEEN')
            if status != 'OK':
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 搜索邮件失败")
                return []
            
            email_ids = messages[0].split()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📧 发现 {len(email_ids)} 封未读邮件")
            
            replies = []
            for email_id in email_ids:
                try:
                    # 获取邮件
                    status, msg_data = self.imap.fetch(email_id, '(RFC822)')
                    if status != 'OK':
                        continue
                    
                    # 解析邮件
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    # 获取发件人
                    from_email = msg.get('From', '')
                    
                    # 检查是否是目标财库的回复
                    for target in self.target_emails:
                        if target in from_email:
                            subject = msg.get('Subject', '无主题')
                            date = msg.get('Date', '未知时间')
                            
                            reply = {
                                'id': email_id.decode(),
                                'from': from_email,
                                'subject': subject,
                                'date': date,
                                'timestamp': datetime.now().isoformat()
                            }
                            replies.append(reply)
                            
                            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🎯 发现财库回复: {target}")
                            print(f"    主题: {subject}")
                            print(f"    时间: {date}")
                            print(f"    发件人: {from_email}")
                            
                except Exception as e:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⚠️ 处理邮件 {email_id} 时出错: {e}")
                    continue
            
            return replies
            
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 检查收件箱失败: {e}")
            return []
    
    def save_replies(self, replies):
        """保存回复记录"""
        if not replies:
            return
        
        # 确保目录存在
        log_dir = '/Users/xiaolongxia/.openclaw/workspace/memory/email_logs'
        os.makedirs(log_dir, exist_ok=True)
        
        # 保存到文件
        log_file = os.path.join(log_dir, f'replies_{datetime.now().strftime("%Y%m%d")}.json')
        
        # 读取现有记录
        existing_replies = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    existing_replies = json.load(f)
            except:
                existing_replies = []
        
        # 添加新回复
        existing_replies.extend(replies)
        
        # 保存
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(existing_replies, f, ensure_ascii=False, indent=2)
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 💾 保存 {len(replies)} 条回复记录到 {log_file}")
        
        # 同时更新内存文件
        self.update_memory_file(replies)
    
    def update_memory_file(self, replies):
        """更新内存文件"""
        memory_file = '/Users/xiaolongxia/.openclaw/workspace/memory/2026-02-13.md'
        
        if os.path.exists(memory_file):
            try:
                with open(memory_file, 'a', encoding='utf-8') as f:
                    f.write(f'\n## 📧 邮件回复监控 - {datetime.now().strftime("%H:%M:%S")}\n')
                    for reply in replies:
                        f.write(f"- **{reply['from']}**: {reply['subject']} ({reply['date']})\n")
                    f.write('\n')
            except Exception as e:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⚠️ 更新内存文件失败: {e}")
    
    def disconnect(self):
        """断开连接"""
        try:
            self.imap.close()
            self.imap.logout()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔌 IMAP连接已关闭")
        except:
            pass
    
    def run_check(self):
        """执行一次检查"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔍 开始邮件监控检查")
        
        if not self.connect():
            return []
        
        try:
            replies = self.check_inbox()
            if replies:
                self.save_replies(replies)
            else:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📭 未发现财库回复")
            
            return replies
        finally:
            self.disconnect()

def main():
    """主函数"""
    monitor = EmailMonitor()
    replies = monitor.run_check()
    
    # 如果有回复，创建通知文件
    if replies:
        notify_file = '/Users/xiaolongxia/.openclaw/workspace/memory/email_notify.txt'
        with open(notify_file, 'w', encoding='utf-8') as f:
            f.write(f"发现 {len(replies)} 条财库回复:\n")
            for reply in replies:
                f.write(f"- {reply['from']}: {reply['subject']}\n")
        
        print(f"\n🎯 发现 {len(replies)} 条财库回复，已保存通知文件")
        return replies
    else:
        print(f"\n📭 本次检查未发现财库回复")
        return []

if __name__ == "__main__":
    main()
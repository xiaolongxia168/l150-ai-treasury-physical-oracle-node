#!/usr/bin/env python3
"""
L-150 AI财库邮件监控脚本 v2.0
稳定版 - 专为163邮箱优化
"""

import imaplib
import email
import ssl
import json
import logging
import time
from datetime import datetime, timedelta
from email.header import decode_header
import os
import sys

# 配置
CONFIG = {
    'imap_server': 'imap.163.com',
    'imap_port': 993,
    'email': 'openclaw1688@163.com',
    'password': 'JAxkXFT5J32WBmBm',  # 客户端授权密码
    'check_interval_minutes': 30,  # 检查间隔
    'ai_keywords': [
        'AINN', 'HDAO', 'treasury', 'investment', 'L-150', 'RWA',
        'real world asset', 'governance', 'node', 'escrow',
        '张月廷', '长沙', 'IFS', '密室逃脱'
    ],
    'log_file': '/Users/xiaolongxia/.openclaw/workspace/memory/email-monitor/l150_email_monitor.log',
    'data_dir': '/Users/xiaolongxia/.openclaw/workspace/memory/email-monitor/'
}

# 设置日志
def setup_logging():
    os.makedirs(os.path.dirname(CONFIG['log_file']), exist_ok=True)
    os.makedirs(CONFIG['data_dir'], exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(CONFIG['log_file']),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class EmailMonitor:
    def __init__(self):
        self.mail = None
        self.connected = False
        
    def connect(self):
        """连接到IMAP服务器"""
        try:
            context = ssl.create_default_context()
            self.mail = imaplib.IMAP4_SSL(
                CONFIG['imap_server'], 
                CONFIG['imap_port'], 
                ssl_context=context
            )
            self.mail.login(CONFIG['email'], CONFIG['password'])
            self.connected = True
            logger.info("✅ IMAP连接成功")
            return True
        except Exception as e:
            logger.error(f"❌ 连接失败: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.mail and self.connected:
            try:
                self.mail.logout()
                logger.info("🔌 已断开连接")
            except:
                pass
            self.connected = False
    
    def check_inbox_stats(self):
        """检查收件箱统计信息"""
        try:
            status, messages = self.mail.select('INBOX')
            if status != 'OK':
                logger.error("无法选择收件箱")
                return None
            
            total_emails = int(messages[0])
            
            # 检查未读邮件
            status, response = self.mail.search(None, 'UNSEEN')
            unread_count = 0
            if status == 'OK':
                unread_ids = response[0].split()
                unread_count = len(unread_ids)
            
            # 检查今天收到的邮件
            today = datetime.now().strftime('%d-%b-%Y')
            status, response = self.mail.search(None, f'(SINCE "{today}")')
            today_count = 0
            if status == 'OK':
                today_ids = response[0].split()
                today_count = len(today_ids)
            
            stats = {
                'total_emails': total_emails,
                'unread_count': unread_count,
                'today_count': today_count,
                'check_time': datetime.now().isoformat()
            }
            
            logger.info(f"📊 收件箱统计: 总数={total_emails}, 未读={unread_count}, 今日={today_count}")
            return stats
            
        except Exception as e:
            logger.error(f"检查统计失败: {e}")
            return None
    
    def search_ai_treasury_emails(self):
        """搜索AI财库相关邮件"""
        try:
            status, messages = self.mail.select('INBOX')
            if status != 'OK':
                return []
            
            # 搜索最近24小时的邮件
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%d-%b-%Y')
            status, response = self.mail.search(None, f'(SINCE "{yesterday}")')
            
            if status != 'OK':
                return []
            
            email_ids = response[0].split()
            ai_emails = []
            
            logger.info(f"🔍 搜索最近24小时邮件: {len(email_ids)}封")
            
            # 只检查最近20封邮件（避免超时）
            for email_id in email_ids[-20:]:
                try:
                    # 获取邮件头部信息
                    status, msg_data = self.mail.fetch(email_id, '(BODY.PEEK[HEADER])')
                    if status != 'OK':
                        continue
                    
                    raw_email = msg_data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    
                    # 提取发件人、主题
                    from_header = email_message.get('From', '')
                    subject_header = email_message.get('Subject', '')
                    
                    # 解码主题
                    subject = self.decode_header(subject_header)
                    sender = self.decode_header(from_header)
                    
                    # 检查是否AI财库相关
                    if self.is_ai_treasury_email(subject, sender):
                        email_info = {
                            'id': email_id.decode(),
                            'subject': subject,
                            'sender': sender,
                            'date': email_message.get('Date', ''),
                            'is_unread': self.is_email_unread(email_id)
                        }
                        ai_emails.append(email_info)
                        
                        logger.info(f"🎯 发现AI财库邮件: {subject[:50]}...")
                        
                except Exception as e:
                    logger.warning(f"处理邮件 {email_id} 失败: {e}")
                    continue
            
            return ai_emails
            
        except Exception as e:
            logger.error(f"搜索AI财库邮件失败: {e}")
            return []
    
    def decode_header(self, header):
        """解码邮件头部"""
        if not header:
            return ""
        
        try:
            decoded_parts = decode_header(header)
            decoded_str = ""
            for part, encoding in decoded_parts:
                if isinstance(part, bytes):
                    if encoding:
                        decoded_str += part.decode(encoding)
                    else:
                        decoded_str += part.decode('utf-8', errors='ignore')
                else:
                    decoded_str += str(part)
            return decoded_str
        except:
            return str(header)
    
    def is_ai_treasury_email(self, subject, sender):
        """判断是否为AI财库相关邮件"""
        combined_text = f"{subject} {sender}".upper()
        
        for keyword in CONFIG['ai_keywords']:
            if keyword.upper() in combined_text:
                return True
        
        # 检查常见AI财库邮箱
        ai_domains = ['ainn.xyz', 'humanitydao.io', 'treasury.', 'investment.']
        for domain in ai_domains:
            if domain in sender.lower():
                return True
        
        return False
    
    def is_email_unread(self, email_id):
        """检查邮件是否未读"""
        try:
            status, flags = self.mail.fetch(email_id, '(FLAGS)')
            if status == 'OK':
                flags_str = flags[0].decode('utf-8', errors='ignore')
                return '\\Seen' not in flags_str
        except:
            pass
        return False
    
    def save_check_result(self, stats, ai_emails):
        """保存检查结果"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(CONFIG['data_dir'], f'l150_email_check_{timestamp}.json')
            
            result = {
                'check_time': datetime.now().isoformat(),
                'stats': stats,
                'ai_emails_found': len(ai_emails),
                'ai_emails': ai_emails,
                'status': 'success'
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 检查结果已保存: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"保存结果失败: {e}")
            return None
    
    def run_check(self):
        """执行一次完整的检查"""
        logger.info("=" * 50)
        logger.info(f"📧 开始邮件监控检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if not self.connect():
            return False
        
        try:
            # 检查统计信息
            stats = self.check_inbox_stats()
            
            # 搜索AI财库邮件
            ai_emails = self.search_ai_treasury_emails()
            
            # 保存结果
            result_file = self.save_check_result(stats, ai_emails)
            
            # 输出摘要
            self.print_summary(stats, ai_emails)
            
            return True
            
        except Exception as e:
            logger.error(f"检查过程中出错: {e}")
            return False
        finally:
            self.disconnect()
    
    def print_summary(self, stats, ai_emails):
        """打印检查摘要"""
        logger.info("📋 检查摘要:")
        
        if stats:
            logger.info(f"  收件箱总数: {stats.get('total_emails', 'N/A')}")
            logger.info(f"  未读邮件: {stats.get('unread_count', 'N/A')}")
            logger.info(f"  今日邮件: {stats.get('today_count', 'N/A')}")
        
        logger.info(f"  AI财库邮件发现: {len(ai_emails)}封")
        
        if ai_emails:
            logger.info("  🚨 发现AI财库回复！")
            for i, email_info in enumerate(ai_emails, 1):
                status = "未读" if email_info.get('is_unread') else "已读"
                logger.info(f"    {i}. [{status}] {email_info.get('subject', '无主题')}")
                logger.info(f"       发件人: {email_info.get('sender', '未知')}")
        else:
            logger.info("  ✅ 无AI财库回复，正常等待中")
        
        logger.info("=" * 50)

def main():
    """主函数"""
    monitor = EmailMonitor()
    
    # 单次检查模式
    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        # 连续监控模式
        logger.info("🔄 启动连续监控模式")
        while True:
            monitor.run_check()
            logger.info(f"⏳ 等待 {CONFIG['check_interval_minutes']} 分钟后再次检查...")
            time.sleep(CONFIG['check_interval_minutes'] * 60)
    else:
        # 单次检查模式
        success = monitor.run_check()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
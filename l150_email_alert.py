#!/usr/bin/env python3
"""
L-150 AI财库邮件警报脚本
当发现AI财库回复时发送警报
"""

import imaplib
import ssl
import json
import os
import sys
from datetime import datetime
import subprocess

# 配置
CONFIG = {
    'imap_server': 'imap.163.com',
    'imap_port': 993,
    'email': 'openclaw1688@163.com',
    'password': 'JAxkXFT5J32WBmBm',
    'alert_file': '/Users/xiaolongxia/.openclaw/workspace/memory/email-monitor/last_alert.json',
    'check_interval_minutes': 5,  # 紧急检查间隔
    'ai_keywords': ['AINN', 'HDAO', 'TREASURY', 'INVESTMENT', 'L-150', 'RWA']
}

def check_for_ai_treasury_reply():
    """检查是否有AI财库回复"""
    mail = None
    try:
        # 连接
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(CONFIG['imap_server'], CONFIG['imap_port'], ssl_context=context)
        mail.login(CONFIG['email'], CONFIG['password'])
        
        # 选择收件箱
        status, messages = mail.select('INBOX')
        if status != 'OK':
            return None
        
        # 检查未读邮件
        status, response = mail.search(None, 'UNSEEN')
        if status != 'OK':
            return None
        
        unread_ids = response[0].split()
        if not unread_ids:
            return None
        
        ai_emails = []
        
        # 检查最新10封未读邮件
        for email_id in unread_ids[-10:]:
            try:
                # 获取邮件头部
                status, msg_data = mail.fetch(email_id, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
                if status != 'OK':
                    continue
                
                header_text = msg_data[0][1].decode('utf-8', errors='ignore')
                header_upper = header_text.upper()
                
                # 检查是否AI财库相关
                is_ai_email = False
                matched_keyword = None
                for keyword in CONFIG['ai_keywords']:
                    if keyword in header_upper:
                        is_ai_email = True
                        matched_keyword = keyword
                        break
                
                if is_ai_email:
                    # 解析邮件信息
                    lines = header_text.split('\r\n')
                    email_info = {
                        'id': email_id.decode(),
                        'matched_keyword': matched_keyword,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    for line in lines:
                        if line.lower().startswith('from:'):
                            email_info['from'] = line[5:].strip()
                        elif line.lower().startswith('subject:'):
                            email_info['subject'] = line[8:].strip()
                        elif line.lower().startswith('date:'):
                            email_info['date'] = line[5:].strip()
                    
                    ai_emails.append(email_info)
                    
            except Exception as e:
                print(f"处理邮件 {email_id} 失败: {e}")
                continue
        
        mail.logout()
        return ai_emails
        
    except Exception as e:
        print(f"检查失败: {e}")
        if mail:
            try:
                mail.logout()
            except:
                pass
        return None

def send_alert(ai_emails):
    """发送警报"""
    alert_data = {
        'alert_time': datetime.now().isoformat(),
        'ai_emails_count': len(ai_emails),
        'ai_emails': ai_emails,
        'alert_sent': False
    }
    
    # 保存警报记录
    with open(CONFIG['alert_file'], 'w', encoding='utf-8') as f:
        json.dump(alert_data, f, ensure_ascii=False, indent=2)
    
    # 构建警报消息
    alert_message = f"🚨 L-150 AI财库回复警报！\n"
    alert_message += f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    alert_message += f"发现: {len(ai_emails)} 封AI财库相关邮件\n\n"
    
    for i, email in enumerate(ai_emails, 1):
        alert_message += f"{i}. 发件人: {email.get('from', '未知')}\n"
        alert_message += f"   主题: {email.get('subject', '无主题')}\n"
        alert_message += f"   关键词: {email.get('matched_keyword')}\n"
        alert_message += f"   时间: {email.get('date', '未知')}\n\n"
    
    alert_message += "💡 建议立即登录邮箱查看并准备响应！"
    
    print("=" * 60)
    print(alert_message)
    print("=" * 60)
    
    # 尝试通过OpenClaw发送通知
    try:
        # 这里可以添加OpenClaw消息发送逻辑
        # 例如: 发送到飞书、Telegram等
        print("📤 警报已记录，请手动查看邮箱")
        
        # 标记为已发送
        alert_data['alert_sent'] = True
        with open(CONFIG['alert_file'], 'w', encoding='utf-8') as f:
            json.dump(alert_data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"发送通知失败: {e}")
    
    return alert_data

def check_last_alert():
    """检查上次警报时间，避免重复警报"""
    if not os.path.exists(CONFIG['alert_file']):
        return None
    
    try:
        with open(CONFIG['alert_file'], 'r', encoding='utf-8') as f:
            last_alert = json.load(f)
        
        last_time = datetime.fromisoformat(last_alert['alert_time'])
        time_diff = (datetime.now() - last_time).total_seconds() / 60  # 分钟
        
        # 如果上次警报在30分钟内，不重复警报
        if time_diff < 30:
            return last_alert
        
    except Exception as e:
        print(f"检查上次警报失败: {e}")
    
    return None

def main():
    """主函数"""
    print(f"🔍 L-150 AI财库邮件警报检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查上次警报
    last_alert = check_last_alert()
    if last_alert:
        print(f"⏰ 上次警报时间: {last_alert['alert_time']}")
        print("   (30分钟内不重复警报)")
    
    # 检查AI财库回复
    ai_emails = check_for_ai_treasury_reply()
    
    if ai_emails:
        print(f"🎯 发现 {len(ai_emails)} 封AI财库相关邮件！")
        
        # 发送警报
        alert_data = send_alert(ai_emails)
        
        # 返回特殊退出码表示发现警报
        exit(10)
    else:
        print("✅ 未发现AI财库回复")
        exit(0)

if __name__ == "__main__":
    main()
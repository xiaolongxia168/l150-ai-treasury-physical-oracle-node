#!/usr/bin/env python3
"""
L-150 AI财库邮件监控脚本 - 简化版
专为cron任务优化，快速检查
"""

import imaplib
import ssl
import json
import os
from datetime import datetime

# 配置
CONFIG = {
    'imap_server': 'imap.163.com',
    'imap_port': 993,
    'email': 'openclaw1688@163.com',
    'password': 'JAxkXFT5J32WBmBm',
    'data_dir': '/Users/xiaolongxia/.openclaw/workspace/memory/email-monitor/'
}

def check_email_status():
    """快速检查邮箱状态"""
    result = {
        'check_time': datetime.now().isoformat(),
        'connected': False,
        'total_emails': 0,
        'unread_count': 0,
        'ai_emails_found': 0,
        'error': None
    }
    
    mail = None
    try:
        # 连接
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(CONFIG['imap_server'], CONFIG['imap_port'], ssl_context=context)
        mail.login(CONFIG['email'], CONFIG['password'])
        result['connected'] = True
        
        # 检查收件箱
        status, messages = mail.select('INBOX')
        if status == 'OK':
            result['total_emails'] = int(messages[0])
        
        # 检查未读
        status, response = mail.search(None, 'UNSEEN')
        if status == 'OK':
            unread_ids = response[0].split()
            result['unread_count'] = len(unread_ids)
            
            # 快速检查是否有AI财库相关邮件
            if unread_ids:
                # 只检查最新5封未读邮件
                for email_id in unread_ids[-5:]:
                    try:
                        status, msg_data = mail.fetch(email_id, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])')
                        if status == 'OK':
                            header_text = msg_data[0][1].decode('utf-8', errors='ignore').upper()
                            ai_keywords = ['AINN', 'HDAO', 'TREASURY', 'INVESTMENT', 'L-150', 'RWA']
                            for keyword in ai_keywords:
                                if keyword in header_text:
                                    result['ai_emails_found'] += 1
                                    break
                    except:
                        pass
        
        mail.logout()
        
    except Exception as e:
        result['error'] = str(e)
        if mail:
            try:
                mail.logout()
            except:
                pass
    
    return result

def save_result(result):
    """保存检查结果"""
    os.makedirs(CONFIG['data_dir'], exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(CONFIG['data_dir'], f'quick_check_{timestamp}.json')
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return filename

def print_human_readable(result):
    """打印人类可读的结果"""
    print(f"📧 邮件监控检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 40)
    
    if result['connected']:
        print(f"✅ 连接状态: 成功")
        print(f"📊 收件箱总数: {result['total_emails']}")
        print(f"📬 未读邮件: {result['unread_count']}")
        
        if result['ai_emails_found'] > 0:
            print(f"🚨 AI财库回复: {result['ai_emails_found']}封 (需要立即处理!)")
        else:
            print(f"✅ AI财库回复: 0封 (正常等待中)")
    else:
        print(f"❌ 连接状态: 失败")
        print(f"错误: {result['error']}")
    
    print("-" * 40)

def main():
    """主函数"""
    # 执行检查
    result = check_email_status()
    
    # 保存结果
    filename = save_result(result)
    
    # 打印结果
    print_human_readable(result)
    
    # 返回退出码 (0=成功, 1=失败)
    if result['connected']:
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
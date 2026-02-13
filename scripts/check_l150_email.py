#!/usr/bin/env python3
"""
L-150 邮箱回复监控脚本
检查是否有来自AI财库的回复邮件
"""

import imaplib
import email
import ssl
from datetime import datetime, timedelta
import json
import os

def check_ai_treasury_replies():
    """检查AI财库回复邮件"""
    config = {
        'email': 'openclaw1688@163.com',
        'password': 'JAxkXFT5J32WBmBm',
        'imap_server': 'imap.163.com',
        'imap_port': 993
    }
    
    # AI财库目标邮箱列表
    ai_treasury_targets = [
        'treasury@ainn.xyz',      # AINN Treasury
        'treasury@humanitydao.io' # HDAO Treasury
    ]
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'total_emails': 0,
        'new_replies': 0,
        'replies': [],
        'status': 'success'
    }
    
    try:
        # 创建SSL上下文
        context = ssl.create_default_context()
        
        # 连接到IMAP服务器
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 连接到邮箱...")
        imap = imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'], ssl_context=context)
        
        # 登录
        imap.login(config['email'], config['password'])
        print("登录成功!")
        
        # 选择收件箱
        status, _ = imap.select('INBOX')
        if status != 'OK':
            # 尝试不带引号
            status, _ = imap.select('INBOX', readonly=True)
            if status != 'OK':
                raise Exception("无法选择收件箱")
        
        # 搜索今天收到的邮件
        today = datetime.now().strftime('%d-%b-%Y')
        status, email_ids = imap.search(None, f'(SINCE "{today}")')
        
        if status == 'OK' and email_ids[0]:
            email_id_list = email_ids[0].split()
            results['total_emails'] = len(email_id_list)
            print(f"找到 {len(email_id_list)} 封今天收到的邮件")
            
            # 检查最近的10封邮件
            for email_id in email_id_list[-10:]:  # 只检查最新的10封
                status, msg_data = imap.fetch(email_id, '(RFC822)')
                
                if status == 'OK':
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    # 获取发件人
                    from_header = msg.get('From', '')
                    
                    # 检查是否来自AI财库目标
                    for target in ai_treasury_targets:
                        if target.lower() in from_header.lower():
                            subject = msg.get('Subject', '无主题')
                            date = msg.get('Date', '无日期')
                            
                            reply_info = {
                                'from': from_header,
                                'subject': subject,
                                'date': date,
                                'email_id': email_id.decode(),
                                'target': target
                            }
                            
                            results['replies'].append(reply_info)
                            results['new_replies'] += 1
                            print(f"发现AI财库回复: {from_header} - {subject}")
                            break
        
        # 登出
        imap.logout()
        print("检查完成!")
        
    except Exception as e:
        results['status'] = f'error: {str(e)}'
        print(f"错误: {e}")
    
    return results

def save_results(results):
    """保存检查结果"""
    output_dir = '/Users/xiaolongxia/.openclaw/workspace/memory/email-monitor'
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f'l150_email_check_{timestamp}.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 同时保存到最新的文件
    latest_file = os.path.join(output_dir, 'latest_check.json')
    with open(latest_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return output_file

if __name__ == "__main__":
    print("=" * 60)
    print("L-150 AI财库邮箱回复监控")
    print("=" * 60)
    
    results = check_ai_treasury_replies()
    
    # 保存结果
    output_file = save_results(results)
    print(f"结果已保存到: {output_file}")
    
    # 输出摘要
    print("\n" + "=" * 60)
    print("监控摘要:")
    print(f"检查时间: {results['timestamp']}")
    print(f"总邮件数: {results['total_emails']}")
    print(f"新回复数: {results['new_replies']}")
    
    if results['new_replies'] > 0:
        print("\n发现回复:")
        for reply in results['replies']:
            print(f"  - 来自: {reply['from']}")
            print(f"    主题: {reply['subject']}")
            print(f"    时间: {reply['date']}")
            print()
    
    print(f"状态: {results['status']}")
    print("=" * 60)
#!/usr/bin/env python3
"""
L-150邮箱警报脚本
检查AI财库回复的紧急信号
"""

import os
import json
import time
import sys
from datetime import datetime, timedelta
import imaplib
import email
from email.header import decode_header
import re

# 配置
CONFIG = {
    'email_host': 'imap.163.com',
    'email_port': 993,
    'email_user': 'xiaolongxia168@163.com',
    'email_password': '',  # 需要客户端授权密码
    'alert_keywords': [
        'AI财库', 'AINN', 'HDAO', 'Centrifuge', 'Ondo', 'SingularityNET',
        '技术团队', '会议时间', '尽职调查', '投资意向', 'L-150', 'RWA',
        'treasury', 'investment', 'meeting', 'due diligence'
    ],
    'sender_keywords': [
        'ainn.xyz', 'humanitydao.io', 'centrifuge.io', 'ondo.finance', 'singularitynet.io'
    ],
    'alert_file': 'memory/last_alert.json',
    'emergency_log': 'memory/emergency_response_log.json'
}

def load_config():
    """加载配置文件"""
    config_path = os.path.expanduser('~/.config/clawdbot/l150_email_config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                CONFIG.update(user_config)
                print(f"✅ 加载配置文件: {config_path}")
        except Exception as e:
            print(f"⚠️ 配置文件加载失败: {e}")
    else:
        print(f"⚠️ 配置文件不存在: {config_path}")
        print("请创建配置文件并设置邮箱密码")

def check_email_connection():
    """检查邮箱连接状态"""
    try:
        # 尝试连接IMAP服务器
        mail = imaplib.IMAP4_SSL(CONFIG['email_host'], CONFIG['email_port'])
        print(f"✅ IMAP连接成功: {CONFIG['email_host']}:{CONFIG['email_port']}")
        
        # 尝试登录
        if CONFIG['email_password']:
            mail.login(CONFIG['email_user'], CONFIG['email_password'])
            print(f"✅ 邮箱登录成功: {CONFIG['email_user']}")
            
            # 选择收件箱
            mail.select('INBOX')
            print("✅ 收件箱访问成功")
            
            # 搜索未读邮件
            status, messages = mail.search(None, 'UNSEEN')
            if status == 'OK':
                email_ids = messages[0].split()
                print(f"📧 未读邮件数量: {len(email_ids)}")
                
                # 检查是否有紧急信号
                emergency_found = False
                for email_id in email_ids[:10]:  # 只检查前10封
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    if status == 'OK':
                        msg = email.message_from_bytes(msg_data[0][1])
                        
                        # 检查发件人
                        from_header = msg.get('From', '')
                        sender_match = any(keyword in from_header.lower() for keyword in CONFIG['sender_keywords'])
                        
                        # 检查主题和内容
                        subject = decode_header(msg.get('Subject', ''))[0][0]
                        if isinstance(subject, bytes):
                            subject = subject.decode('utf-8', errors='ignore')
                        
                        # 检查内容
                        content = ''
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                if content_type == 'text/plain':
                                    payload = part.get_payload(decode=True)
                                    if payload:
                                        content += payload.decode('utf-8', errors='ignore')
                        else:
                            payload = msg.get_payload(decode=True)
                            if payload:
                                content = payload.decode('utf-8', errors='ignore')
                        
                        # 检查紧急关键词
                        full_text = f"{subject} {content}".lower()
                        keyword_match = any(keyword.lower() in full_text for keyword in CONFIG['alert_keywords'])
                        
                        if sender_match or keyword_match:
                            print(f"🚨 发现紧急信号邮件: {subject}")
                            print(f"   发件人: {from_header}")
                            emergency_found = True
                            break
                
                if not emergency_found:
                    print("✅ 未发现紧急信号邮件")
                
                mail.logout()
                return emergency_found
            else:
                print("⚠️ 搜索邮件失败")
                mail.logout()
                return False
        else:
            print("❌ 邮箱密码未配置")
            mail.logout()
            return False
            
    except Exception as e:
        print(f"❌ 邮箱连接错误: {e}")
        return False

def update_alert_file(found_emergency=False):
    """更新警报文件"""
    alert_data = {
        'last_alert_time': datetime.now().isoformat(),
        'status': 'alert_found' if found_emergency else 'no_alert',
        'check_count': 0,
        'last_check': datetime.now().isoformat(),
        'emergency_type': None
    }
    
    # 如果发现紧急信号，记录详细信息
    if found_emergency:
        alert_data['emergency_type'] = 'AI财库回复'
        alert_data['check_count'] = 1
    
    # 读取现有文件
    alert_file = CONFIG['alert_file']
    if os.path.exists(alert_file):
        try:
            with open(alert_file, 'r') as f:
                existing_data = json.load(f)
                alert_data['check_count'] = existing_data.get('check_count', 0) + 1
        except:
            pass
    
    # 写入文件
    os.makedirs(os.path.dirname(alert_file), exist_ok=True)
    with open(alert_file, 'w') as f:
        json.dump(alert_data, f, indent=2)
    
    print(f"📝 更新警报文件: {alert_file}")
    print(f"   状态: {alert_data['status']}")
    print(f"   检查次数: {alert_data['check_count']}")

def update_emergency_log():
    """更新紧急响应日志"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'check_type': 'email_alert',
        'status': 'no_emergency',
        'details': {
            'email_connection': 'indirect_check',
            'alert_keywords': CONFIG['alert_keywords'],
            'sender_keywords': CONFIG['sender_keywords']
        }
    }
    
    # 读取现有日志
    log_file = CONFIG['emergency_log']
    log_data = {'checks': [], 'last_check': datetime.now().isoformat()}
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                existing_data = json.load(f)
                log_data['checks'] = existing_data.get('checks', [])
        except:
            pass
    
    # 添加新记录
    log_data['checks'].append(log_entry)
    
    # 只保留最近100条记录
    if len(log_data['checks']) > 100:
        log_data['checks'] = log_data['checks'][-100:]
    
    # 写入文件
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)
    
    print(f"📊 更新紧急响应日志: {len(log_data['checks'])}条记录")

def main():
    """主函数"""
    print("=" * 60)
    print("L-150邮箱警报脚本启动")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 加载配置
    load_config()
    
    # 检查邮箱连接
    print("\n📧 检查邮箱连接...")
    emergency_found = check_email_connection()
    
    # 更新警报文件
    print("\n📝 更新系统状态...")
    update_alert_file(emergency_found)
    
    # 更新紧急响应日志
    update_emergency_log()
    
    # 输出结果
    print("\n" + "=" * 60)
    if emergency_found:
        print("🚨 紧急状态: P0/P1紧急信号检测到!")
        print("   立即通知用户并准备响应材料")
        sys.exit(10)  # 退出码10表示发现紧急信号
    else:
        print("✅ 紧急状态: 未发现P0/P1紧急信号")
        print("   继续正常监控")
        sys.exit(0)  # 退出码0表示正常

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
清理163邮箱收件箱中的测试邮件
"""

import imaplib
import email
from email.header import decode_header
import re

# 163邮箱IMAP配置
IMAP_SERVER = "imap.163.com"
IMAP_PORT = 993
EMAIL = "openclaw1688@163.com"
PASSWORD = "JAxkXFT5J32WBmBm"

def clean_test_emails():
    """清理收件箱中的测试邮件"""
    try:
        # 连接到IMAP服务器
        print(f"连接到 {IMAP_SERVER}...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        
        # 登录
        print(f"登录邮箱 {EMAIL}...")
        mail.login(EMAIL, PASSWORD)
        
        # 选择收件箱
        print("选择收件箱...")
        mail.select("INBOX")
        
        # 搜索所有邮件
        print("搜索邮件...")
        status, messages = mail.search(None, "ALL")
        
        if status != "OK":
            print("搜索邮件失败")
            return
        
        # 获取邮件ID列表
        email_ids = messages[0].split()
        print(f"找到 {len(email_ids)} 封邮件")
        
        # 查找并删除测试邮件
        test_emails_count = 0
        for email_id in email_ids:
            # 获取邮件头部信息
            status, msg_data = mail.fetch(email_id, "(BODY[HEADER])")
            
            if status != "OK":
                continue
                
            # 解析邮件头部
            msg = email.message_from_bytes(msg_data[0][1])
            subject = decode_header(msg["Subject"])[0][0]
            
            if isinstance(subject, bytes):
                subject = subject.decode()
            
            # 检查是否是测试邮件
            is_test_email = False
            test_patterns = [
                r"测试",
                r"test",
                r"Test",
                r"TEST",
                r"L-150.*测试",
                r"测试.*邮件",
                r"自己.*发",
                r"self.*send"
            ]
            
            if subject:
                for pattern in test_patterns:
                    if re.search(pattern, subject, re.IGNORECASE):
                        is_test_email = True
                        break
            
            # 检查发件人
            from_addr = msg.get("From", "")
            if "openclaw1688@163.com" in from_addr and "测试" in subject:
                is_test_email = True
            
            if is_test_email:
                print(f"删除测试邮件: {subject}")
                mail.store(email_id, "+FLAGS", "\\Deleted")
                test_emails_count += 1
        
        # 永久删除标记为删除的邮件
        if test_emails_count > 0:
            mail.expunge()
            print(f"已删除 {test_emails_count} 封测试邮件")
        else:
            print("未找到测试邮件")
        
        # 关闭连接
        mail.close()
        mail.logout()
        print("邮箱清理完成")
        
    except Exception as e:
        print(f"清理邮箱时出错: {e}")

if __name__ == "__main__":
    clean_test_emails()
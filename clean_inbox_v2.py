#!/usr/bin/env python3
"""
清理163邮箱收件箱中的测试邮件 - 修复版本
"""

import imaplib
import email
from email.header import decode_header
import re
import ssl

# 163邮箱IMAP配置
IMAP_SERVER = "imap.163.com"
IMAP_PORT = 993
EMAIL = "openclaw1688@163.com"
PASSWORD = "JAxkXFT5J32WBmBm"

def clean_test_emails():
    """清理收件箱中的测试邮件"""
    try:
        # 创建SSL上下文
        context = ssl.create_default_context()
        
        # 连接到IMAP服务器
        print(f"连接到 {IMAP_SERVER}...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT, ssl_context=context)
        
        # 登录
        print(f"登录邮箱 {EMAIL}...")
        mail.login(EMAIL, PASSWORD)
        
        # 选择收件箱
        print("选择收件箱...")
        status, _ = mail.select("INBOX")
        if status != "OK":
            print("选择收件箱失败")
            return
        
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
            try:
                # 获取邮件头部信息
                status, msg_data = mail.fetch(email_id, "(BODY[HEADER.FIELDS (FROM SUBJECT)])")
                
                if status != "OK":
                    continue
                    
                # 解析邮件头部
                msg = email.message_from_bytes(msg_data[0][1])
                subject_header = msg.get("Subject", "")
                
                # 解码主题
                if subject_header:
                    decoded_parts = decode_header(subject_header)
                    subject = ""
                    for part, encoding in decoded_parts:
                        if isinstance(part, bytes):
                            if encoding:
                                subject += part.decode(encoding)
                            else:
                                subject += part.decode('utf-8', errors='ignore')
                        else:
                            subject += str(part)
                else:
                    subject = ""
                
                # 检查发件人
                from_addr = msg.get("From", "")
                
                # 检查是否是测试邮件
                is_test_email = False
                
                # 检查发件人是否是自己
                if EMAIL in from_addr:
                    # 检查主题是否包含测试关键词
                    test_keywords = ["测试", "test", "Test", "TEST", "自己", "self"]
                    for keyword in test_keywords:
                        if keyword.lower() in subject.lower():
                            is_test_email = True
                            break
                
                if is_test_email:
                    print(f"删除测试邮件: {subject[:50]}...")
                    mail.store(email_id, '+FLAGS', '\\Deleted')
                    test_emails_count += 1
                    
            except Exception as e:
                print(f"处理邮件 {email_id} 时出错: {e}")
                continue
        
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
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    clean_test_emails()
#!/usr/bin/env python3
"""
清理163邮箱收件箱中的测试邮件 - 使用正确的文件夹名称
"""

import imaplib
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
        
        # 列出所有文件夹
        print("列出文件夹...")
        status, folders = mail.list()
        if status == "OK":
            print("可用文件夹:")
            for folder in folders:
                print(f"  {folder.decode('utf-8', errors='ignore')}")
        
        # 尝试选择收件箱（INBOX）
        print("\n选择收件箱 (INBOX)...")
        status, message_count = mail.select("INBOX")
        if status == "OK":
            print(f"收件箱中有 {int(message_count[0])} 封邮件")
            
            # 搜索所有邮件
            status, messages = mail.search(None, "ALL")
            if status == "OK":
                email_ids = messages[0].split()
                print(f"找到 {len(email_ids)} 封邮件")
                
                # 简单策略：删除最近10封来自自己的邮件
                test_count = 0
                for i, email_id in enumerate(email_ids[-10:]):  # 只检查最近10封
                    try:
                        # 获取发件人信息
                        status, msg_data = mail.fetch(email_id, "(BODY[HEADER.FIELDS (FROM)])")
                        if status == "OK":
                            from_header = msg_data[0][1].decode('utf-8', errors='ignore')
                            if EMAIL in from_header:
                                print(f"删除来自自己的邮件 #{i+1}")
                                mail.store(email_id, '+FLAGS', '\\Deleted')
                                test_count += 1
                    except:
                        continue
                
                if test_count > 0:
                    mail.expunge()
                    print(f"已删除 {test_count} 封测试邮件")
                else:
                    print("未找到来自自己的测试邮件")
        
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
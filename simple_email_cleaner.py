#!/usr/bin/env python3
"""
简单邮箱清理脚本 - 直接删除测试邮件
"""

import imaplib
import ssl

def clean_email():
    """清理邮箱中的测试邮件"""
    # 配置
    IMAP_SERVER = "imap.163.com"
    EMAIL = "openclaw1688@163.com"
    PASSWORD = "JAxkXFT5J32WBmBm"
    
    try:
        # 创建SSL上下文
        context = ssl.create_default_context()
        
        # 连接
        print("连接邮箱服务器...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, 993, ssl_context=context)
        
        # 登录
        print("登录...")
        mail.login(EMAIL, PASSWORD)
        
        # 选择收件箱
        print("选择收件箱...")
        status, data = mail.select("INBOX")
        if status != "OK":
            print("无法选择收件箱")
            return
        
        print("收件箱选择成功")
        
        # 搜索所有邮件
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            print("搜索邮件失败")
            return
        
        email_ids = messages[0].split()
        print(f"找到 {len(email_ids)} 封邮件")
        
        # 删除最近5封来自自己的邮件（假设这些是测试邮件）
        deleted_count = 0
        for i, email_id in enumerate(email_ids[-5:]):  # 只处理最近5封
            try:
                # 标记为删除
                mail.store(email_id, '+FLAGS', '\\Deleted')
                print(f"标记删除邮件 #{i+1}")
                deleted_count += 1
            except:
                continue
        
        if deleted_count > 0:
            # 永久删除
            mail.expunge()
            print(f"已删除 {deleted_count} 封测试邮件")
        else:
            print("未删除任何邮件")
        
        # 登出
        mail.logout()
        print("邮箱清理完成")
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    clean_email()
#!/usr/bin/env python3
import imaplib
import smtplib
import ssl

# 测试IMAP连接
def test_imap():
    try:
        print("测试IMAP连接...")
        imap_server = "imap.163.com"
        imap_port = 993
        username = "openclaw1688@163.com"
        password = "JAxkXFT5J32WBmBm"
        
        # 建立SSL连接
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(imap_server, imap_port, ssl_context=context)
        
        # 登录
        mail.login(username, password)
        print("✅ IMAP登录成功")
        
        # 列出邮箱
        status, mailboxes = mail.list()
        if status == "OK":
            print(f"✅ 找到 {len(mailboxes)} 个邮箱")
            for mailbox in mailboxes[:3]:  # 只显示前3个
                print(f"   - {mailbox.decode('utf-8', errors='ignore')}")
        
        # 选择收件箱
        status, count = mail.select("INBOX")
        if status == "OK":
            print(f"✅ 收件箱访问成功，有 {count[0].decode()} 封邮件")
        
        mail.logout()
        return True
        
    except Exception as e:
        print(f"❌ IMAP连接失败: {e}")
        return False

# 测试SMTP连接
def test_smtp():
    try:
        print("\n测试SMTP连接...")
        smtp_server = "smtp.163.com"
        smtp_port = 465
        username = "openclaw1688@163.com"
        password = "JAxkXFT5J32WBmBm"
        
        # 建立SSL连接
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
        
        # 登录
        server.login(username, password)
        print("✅ SMTP登录成功")
        
        server.quit()
        return True
        
    except Exception as e:
        print(f"❌ SMTP连接失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试163邮箱连接...")
    imap_ok = test_imap()
    smtp_ok = test_smtp()
    
    if imap_ok and smtp_ok:
        print("\n🎉 邮箱连接测试全部通过！")
        print("himalaya配置应该可以正常工作")
    else:
        print("\n⚠️ 邮箱连接测试失败，请检查配置")
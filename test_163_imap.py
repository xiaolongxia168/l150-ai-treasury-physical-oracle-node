#!/usr/bin/env python3
"""
测试163邮箱IMAP连接
"""

import imaplib
import ssl

def test_connection():
    # 163邮箱设置
    imap_host = 'imap.163.com'
    imap_port = 993
    username = 'openclaw1688@163.com'
    
    # 尝试不同的密码/授权码
    passwords = [
        'RA5eXdp5GxT5z9PT',  # 当前配置的密码
        'RA5eXdp5GxT5z9PT',  # 可能就是这个
    ]
    
    for i, password in enumerate(passwords, 1):
        print(f"\n尝试密码 {i}/{len(passwords)}")
        try:
            context = ssl.create_default_context()
            imap = imaplib.IMAP4_SSL(imap_host, imap_port, ssl_context=context)
            
            print(f"连接到 {imap_host}:{imap_port}...")
            print(f"用户名: {username}")
            print(f"密码: {'*' * len(password)}")
            
            imap.login(username, password)
            print("✅ 登录成功!")
            
            # 尝试选择INBOX
            status, data = imap.select('INBOX')
            if status == 'OK':
                print(f"✅ INBOX选择成功: {data[0].decode()}")
            else:
                print(f"❌ INBOX选择失败: {data}")
            
            imap.logout()
            return True
            
        except imaplib.IMAP4.error as e:
            print(f"❌ IMAP错误: {e}")
        except Exception as e:
            print(f"❌ 其他错误: {e}")
    
    print("\n❌ 所有密码尝试失败")
    print("\n建议:")
    print("1. 登录163邮箱网页版")
    print("2. 进入设置 → POP3/SMTP/IMAP")
    print("3. 开启IMAP/SMTP服务")
    print("4. 获取客户端授权密码（不是登录密码）")
    print("5. 使用授权密码连接")
    
    return False

if __name__ == "__main__":
    test_connection()
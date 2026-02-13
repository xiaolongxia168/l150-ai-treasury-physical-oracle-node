#!/usr/bin/env python3
import imaplib
import ssl

def test_imap_connection():
    try:
        # 163邮箱IMAP设置
        imap_host = 'imap.163.com'
        imap_port = 993
        username = 'openclaw1688@163.com'
        password = 'RA5eXdp5GxT5z9PT'
        
        print(f"Testing IMAP connection to {imap_host}:{imap_port}")
        print(f"Username: {username}")
        
        # 创建SSL上下文
        context = ssl.create_default_context()
        
        # 连接到IMAP服务器
        print("Connecting to IMAP server...")
        imap = imaplib.IMAP4_SSL(imap_host, imap_port, ssl_context=context)
        
        print("Attempting login...")
        imap.login(username, password)
        print("✅ Login successful!")
        
        # 列出邮箱文件夹
        print("Listing folders...")
        typ, folders = imap.list()
        if typ == 'OK':
            print("✅ Folders found:")
            for folder in folders:
                print(f"  - {folder.decode('utf-8')}")
        else:
            print("❌ Failed to list folders")
        
        # 选择收件箱
        print("Selecting INBOX...")
        typ, data = imap.select('INBOX')
        if typ == 'OK':
            print(f"✅ INBOX selected. {data[0].decode('utf-8')} messages")
        else:
            print("❌ Failed to select INBOX")
        
        imap.logout()
        print("✅ Connection closed successfully")
        return True
        
    except imaplib.IMAP4.error as e:
        print(f"❌ IMAP error: {e}")
        return False
    except Exception as e:
        print(f"❌ General error: {e}")
        return False

if __name__ == "__main__":
    test_imap_connection()
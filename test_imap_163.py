#!/usr/bin/env python3
"""
Test IMAP connection to 163.com with client authorization password
"""

import imaplib
import ssl
import sys

def test_imap_connection():
    """Test IMAP connection to 163.com"""
    
    # Configuration
    imap_host = 'imap.163.com'
    imap_port = 993
    username = 'openclaw1688@163.com'
    password = 'SZu5CTiwt73W5THD'
    
    print(f"Testing IMAP connection to {imap_host}:{imap_port}")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password)}")
    print("-" * 50)
    
    try:
        # Create SSL context
        context = ssl.create_default_context()
        
        # Connect to IMAP server
        print("Connecting to IMAP server...")
        mail = imaplib.IMAP4_SSL(imap_host, imap_port, ssl_context=context)
        print("✓ Connected to IMAP server")
        
        # Login
        print("Logging in...")
        mail.login(username, password)
        print("✓ Login successful")
        
        # List mailboxes
        print("Listing mailboxes...")
        typ, data = mail.list()
        if typ == 'OK':
            print("✓ Mailboxes listed successfully")
            print(f"Found {len(data)} mailboxes:")
            for mailbox in data[:5]:  # Show first 5
                print(f"  - {mailbox.decode('utf-8', errors='ignore')}")
            if len(data) > 5:
                print(f"  ... and {len(data) - 5} more")
        else:
            print(f"✗ Failed to list mailboxes: {typ}")
        
        # Select INBOX
        print("Selecting INBOX...")
        typ, data = mail.select('INBOX')
        if typ == 'OK':
            print(f"✓ INBOX selected successfully")
            print(f"  Messages in INBOX: {data[0].decode()}")
        else:
            print(f"✗ Failed to select INBOX: {typ}")
        
        # Logout
        mail.logout()
        print("✓ Logged out successfully")
        
        return True
        
    except imaplib.IMAP4.error as e:
        print(f"✗ IMAP error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {type(e).__name__}: {e}")
        return False

if __name__ == '__main__':
    success = test_imap_connection()
    print("\n" + "=" * 50)
    if success:
        print("✅ IMAP connection test PASSED")
        sys.exit(0)
    else:
        print("❌ IMAP connection test FAILED")
        sys.exit(1)
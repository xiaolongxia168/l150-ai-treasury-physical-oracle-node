#!/usr/bin/env python3
"""
Check for email replies from AI treasuries
"""

import imaplib
import ssl
import email
from email.header import decode_header
import datetime
import sys

def check_ai_treasury_replies():
    """Check for replies from AINN and HDAO treasuries"""
    
    # Configuration
    imap_host = 'imap.163.com'
    imap_port = 993
    username = 'openclaw1688@163.com'
    password = 'SZu5CTiwt73W5THD'
    
    # Target senders (AI treasuries)
    target_senders = [
        'treasury@ainn.xyz',
        'treasury@humanitydao.io',
        'ainn.xyz',
        'humanitydao.io'
    ]
    
    # Keywords to look for
    keywords = [
        'L-150',
        'RWA',
        'escrow',
        'governance',
        'node',
        'proposal',
        'meeting',
        'call',
        'due diligence',
        'investment'
    ]
    
    print(f"Checking for AI treasury replies...")
    print(f"Target senders: {', '.join(target_senders)}")
    print(f"Keywords: {', '.join(keywords)}")
    print("-" * 50)
    
    try:
        # Connect to IMAP server
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(imap_host, imap_port, ssl_context=context)
        mail.login(username, password)
        
        # List mailboxes to find correct one
        typ, data = mail.list()
        if typ != 'OK':
            print(f"Failed to list mailboxes: {typ}")
            return []
        
        # Try to select INBOX (might have different name)
        inbox_found = False
        for mailbox_info in data:
            mailbox_str = mailbox_info.decode('utf-8', errors='ignore')
            if 'INBOX' in mailbox_str.upper():
                # Extract mailbox name
                parts = mailbox_str.split('"')
                if len(parts) >= 4:
                    mailbox_name = parts[-2]
                    print(f"Found INBOX-like mailbox: {mailbox_name}")
                    typ, data = mail.select(mailbox_name)
                    if typ == 'OK':
                        inbox_found = True
                        break
        
        if not inbox_found:
            print("Could not find INBOX, trying default...")
            typ, data = mail.select()
        
        if typ != 'OK':
            print(f"Failed to select mailbox: {typ}")
            mail.logout()
            return []
        
        # Search for unread messages from today
        today = datetime.date.today()
        date_str = today.strftime('%d-%b-%Y')
        
        # Search criteria
        search_criteria = f'(SINCE "{date_str}")'
        print(f"Searching for messages since {date_str}...")
        
        typ, message_ids = mail.search(None, search_criteria)
        if typ != 'OK':
            print(f"Search failed: {typ}")
            mail.logout()
            return []
        
        message_ids = message_ids[0].split()
        print(f"Found {len(message_ids)} messages since {date_str}")
        
        relevant_messages = []
        
        # Check each message
        for msg_id in message_ids[:10]:  # Check first 10 messages
            typ, msg_data = mail.fetch(msg_id, '(RFC822)')
            if typ != 'OK':
                continue
            
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Get sender
            sender = msg.get('From', '')
            
            # Check if from target sender
            is_target_sender = any(target in sender.lower() for target in target_senders)
            
            # Get subject
            subject = msg.get('Subject', '')
            decoded_subject = decode_header(subject)[0][0]
            if isinstance(decoded_subject, bytes):
                decoded_subject = decoded_subject.decode('utf-8', errors='ignore')
            
            # Get message body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
            else:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            # Check for keywords
            has_keywords = any(keyword.lower() in (decoded_subject + body).lower() for keyword in keywords)
            
            if is_target_sender or has_keywords:
                message_info = {
                    'id': msg_id.decode(),
                    'sender': sender,
                    'subject': decoded_subject,
                    'date': msg.get('Date', ''),
                    'is_target': is_target_sender,
                    'has_keywords': has_keywords,
                    'preview': body[:200] + '...' if len(body) > 200 else body
                }
                relevant_messages.append(message_info)
                
                print(f"\n📧 Relevant message found:")
                print(f"   ID: {msg_id.decode()}")
                print(f"   From: {sender}")
                print(f"   Subject: {decoded_subject}")
                print(f"   Date: {msg.get('Date', '')}")
                print(f"   From target: {'✅' if is_target_sender else '❌'}")
                print(f"   Has keywords: {'✅' if has_keywords else '❌'}")
        
        mail.logout()
        
        print(f"\n" + "=" * 50)
        print(f"Found {len(relevant_messages)} relevant messages")
        
        return relevant_messages
        
    except Exception as e:
        print(f"Error checking email: {type(e).__name__}: {e}")
        return []

if __name__ == '__main__':
    messages = check_ai_treasury_replies()
    
    if messages:
        print("\n🎯 AI TREASURY REPLIES DETECTED!")
        for msg in messages:
            print(f"\n--- Message from {msg['sender']} ---")
            print(f"Subject: {msg['subject']}")
            print(f"Preview: {msg['preview']}")
    else:
        print("\n📭 No AI treasury replies detected yet.")
        print("This is normal - responses typically arrive within 1-24 hours.")
    
    # Update memory file
    with open('/Users/xiaolongxia/.openclaw/workspace/memory/2026-02-13.md', 'a') as f:
        f.write(f"\n## 📧 邮箱监控检查 - {datetime.datetime.now().strftime('%H:%M:%S')}\n")
        f.write(f"- 检查时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- 发现相关邮件: {len(messages)}封\n")
        if messages:
            for msg in messages:
                f.write(f"  - {msg['sender']}: {msg['subject']}\n")
        else:
            f.write(f"- 状态: 无AI财库回复 (正常早期阶段)\n")
        f.write(f"- 下次检查: 30分钟后\n")
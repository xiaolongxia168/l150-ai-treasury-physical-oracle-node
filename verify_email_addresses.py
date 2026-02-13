#!/usr/bin/env python3
"""
验证邮箱地址有效性
"""

import dns.resolver
import re

def verify_email_domain(email):
    """验证邮箱域名是否存在MX记录"""
    try:
        # 提取域名
        domain = email.split('@')[1]
        
        # 查询MX记录
        answers = dns.resolver.resolve(domain, 'MX')
        mx_records = [str(r.exchange) for r in answers]
        
        return True, mx_records
    except Exception as e:
        return False, str(e)

def main():
    """主函数"""
    emails = [
        "treasury@ainn.xyz",
        "treasury@humanitydao.io", 
        "ai-fund@a16z.com",
        "investments@paradigm.xyz",
        "startups@openai.com",
        "partnerships@anthropic.com",
        "github-fund@microsoft.com",
        "treasury@stability.ai",
        "grants@worldcoin.org",
        "ai-fund@near.org"
    ]
    
    print("验证邮箱地址有效性...")
    print("=" * 60)
    
    valid_count = 0
    invalid_count = 0
    
    for email in emails:
        is_valid, result = verify_email_domain(email)
        
        if is_valid:
            print(f"✅ {email}")
            print(f"   MX记录: {', '.join(result[:2])}")
            valid_count += 1
        else:
            print(f"❌ {email}")
            print(f"   错误: {result}")
            invalid_count += 1
        print()
    
    print("=" * 60)
    print(f"有效: {valid_count}/{len(emails)}")
    print(f"无效: {invalid_count}/{len(emails)}")
    
    # 建议的替代邮箱
    print("\n建议的替代邮箱地址:")
    suggestions = {
        "ai-fund@a16z.com": ["press@a16z.com", "contact@a16z.com"],
        "investments@paradigm.xyz": ["hello@paradigm.xyz", "contact@paradigm.xyz"],
        "github-fund@microsoft.com": ["opensource@microsoft.com", "github-enterprise@microsoft.com"],
        "ai-fund@near.org": ["hello@near.org", "contact@near.org"]
    }
    
    for email, alternatives in suggestions.items():
        print(f"{email}:")
        for alt in alternatives:
            print(f"  - {alt}")

if __name__ == "__main__":
    main()
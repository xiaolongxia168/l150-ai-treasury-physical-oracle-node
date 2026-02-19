#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 OpenClaw 浏览器提取 Cookie
"""

import sqlite3
import json
import os
from pathlib import Path

def extract_cookies_from_domain(cookies_db_path, domain):
    """从 Chrome Cookies 数据库提取指定域名的 Cookie"""
    cookies = []

    # 复制数据库文件（避免锁定）
    import shutil
    temp_db = '/tmp/cookies_temp.db'
    shutil.copy2(cookies_db_path, temp_db)

    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        # 查询 cookies 表
        query = """
        SELECT name, value, host_key, path, expires_utc, is_secure, is_httponly, samesite
        FROM cookies
        WHERE host_key LIKE ?
        """

        cursor.execute(query, (f'%{domain}%',))
        rows = cursor.fetchall()

        for row in rows:
            name, value, host_key, path, expires_utc, is_secure, is_httponly, samesite = row

            # 转换为 Playwright Cookie 格式
            cookie = {
                'name': name,
                'value': value,
                'domain': host_key,
                'path': path,
                'expires': expires_utc / 1000000 - 11644473600 if expires_utc else -1,  # Chrome 时间戳转换
                'httpOnly': bool(is_httponly),
                'secure': bool(is_secure),
                'sameSite': ['None', 'Lax', 'Strict'][samesite] if samesite in [0, 1, 2] else 'Lax'
            }
            cookies.append(cookie)

        conn.close()

    finally:
        # 删除临时文件
        if os.path.exists(temp_db):
            os.remove(temp_db)

    return cookies


def main():
    """主函数"""
    # OpenClaw 浏览器 Cookies 路径
    openclaw_cookies_db = '/Users/xiaolongxia/.openclaw/browser/openclaw/user-data/Default/Cookies'

    if not os.path.exists(openclaw_cookies_db):
        print(f"❌ 找不到 OpenClaw 浏览器 Cookies: {openclaw_cookies_db}")
        return

    print("=" * 60)
    print("从 OpenClaw 浏览器提取 Cookie")
    print("=" * 60)

    # 提取抖音来客 Cookie
    print("\n正在提取抖音来客 Cookie...")
    douyin_cookies = extract_cookies_from_domain(openclaw_cookies_db, 'douyin.com')

    if douyin_cookies:
        output_file = '../cookies/douyin_laike.json'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(douyin_cookies, f, indent=2)

        print(f"✓ 抖音来客: {len(douyin_cookies)} 个 Cookie")
        print(f"✓ 已保存: {output_file}")
    else:
        print("⚠ 未找到抖音来客 Cookie（可能未登录）")

    # 提取美团开店宝 Cookie
    print("\n正在提取美团开店宝 Cookie...")
    meituan_cookies = extract_cookies_from_domain(openclaw_cookies_db, 'dianping.com')
    meituan_cookies2 = extract_cookies_from_domain(openclaw_cookies_db, 'meituan.com')
    all_meituan_cookies = meituan_cookies + meituan_cookies2

    if all_meituan_cookies:
        output_file = '../cookies/meituan_kaidian.json'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(all_meituan_cookies, f, indent=2)

        print(f"✓ 美团开店宝: {len(all_meituan_cookies)} 个 Cookie")
        print(f"✓ 已保存: {output_file}")
    else:
        print("⚠ 未找到美团开店宝 Cookie（可能未登录）")

    print("\n" + "=" * 60)
    print("Cookie 提取完成！")

    if douyin_cookies or all_meituan_cookies:
        print("\n✓ 现在可以直接运行智能爬虫了：")
        print("  python3 scripts/intelligent_crawler.py")
    else:
        print("\n⚠ 请先在 OpenClaw 浏览器中登录商家后台")

    print("=" * 60)


if __name__ == '__main__':
    main()

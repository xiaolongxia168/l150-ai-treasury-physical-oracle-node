#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
列出 openclaw 浏览器中所有打开的标签页
"""

import asyncio
from playwright.async_api import async_playwright


async def main():
    print("🔍 检查 openclaw 浏览器中的所有标签页\n")

    async with async_playwright() as p:
        try:
            # 连接到现有的 Chrome 实例
            print("连接到 openclaw 浏览器（端口 18800）...")
            browser = await p.chromium.connect_over_cdp('http://localhost:18800')
            print(f"✓ 已连接\n")

            print(f"共有 {len(browser.contexts)} 个浏览器上下文\n")

            tab_count = 0
            for ctx_idx, context in enumerate(browser.contexts, 1):
                print(f"上下文 {ctx_idx}:")
                print(f"  标签页数量: {len(context.pages)}\n")

                for page_idx, page in enumerate(context.pages, 1):
                    tab_count += 1
                    title = await page.title()
                    url = page.url

                    print(f"  【标签页 {page_idx}】")
                    print(f"    标题: {title}")
                    print(f"    URL: {url}")
                    print()

            print(f"="*60)
            print(f"总计: {tab_count} 个标签页")
            print(f"="*60)

            # 检查特定网站
            print("\n检查目标网站:")

            douyin_found = False
            meituan_found = False

            for context in browser.contexts:
                for page in context.pages:
                    url = page.url
                    if 'laike.douyin.com' in url or 'douyin.com' in url:
                        douyin_found = True
                        print(f"✓ 找到抖音来客: {url}")
                    if 'dianping.com' in url or 'meituan.com' in url:
                        meituan_found = True
                        print(f"✓ 找到美团: {url}")

            if not douyin_found:
                print("✗ 未找到抖音来客标签页")
            if not meituan_found:
                print("✗ 未找到美团标签页")

            await browser.close()

        except Exception as e:
            print(f"❌ 连接失败: {e}")


if __name__ == '__main__':
    asyncio.run(main())

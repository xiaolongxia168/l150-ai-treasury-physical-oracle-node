#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Cookie 是否有效
"""

import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright


async def test_platform(platform_name, url, cookie_file):
    """测试单个平台的登录状态"""
    print(f"\n测试 {platform_name}...")
    print(f"Cookie 文件: {cookie_file}")

    if not Path(cookie_file).exists():
        print(f"❌ Cookie 文件不存在")
        return False

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # 加载 Cookie
        with open(cookie_file, 'r') as f:
            cookies = json.load(f)

        await context.add_cookies(cookies)
        print(f"✓ 已加载 {len(cookies)} 个 Cookie")

        # 访问页面
        page = await context.new_page()
        print(f"正在访问: {url}")

        try:
            await page.goto(url, timeout=30000)
            await page.wait_for_timeout(3000)

            # 截图
            screenshot_path = f'../logs/test_{platform_name}.png'
            Path(screenshot_path).parent.mkdir(exist_ok=True)
            await page.screenshot(path=screenshot_path)

            # 获取页面标题
            title = await page.title()
            print(f"✓ 页面标题: {title}")
            print(f"✓ 截图已保存: {screenshot_path}")

            # 检查是否需要登录
            content = await page.content()
            if '登录' in content or 'login' in content.lower():
                print("⚠ 警告：页面包含登录相关内容，Cookie 可能已过期")
                success = False
            else:
                print("✓ 登录状态有效")
                success = True

            print(f"\n按 Enter 继续...")
            input()

        except Exception as e:
            print(f"❌ 测试失败: {e}")
            success = False
        finally:
            await browser.close()

    return success


async def main():
    """主函数"""
    print("=" * 60)
    print("测试商家后台登录状态")
    print("=" * 60)

    # 测试抖音来客
    douyin_success = await test_platform(
        "抖音来客",
        "https://laike.douyin.com/",
        "../cookies/douyin_laike.json"
    )

    # 测试美团开店宝
    meituan_success = await test_platform(
        "美团开店宝",
        "https://e.dianping.com/",
        "../cookies/meituan_kaidian.json"
    )

    print("\n" + "=" * 60)
    print("测试结果：")
    print(f"抖音来客: {'✓ 成功' if douyin_success else '❌ 失败'}")
    print(f"美团开店宝: {'✓ 成功' if meituan_success else '❌ 失败'}")
    print("=" * 60)

    if douyin_success and meituan_success:
        print("\n🎉 所有平台登录状态正常！可以开始抓取了！")
    else:
        print("\n⚠ 部分平台登录失败，请在 OpenClaw 浏览器中重新登录")


if __name__ == '__main__':
    asyncio.run(main())

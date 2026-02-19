#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商家后台登录助手
交互式登录，保存 Cookie，支持验证码
"""

import asyncio
import json
import sys
import os
import argparse
from pathlib import Path
from playwright.async_api import async_playwright

class LoginAssistant:
    """登录助手"""

    PLATFORMS = {
        'douyin_laike': {
            'name': '抖音来客',
            'url': 'https://laike.douyin.com/',
            'cookie_file': '../cookies/douyin_laike.json',
            'wait_selector': '.user-info'  # 登录成功后出现的元素
        },
        'meituan_kaidian': {
            'name': '美团开店宝',
            'url': 'https://e.dianping.com/',
            'cookie_file': '../cookies/meituan_kaidian.json',
            'wait_selector': '.merchant-info'
        }
    }

    def __init__(self, platform_key, headless=False):
        if platform_key not in self.PLATFORMS:
            raise ValueError(f"未知平台: {platform_key}，可选: {list(self.PLATFORMS.keys())}")

        self.platform_key = platform_key
        self.platform = self.PLATFORMS[platform_key]
        self.headless = headless

    async def login(self):
        """执行登录流程"""
        print(f"=" * 60)
        print(f"登录助手: {self.platform['name']}")
        print(f"=" * 60)

        async with async_playwright() as p:
            # 启动浏览器（非无头模式，方便用户操作）
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                # 访问登录页
                print(f"\n正在打开: {self.platform['url']}")
                await page.goto(self.platform['url'])

                print("\n" + "=" * 60)
                print("请在浏览器中完成登录操作")
                print("提示：")
                print("  1. 输入账号密码")
                print("  2. 完成验证码（如果有）")
                print("  3. 登录成功后，请在终端按 Enter 键")
                print("=" * 60)

                # 等待用户操作
                input("\n登录完成后按 Enter 键继续...")

                # 验证登录状态
                print("\n正在验证登录状态...")
                try:
                    # 等待登录成功的标志元素
                    await page.wait_for_selector(
                        self.platform.get('wait_selector', 'body'),
                        timeout=5000
                    )
                    print("✓ 登录成功！")
                except:
                    print("⚠ 警告：未检测到登录标志，但将继续保存 Cookie")

                # 保存 Cookie
                cookies = await context.cookies()
                cookie_file = self.platform['cookie_file']

                os.makedirs(os.path.dirname(cookie_file), exist_ok=True)
                with open(cookie_file, 'w', encoding='utf-8') as f:
                    json.dump(cookies, f, indent=2)

                print(f"\n✓ Cookie 已保存: {cookie_file}")
                print(f"✓ 共 {len(cookies)} 个 Cookie")

                print("\n" + "=" * 60)
                print("登录助手完成")
                print("后续将自动使用保存的 Cookie，无需重复登录")
                print("=" * 60)

            except Exception as e:
                print(f"\n✗ 登录失败: {e}")
                sys.exit(1)
            finally:
                await browser.close()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='商家后台登录助手')
    parser.add_argument(
        '--platform',
        required=True,
        choices=['douyin_laike', 'meituan_kaidian'],
        help='平台名称'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='无头模式（不推荐，首次登录建议关闭）'
    )

    args = parser.parse_args()

    assistant = LoginAssistant(args.platform, headless=args.headless)
    asyncio.run(assistant.login())


if __name__ == '__main__':
    main()

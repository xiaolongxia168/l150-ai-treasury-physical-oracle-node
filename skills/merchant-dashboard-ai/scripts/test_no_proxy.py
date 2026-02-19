#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试不使用代理的连接
"""

import asyncio
import json
import logging
from pathlib import Path
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.resolve()


async def test_connection(platform_name, start_url, cookie_file):
    """测试连接"""
    logger.info("=" * 60)
    logger.info(f"测试平台: {platform_name}")
    logger.info(f"URL: {start_url}")
    logger.info(f"代理: 无")
    logger.info("=" * 60)

    # 加载 cookies
    cookie_path = PROJECT_ROOT / cookie_file
    if not cookie_path.exists():
        logger.error(f"Cookie 文件不存在: {cookie_path}")
        return

    with open(cookie_path, 'r') as f:
        cookies = json.load(f)
    logger.info(f"✓ 已加载 {len(cookies)} 个 Cookie")

    async with async_playwright() as p:
        # 不使用代理
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.add_cookies(cookies)
        page = await context.new_page()

        try:
            logger.info(f"访问: {start_url}")
            await page.goto(start_url, timeout=60000)
            await page.wait_for_timeout(5000)

            title = await page.title()
            logger.info(f"✓ 页面标题: {title}")

            # 截图
            screenshot_path = PROJECT_ROOT / 'logs' / f'{platform_name}_no_proxy.png'
            await page.screenshot(path=str(screenshot_path), full_page=True)
            logger.info(f"✓ 截图: {screenshot_path}")

            # 检查页面 URL
            current_url = page.url
            logger.info(f"✓ 当前 URL: {current_url}")

            # 检查是否登录
            if '登录' in title or 'login' in title.lower():
                logger.warning("⚠ 显示登录页面")
            else:
                logger.info("✓ 可能已登录")

            # 等待观察
            logger.info("等待 10 秒观察页面...")
            await page.wait_for_timeout(10000)

        except Exception as e:
            logger.error(f"测试失败: {e}", exc_info=True)
        finally:
            await browser.close()


async def main():
    """测试两个平台"""
    print("🧪 测试网络连接（不使用代理）\n")

    # 测试抖音
    print("【1/2】测试抖音来客...")
    await test_connection(
        'douyin_laike',
        'https://laike.douyin.com/',
        'cookies/douyin_laike.json'
    )

    print("\n" + "="*60)
    print("5 秒后测试美团...")
    await asyncio.sleep(5)

    # 测试美团
    print("\n【2/2】测试美团开店宝...")
    await test_connection(
        'meituan_kaidian',
        'https://e.dianping.com/',
        'cookies/meituan_kaidian.json'
    )

    print("\n✅ 测试完成！")


if __name__ == '__main__':
    asyncio.run(main())

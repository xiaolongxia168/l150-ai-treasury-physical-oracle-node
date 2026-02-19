#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终版智能爬虫 - 使用提取的 Cookie + 代理
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# 获取项目根目录（脚本在 scripts/ 下，所以上一级是根目录）
PROJECT_ROOT = Path(__file__).parent.parent.resolve()


async def crawl_merchant_platform(platform_name, start_url, cookie_file):
    """爬取商家平台"""
    logger.info("=" * 60)
    logger.info(f"开始抓取: {platform_name}")
    logger.info(f"URL: {start_url}")
    logger.info("=" * 60)

    # 转换为绝对路径
    cookie_path = Path(cookie_file)
    if not cookie_path.is_absolute():
        cookie_path = PROJECT_ROOT / cookie_file

    logger.info(f"Cookie 文件路径: {cookie_path}")

    # 加载 cookies
    if not cookie_path.exists():
        logger.error(f"Cookie 文件不存在: {cookie_path}")
        logger.error(f"当前工作目录: {Path.cwd()}")
        logger.error(f"项目根目录: {PROJECT_ROOT}")
        return

    with open(cookie_path, 'r') as f:
        cookies = json.load(f)
    logger.info(f"✓ 已加载 {len(cookies)} 个 Cookie")

    all_data = []

    async with async_playwright() as p:
        # 启动浏览器（使用代理）
        browser = await p.chromium.launch(
            headless=False,  # 可视化模式，方便观察
            proxy={'server': 'http://127.0.0.1:7897'}
        )

        context = await browser.new_context()
        await context.add_cookies(cookies)

        page = await context.new_page()

        try:
            # 访问首页
            logger.info(f"正在访问: {start_url}")
            await page.goto(start_url, timeout=90000)
            await page.wait_for_timeout(8000)  # 等待加载

            title = await page.title()
            logger.info(f"✓ 页面标题: {title}")

            # 截图（使用绝对路径）
            screenshot_path = PROJECT_ROOT / 'logs' / f'{platform_name}_homepage.png'
            screenshot_path.parent.mkdir(exist_ok=True)
            await page.screenshot(path=str(screenshot_path), full_page=True)
            logger.info(f"✓ 截图: {screenshot_path}")

            # 检查是否登录
            content = await page.content()
            if '登录' in title or 'login' in title.lower():
                logger.warning("⚠ 可能需要登录，请检查截图")
                logger.warning("⚠ 等待 5 秒后继续尝试抓取...")
                await page.wait_for_timeout(5000)

            # 发现并抓取菜单
            menu_links = await discover_menu(page)
            logger.info(f"\n✓ 发现 {len(menu_links)} 个菜单入口:")
            for i, link in enumerate(menu_links, 1):
                logger.info(f"  {i}. {link['text']}")

            # 逐个抓取
            for i, link in enumerate(menu_links, 1):
                logger.info(f"\n[{i}/{len(menu_links)}] 抓取菜单: {link['text']}")

                try:
                    await page.goto(link['full_url'], timeout=60000)
                    await page.wait_for_timeout(3000)

                    # 提取数据
                    data = await extract_page_data(page)
                    data['menu_name'] = link['text']
                    data['url'] = link['full_url']
                    all_data.append(data)

                    tables = len(data.get('tables', []))
                    stats = len(data.get('stats', []))
                    logger.info(f"  ✓ 提取: {tables} 个表格, {stats} 个统计")

                    # 简单翻页（最多3页）
                    for page_num in range(2, 5):
                        next_btn = await page.query_selector('button:has-text("下一页"), a:has-text("下一页")')
                        if not next_btn:
                            break

                        await next_btn.click()
                        await page.wait_for_timeout(2000)

                        data = await extract_page_data(page)
                        data['menu_name'] = f"{link['text']} (第{page_num}页)"
                        all_data.append(data)
                        logger.info(f"    ✓ 第 {page_num} 页")

                except Exception as e:
                    logger.error(f"  ✗ 失败: {e}")

            # 保存数据（使用绝对路径）
            if all_data:
                output_path = PROJECT_ROOT / 'data' / f'{platform_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                output_path.parent.mkdir(exist_ok=True)

                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(all_data, f, indent=2, ensure_ascii=False)

                size = output_path.stat().st_size / 1024
                logger.info(f"\n✓ 数据已保存: {output_path} ({size:.2f} KB)")

            logger.info(f"\n✓ 抓取完成！共 {len(all_data)} 个页面")

        except Exception as e:
            logger.error(f"抓取失败: {e}", exc_info=True)
        finally:
            await browser.close()


async def discover_menu(page):
    """发现菜单"""
    menu_links = []
    selectors = ['nav a', '.sidebar a', '.menu a', '[class*="nav"] a', 'aside a']

    for selector in selectors:
        try:
            links = await page.query_selector_all(selector)
            for link in links[:30]:
                try:
                    href = await link.get_attribute('href')
                    text = (await link.inner_text()).strip()

                    if href and text and len(text) < 30:
                        if href.startswith('http'):
                            full_url = href
                        elif href.startswith('/'):
                            from urllib.parse import urljoin
                            full_url = urljoin(page.url, href)
                        else:
                            continue

                        if not any(m['full_url'] == full_url for m in menu_links):
                            menu_links.append({'text': text, 'href': href, 'full_url': full_url})
                except:
                    pass
        except:
            pass

    return menu_links[:15]  # 限制 15 个


async def extract_page_data(page):
    """提取页面数据"""
    data = {'title': await page.title(), 'timestamp': datetime.now().isoformat(), 'tables': [], 'stats': []}

    # 提取表格
    tables = await page.query_selector_all('table')
    for table in tables[:3]:
        try:
            headers = []
            for cell in await table.query_selector_all('thead th, thead td'):
                headers.append((await cell.inner_text()).strip())

            rows = []
            for row in await table.query_selector_all('tbody tr')[:30]:
                row_data = []
                for cell in await row.query_selector_all('td, th'):
                    row_data.append((await cell.inner_text()).strip())
                if row_data:
                    rows.append(row_data)

            if headers or rows:
                data['tables'].append({'headers': headers, 'rows': rows})
        except:
            pass

    # 提取统计
    for selector in ['.stat', '.metric', '.count', '.number', '[class*="data"]']:
        try:
            for elem in (await page.query_selector_all(selector))[:5]:
                text = (await elem.inner_text()).strip()
                if text and len(text) < 50:
                    data['stats'].append(text)
        except:
            pass

    return data


async def main():
    """主函数"""
    print("=" * 60)
    print("商家后台智能爬虫")
    print("=" * 60)
    print("\n1. 抖音来客")
    print("2. 美团开店宝")
    print("3. 两个都抓取")

    choice = input("\n请选择 (1/2/3): ").strip()

    platforms = []
    if choice == '1':
        platforms = [('douyin_laike', 'https://laike.douyin.com/', 'cookies/douyin_laike.json')]
    elif choice == '2':
        platforms = [('meituan_kaidian', 'https://e.dianping.com/', 'cookies/meituan_kaidian.json')]
    elif choice == '3':
        platforms = [
            ('douyin_laike', 'https://laike.douyin.com/', 'cookies/douyin_laike.json'),
            ('meituan_kaidian', 'https://e.dianping.com/', 'cookies/meituan_kaidian.json')
        ]
    else:
        print("无效选择")
        return

    for name, url, cookie_file in platforms:
        await crawl_merchant_platform(name, url, cookie_file)
        if len(platforms) > 1:
            print("\n" + "=" * 60)
            print("3秒后继续下一个平台...")
            print("=" * 60)
            await asyncio.sleep(3)

    print("\n" + "=" * 60)
    print("🎉 全部抓取完成！")
    print("=" * 60)


if __name__ == '__main__':
    asyncio.run(main())

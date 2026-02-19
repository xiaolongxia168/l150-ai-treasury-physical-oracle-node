#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
连接到现有的 openclaw 浏览器进行抓取
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.resolve()


async def find_tab_by_url(browser, url_pattern):
    """查找包含指定 URL 的标签页"""
    for context in browser.contexts:
        for page in context.pages:
            if url_pattern in page.url:
                logger.info(f"✓ 找到标签页: {page.url}")
                return page
    return None


async def discover_menu(page):
    """发现菜单 - 改进版，支持点击和链接"""
    menu_items = []

    # 尝试多种菜单选择器
    selectors = [
        # 侧边栏链接
        'aside a', '.sidebar a', '[class*="sidebar"] a',
        'nav a', '.nav a', '[class*="nav"] a',
        '.menu a', '[class*="menu"] a',
        # 可点击的菜单项（即使不是链接）
        'aside [role="menuitem"]', '.sidebar [role="menuitem"]',
        'aside li', '.sidebar li', '[class*="sidebar"] li',
        'nav li', '.menu li'
    ]

    for selector in selectors:
        try:
            elements = await page.query_selector_all(selector)
            logger.info(f"  尝试选择器 '{selector}': 找到 {len(elements)} 个元素")

            for elem in elements[:50]:
                try:
                    # 获取文本
                    text = (await elem.inner_text()).strip()
                    if not text or len(text) > 50 or text in ['', ' ']:
                        continue

                    # 尝试获取 href
                    href = await elem.get_attribute('href')

                    # 如果没有 href，尝试从子元素 a 标签获取
                    if not href:
                        link = await elem.query_selector('a')
                        if link:
                            href = await link.get_attribute('href')

                    # 如果仍然没有 href，检查是否可点击（data-* 属性等）
                    if not href:
                        # 检查 onclick 或其他点击属性
                        onclick = await elem.get_attribute('onclick')
                        data_url = await elem.get_attribute('data-url')
                        if onclick or data_url:
                            # 这是可点击元素，保存为元素引用
                            menu_items.append({
                                'text': text,
                                'element': elem,
                                'type': 'clickable'
                            })
                            continue

                    if href and href not in ['#', 'javascript:void(0)', 'javascript:;']:
                        # 构建完整 URL
                        if href.startswith('http'):
                            full_url = href
                        elif href.startswith('/'):
                            from urllib.parse import urljoin
                            full_url = urljoin(page.url, href)
                        else:
                            continue

                        # 去重
                        if not any(m.get('full_url') == full_url for m in menu_items):
                            menu_items.append({
                                'text': text,
                                'href': href,
                                'full_url': full_url,
                                'type': 'link'
                            })
                except Exception as e:
                    pass
        except Exception as e:
            pass

    logger.info(f"✓ 发现 {len(menu_items)} 个菜单项（链接 + 可点击）")
    return menu_items[:25]  # 限制 25 个


async def extract_page_data(page):
    """提取页面数据"""
    data = {
        'title': await page.title(),
        'url': page.url,
        'timestamp': datetime.now().isoformat(),
        'tables': [],
        'stats': [],
        'text_content': []
    }

    # 提取表格
    tables = await page.query_selector_all('table')
    for table in tables[:5]:
        try:
            headers = []
            for cell in await table.query_selector_all('thead th, thead td'):
                text = (await cell.inner_text()).strip()
                if text:
                    headers.append(text)

            rows = []
            table_rows = await table.query_selector_all('tbody tr')
            for row in table_rows[:50]:
                row_data = []
                cells = await row.query_selector_all('td, th')
                for cell in cells:
                    text = (await cell.inner_text()).strip()
                    row_data.append(text)
                if row_data:
                    rows.append(row_data)

            if headers or rows:
                data['tables'].append({'headers': headers, 'rows': rows})
        except:
            pass

    # 提取统计数字
    for selector in [
        '.stat', '.metric', '.count', '.number',
        '[class*="data"]', '[class*="stat"]',
        '[class*="count"]', '[class*="metric"]'
    ]:
        try:
            for elem in (await page.query_selector_all(selector))[:10]:
                text = (await elem.inner_text()).strip()
                if text and len(text) < 100:
                    data['stats'].append(text)
        except:
            pass

    # 提取主要文本内容
    try:
        main_selectors = ['main', '#app', '.content', '[class*="content"]']
        for selector in main_selectors:
            elem = await page.query_selector(selector)
            if elem:
                text = (await elem.inner_text()).strip()
                if text and len(text) > 50:
                    data['text_content'].append(text[:5000])  # 限制长度
                    break
    except:
        pass

    return data


async def crawl_platform(browser, platform_name, url_pattern):
    """抓取平台数据"""
    logger.info("=" * 60)
    logger.info(f"开始抓取: {platform_name}")
    logger.info(f"URL 模式: {url_pattern}")
    logger.info("=" * 60)

    # 查找标签页
    page = await find_tab_by_url(browser, url_pattern)

    if not page:
        logger.warning(f"⚠ 未找到 {platform_name} 的标签页，请确保浏览器中已打开该页面")
        return []

    all_data = []

    try:
        # 等待页面加载
        await page.wait_for_load_state('networkidle', timeout=10000)

        title = await page.title()
        current_url = page.url
        logger.info(f"✓ 页面标题: {title}")
        logger.info(f"✓ 当前 URL: {current_url}")

        # 截图
        screenshot_path = PROJECT_ROOT / 'logs' / f'{platform_name}_existing_{datetime.now().strftime("%H%M%S")}.png'
        screenshot_path.parent.mkdir(exist_ok=True)
        await page.screenshot(path=str(screenshot_path), full_page=True)
        logger.info(f"✓ 截图: {screenshot_path}")

        # 提取当前页面数据
        logger.info("提取当前页面数据...")
        data = await extract_page_data(page)
        data['menu_name'] = '首页'
        all_data.append(data)
        logger.info(f"  ✓ 提取: {len(data.get('tables', []))} 个表格, {len(data.get('stats', []))} 个统计")

        # 发现菜单
        logger.info("\n发现菜单...")
        menu_links = await discover_menu(page)

        if not menu_links:
            logger.warning("⚠ 未发现菜单链接，可能需要手动滚动页面或等待加载")
            return all_data

        logger.info(f"\n✓ 发现 {len(menu_links)} 个菜单入口:")
        for i, item in enumerate(menu_links, 1):
            if item['type'] == 'link':
                logger.info(f"  {i}. [{item['type']}] {item['text']} -> {item['full_url'][:80]}")
            else:
                logger.info(f"  {i}. [{item['type']}] {item['text']}")

        # 逐个抓取菜单
        for i, item in enumerate(menu_links, 1):
            logger.info(f"\n[{i}/{len(menu_links)}] 抓取菜单: {item['text']}")

            try:
                # 根据类型处理
                if item['type'] == 'link':
                    # 导航到菜单页面
                    await page.goto(item['full_url'], timeout=30000, wait_until='networkidle')
                elif item['type'] == 'clickable':
                    # 点击元素
                    await item['element'].click()

                await page.wait_for_timeout(2000)

                # 提取数据
                data = await extract_page_data(page)
                data['menu_name'] = link['text']
                all_data.append(data)

                tables = len(data.get('tables', []))
                stats = len(data.get('stats', []))
                logger.info(f"  ✓ 提取: {tables} 个表格, {stats} 个统计")

                # 简单翻页（最多 3 页）
                for page_num in range(2, 5):
                    next_selectors = [
                        'button:has-text("下一页")',
                        'a:has-text("下一页")',
                        '.ant-pagination-next',
                        '[class*="next"]'
                    ]

                    next_btn = None
                    for selector in next_selectors:
                        next_btn = await page.query_selector(selector)
                        if next_btn:
                            # 检查是否禁用
                            is_disabled = await next_btn.is_disabled() if hasattr(next_btn, 'is_disabled') else False
                            class_name = await next_btn.get_attribute('class') or ''
                            if not is_disabled and 'disabled' not in class_name:
                                break
                            next_btn = None

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

        logger.info(f"\n✓ 抓取完成！共 {len(all_data)} 个页面")

    except Exception as e:
        logger.error(f"抓取失败: {e}", exc_info=True)

    return all_data


async def main():
    """主函数"""
    print("🚀 连接到 openclaw 浏览器进行抓取")
    print("=" * 60)

    async with async_playwright() as p:
        try:
            # 连接到现有的 Chrome 实例
            logger.info("连接到 openclaw 浏览器（端口 18800）...")
            browser = await p.chromium.connect_over_cdp('http://localhost:18800')
            logger.info(f"✓ 已连接，共 {len(browser.contexts)} 个上下文")

            all_results = {}

            # 抓取抖音来客（使用正确的 URL）
            print("\n【1/2】抓取抖音来客...")
            douyin_data = await crawl_platform(browser, 'douyin_laike', 'douyin.com')
            all_results['douyin_laike'] = douyin_data

            print("\n" + "="*60)
            print("等待 5 秒...")
            await asyncio.sleep(5)

            # 抓取美团开店宝（使用正确的 URL）
            print("\n【2/2】抓取美团开店宝...")
            meituan_data = await crawl_platform(browser, 'meituan_kaidian', 'e.dianping.com')
            all_results['meituan_kaidian'] = meituan_data

            # 保存所有数据
            for platform_name, data in all_results.items():
                if data:
                    output_path = PROJECT_ROOT / 'data' / f'{platform_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                    output_path.parent.mkdir(exist_ok=True)

                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)

                    size = output_path.stat().st_size / 1024
                    logger.info(f"✓ {platform_name} 数据已保存: {output_path} ({size:.2f} KB)")

            print("\n" + "="*60)
            print(f"🎉 全部抓取完成！")
            print("="*60)
            print(f"\n统计:")
            print(f"  抖音来客: {len(douyin_data)} 个页面")
            print(f"  美团开店宝: {len(meituan_data)} 个页面")
            print(f"\n查看结果：")
            print(f"  ls -lh {PROJECT_ROOT / 'data'}")

            # 断开连接（不关闭浏览器）
            await browser.close()

        except Exception as e:
            logger.error(f"连接失败: {e}", exc_info=True)
            print("\n⚠ 提示：")
            print("1. 确保 openclaw 浏览器正在运行")
            print("2. 确保已经在浏览器中登录了抖音来客和美团开店宝")
            print("3. 确保浏览器标签页已打开这两个网站")


if __name__ == '__main__':
    asyncio.run(main())

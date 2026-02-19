#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能爬虫 - 自动发现并点击所有菜单项
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


async def find_all_clickable_menu_items(page):
    """智能发现所有可点击的菜单项"""
    logger.info("开始智能菜单发现...")

    # 执行 JavaScript 在浏览器中查找所有可能的菜单项
    menu_items = await page.evaluate("""
        () => {
            const items = [];
            const seen = new Set();

            // 查找左侧区域的所有可能元素
            const leftElements = Array.from(document.querySelectorAll('*')).filter(el => {
                const rect = el.getBoundingClientRect();
                // 左侧 300px 以内，有文本内容，可见
                return rect.left < 300 &&
                       rect.width > 0 &&
                       rect.height > 0 &&
                       rect.height < 100 &&  // 不要太高（避免容器）
                       el.textContent &&
                       el.textContent.trim().length > 0 &&
                       el.textContent.trim().length < 50;
            });

            leftElements.forEach(el => {
                const text = el.textContent.trim();
                const tag = el.tagName.toLowerCase();

                // 跳过已见过的文本或包含换行的
                if (seen.has(text) || text === '' || text.includes('\\n')) {
                    return;
                }

                // 检查是否可点击
                const style = window.getComputedStyle(el);
                const hasClickCursor = style.cursor === 'pointer';
                const hasOnClick = el.onclick !== null;

                // 检查父元素是否可点击
                let parent = el.parentElement;
                let parentClickable = false;
                for (let i = 0; i < 3 && parent; i++) {
                    const parentStyle = window.getComputedStyle(parent);
                    if (parentStyle.cursor === 'pointer' || parent.onclick !== null) {
                        parentClickable = true;
                        break;
                    }
                    parent = parent.parentElement;
                }

                if (hasClickCursor || hasOnClick || parentClickable || tag === 'a' || tag === 'button') {
                    seen.add(text);
                    items.push({text: text, tag: tag});
                }
            });

            return items;
        }
    """)

    logger.info(f"✓ 发现 {len(menu_items)} 个可能的菜单项")
    return menu_items


async def extract_page_data(page, page_name):
    """提取页面数据"""
    try:
        data = {
            'name': page_name,
            'title': await page.title(),
            'url': page.url,
            'timestamp': datetime.now().isoformat(),
            'content': {}
        }

        # 提取页面文本内容
        content = await page.evaluate("""
            () => {
                const selectors = ['main', '#app', '[class*="content"]', 'body'];
                for (const sel of selectors) {
                    const elem = document.querySelector(sel);
                    if (elem) {
                        const text = elem.innerText || elem.textContent;
                        if (text && text.length > 100) {
                            return text.substring(0, 10000);
                        }
                    }
                }
                return '';
            }
        """)

        data['content']['text'] = content

        # 提取所有表格
        tables = await page.evaluate("""
            () => {
                const tables = [];
                document.querySelectorAll('table').forEach(table => {
                    const headers = Array.from(table.querySelectorAll('thead th, thead td')).map(th => th.innerText.trim());
                    const rows = Array.from(table.querySelectorAll('tbody tr')).slice(0, 50).map(tr => {
                        return Array.from(tr.querySelectorAll('td, th')).map(td => td.innerText.trim());
                    });
                    if (headers.length > 0 || rows.length > 0) {
                        tables.push({headers, rows});
                    }
                });
                return tables;
            }
        """)

        data['content']['tables'] = tables

        logger.info(f"  ✓ 提取: {len(tables)} 个表格, 文本 {len(content)} 字符")
        return data

    except Exception as e:
        logger.error(f"  ✗ 提取数据失败: {e}")
        return None


async def crawl_platform(browser, platform_name, url_pattern):
    """智能抓取平台"""
    logger.info("=" * 60)
    logger.info(f"智能抓取: {platform_name}")
    logger.info(f"URL 模式: {url_pattern}")
    logger.info("=" * 60)

    # 查找标签页
    page = None
    for context in browser.contexts:
        for p in context.pages:
            if url_pattern in p.url:
                page = p
                logger.info(f"✓ 找到标签页: {p.url}")
                break
        if page:
            break

    if not page:
        logger.warning(f"⚠ 未找到 {platform_name} 的标签页")
        return []

    all_data = []

    try:
        # 等待页面加载
        await page.wait_for_load_state('domcontentloaded', timeout=10000)

        title = await page.title()
        logger.info(f"✓ 页面标题: {title}")

        # 截图首页
        screenshot_path = PROJECT_ROOT / 'logs' / f'{platform_name}_home_{datetime.now().strftime("%H%M%S")}.png'
        screenshot_path.parent.mkdir(exist_ok=True)
        await page.screenshot(path=str(screenshot_path), full_page=True)
        logger.info(f"✓ 截图: {screenshot_path}")

        # 提取首页数据
        home_data = await extract_page_data(page, '首页')
        if home_data:
            all_data.append(home_data)

        # 智能发现菜单
        menu_items = await find_all_clickable_menu_items(page)

        if not menu_items:
            logger.warning("⚠ 未发现菜单项")
            return all_data

        logger.info(f"\n菜单项列表:")
        for i, item in enumerate(menu_items[:30], 1):
            logger.info(f"  {i}. {item['text']}")

        # 逐个点击菜单项
        clicked = set()
        for i, item in enumerate(menu_items[:20], 1):
            if item['text'] in clicked:
                continue

            logger.info(f"\n[{i}/20] 点击菜单: {item['text']}")

            try:
                element = page.locator(f"text={item['text']}").first
                await element.click(timeout=5000)
                clicked.add(item['text'])
                await page.wait_for_timeout(2000)

                # 提取数据
                data = await extract_page_data(page, item['text'])
                if data:
                    all_data.append(data)

                # 简单截图
                if i <= 10:
                    ss_path = PROJECT_ROOT / 'logs' / f'{platform_name}_menu{i}_{datetime.now().strftime("%H%M%S")}.png'
                    await page.screenshot(path=str(ss_path))

            except Exception as e:
                logger.error(f"  ✗ 失败: {e}")

        logger.info(f"\n✓ 共抓取 {len(all_data)} 个页面")

    except Exception as e:
        logger.error(f"抓取失败: {e}", exc_info=True)

    return all_data


async def main():
    """主函数"""
    print("🤖 智能爬虫 - 自动发现菜单并抓取")
    print("=" * 60)

    async with async_playwright() as p:
        try:
            logger.info("连接到 openclaw 浏览器（端口 18800）...")
            browser = await p.chromium.connect_over_cdp('http://localhost:18800')
            logger.info(f"✓ 已连接\n")

            all_results = {}

            # 抓取抖音来客
            print("\n【1/2】智能抓取抖音来客...")
            douyin_data = await crawl_platform(browser, 'douyin_laike', 'douyin.com')
            all_results['douyin_laike'] = douyin_data

            print("\n" + "="*60)
            print("等待 5 秒...")
            await asyncio.sleep(5)

            # 抓取美团
            print("\n【2/2】智能抓取美团开店宝...")
            meituan_data = await crawl_platform(browser, 'meituan_kaidian', 'dianping.com')
            all_results['meituan_kaidian'] = meituan_data

            # 保存数据
            for platform_name, data in all_results.items():
                if data:
                    output_path = PROJECT_ROOT / 'data' / f'{platform_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                    output_path.parent.mkdir(exist_ok=True)

                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)

                    size = output_path.stat().st_size / 1024
                    logger.info(f"✓ {platform_name} 数据已保存: {output_path} ({size:.2f} KB)")

            print("\n" + "="*60)
            print("🎉 智能抓取完成！")
            print("="*60)
            print(f"\n统计:")
            print(f"  抖音来客: {len(douyin_data)} 个页面")
            print(f"  美团开店宝: {len(meituan_data)} 个页面")
            print(f"\n查看数据：")
            print(f"  ls -lh {PROJECT_ROOT / 'data'}")

            await browser.close()

        except Exception as e:
            logger.error(f"失败: {e}", exc_info=True)


if __name__ == '__main__':
    asyncio.run(main())

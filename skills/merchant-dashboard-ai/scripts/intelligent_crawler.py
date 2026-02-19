#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能全量爬虫 - 自动发现并抓取所有页面数据
功能：
1. 自动发现所有菜单和链接
2. 递归点击进入所有子页面
3. 自动翻页抓取分页数据
4. 提取表格、列表、图表等所有数据
5. 智能去重，避免重复抓取
"""

import asyncio
import json
import logging
import hashlib
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright
from urllib.parse import urlparse, urljoin

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


class IntelligentCrawler:
    """智能全量爬虫"""

    def __init__(self, platform_config, headless=True):
        self.platform_config = platform_config
        self.headless = headless
        self.visited_urls = set()  # 已访问的 URL
        self.visited_hashes = set()  # 已抓取的页面内容哈希
        self.all_data = []  # 收集的所有数据
        self.menu_structure = {}  # 菜单结构
        self.browser = None
        self.context = None
        self.page = None

    async def init(self):
        """初始化浏览器"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context()

        # 加载 Cookie
        cookie_file = self.platform_config.get('cookie_file')
        if cookie_file and Path(cookie_file).exists():
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
            await self.context.add_cookies(cookies)
            logger.info(f"已加载 Cookie: {cookie_file}")

        self.page = await self.context.new_page()

    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()

    async def discover_menu_structure(self):
        """
        发现菜单结构
        自动识别导航菜单、侧边栏、顶部菜单等
        """
        logger.info("正在发现菜单结构...")

        # 常见的菜单选择器
        menu_selectors = [
            'nav a',  # 导航链接
            '.sidebar a',  # 侧边栏链接
            '.menu a',  # 菜单链接
            '[class*="nav"] a',  # 包含 nav 的链接
            '[class*="menu"] a',  # 包含 menu 的链接
            '[role="navigation"] a',  # 语义化导航
            'aside a',  # 侧边栏
        ]

        menu_links = []

        for selector in menu_selectors:
            try:
                links = await self.page.query_selector_all(selector)
                for link in links:
                    href = await link.get_attribute('href')
                    text = await link.inner_text()
                    if href and text:
                        menu_links.append({
                            'text': text.strip(),
                            'href': href,
                            'selector': selector
                        })
            except:
                continue

        # 去重
        unique_links = {}
        for link in menu_links:
            href = link['href']
            if href not in unique_links:
                unique_links[href] = link

        self.menu_structure = unique_links
        logger.info(f"发现 {len(unique_links)} 个菜单入口")

        return unique_links

    async def crawl_page(self, url, depth=0, max_depth=3):
        """
        递归抓取页面
        :param url: 页面 URL
        :param depth: 当前深度
        :param max_depth: 最大深度
        """
        if depth > max_depth:
            logger.debug(f"达到最大深度 {max_depth}，跳过: {url}")
            return

        # 检查是否已访问
        if url in self.visited_urls:
            logger.debug(f"已访问，跳过: {url}")
            return

        self.visited_urls.add(url)

        try:
            logger.info(f"[深度 {depth}] 正在抓取: {url}")

            # 访问页面
            await self.page.goto(url, wait_until='networkidle', timeout=30000)
            await self.page.wait_for_timeout(2000)  # 等待动态内容加载

            # 提取当前页面数据
            page_data = await self.extract_page_data()

            # 检查内容是否重复
            content_hash = self.hash_data(page_data)
            if content_hash not in self.visited_hashes:
                self.visited_hashes.add(content_hash)
                page_data['url'] = url
                page_data['depth'] = depth
                page_data['timestamp'] = datetime.now().isoformat()
                self.all_data.append(page_data)
                logger.info(f"✓ 抓取数据: {len(page_data.get('tables', []))} 个表格, "
                          f"{len(page_data.get('lists', []))} 个列表")
            else:
                logger.debug("内容重复，跳过保存")

            # 检查并处理分页
            await self.handle_pagination(url, depth)

            # 发现新链接
            new_links = await self.discover_links()

            # 递归抓取新链接
            for link_url in new_links:
                await self.crawl_page(link_url, depth + 1, max_depth)

        except Exception as e:
            logger.error(f"抓取失败 {url}: {e}")

    async def extract_page_data(self):
        """
        提取页面所有数据
        包括：表格、列表、统计数字、图表数据等
        """
        data = {
            'title': await self.page.title(),
            'url': self.page.url,
            'tables': [],
            'lists': [],
            'statistics': [],
            'forms': [],
            'charts': []
        }

        # 1. 提取所有表格数据
        tables = await self.page.query_selector_all('table')
        for table in tables:
            table_data = await self.extract_table(table)
            if table_data:
                data['tables'].append(table_data)

        # 2. 提取列表数据
        lists = await self.page.query_selector_all('ul, ol')
        for lst in lists:
            list_data = await self.extract_list(lst)
            if list_data and len(list_data) > 0:
                data['lists'].append(list_data)

        # 3. 提取统计数字（常见的仪表板数据）
        stat_selectors = [
            '[class*="stat"]',
            '[class*="metric"]',
            '[class*="count"]',
            '[class*="number"]',
            '.card',
            '[class*="summary"]'
        ]

        for selector in stat_selectors:
            try:
                elements = await self.page.query_selector_all(selector)
                for elem in elements:
                    text = await elem.inner_text()
                    if text and len(text) < 200:  # 过滤太长的文本
                        data['statistics'].append(text.strip())
            except:
                continue

        # 4. 提取表单数据（用于了解可操作的功能）
        forms = await self.page.query_selector_all('form')
        for form in forms:
            form_data = await self.extract_form(form)
            if form_data:
                data['forms'].append(form_data)

        # 5. 尝试提取图表数据（如果使用 ECharts、Chart.js 等）
        try:
            chart_data = await self.page.evaluate('''() => {
                const charts = [];
                // ECharts
                if (window.echarts) {
                    const instances = echarts.getInstanceByDom ?
                        Array.from(document.querySelectorAll('[_echarts_instance_]')).map(
                            el => echarts.getInstanceByDom(el)
                        ) : [];
                    instances.forEach(chart => {
                        if (chart) {
                            charts.push({
                                type: 'echarts',
                                option: chart.getOption()
                            });
                        }
                    });
                }
                // Chart.js
                if (window.Chart && window.Chart.instances) {
                    Object.values(window.Chart.instances).forEach(chart => {
                        charts.push({
                            type: 'chartjs',
                            data: chart.data,
                            config: chart.config
                        });
                    });
                }
                return charts;
            }''')
            if chart_data:
                data['charts'] = chart_data
        except:
            pass

        return data

    async def extract_table(self, table_element):
        """提取表格数据"""
        try:
            # 提取表头
            headers = []
            header_cells = await table_element.query_selector_all('thead th, thead td')
            for cell in header_cells:
                text = await cell.inner_text()
                headers.append(text.strip())

            # 提取行数据
            rows = []
            body_rows = await table_element.query_selector_all('tbody tr')
            for row in body_rows:
                cells = await row.query_selector_all('td, th')
                row_data = []
                for cell in cells:
                    text = await cell.inner_text()
                    row_data.append(text.strip())
                if row_data:
                    rows.append(row_data)

            if headers or rows:
                return {
                    'headers': headers,
                    'rows': rows,
                    'row_count': len(rows)
                }
        except:
            pass
        return None

    async def extract_list(self, list_element):
        """提取列表数据"""
        try:
            items = await list_element.query_selector_all('li')
            list_data = []
            for item in items:
                text = await item.inner_text()
                if text:
                    list_data.append(text.strip())
            return list_data
        except:
            return []

    async def extract_form(self, form_element):
        """提取表单结构"""
        try:
            inputs = await form_element.query_selector_all('input, select, textarea')
            fields = []
            for inp in inputs:
                field = {
                    'type': await inp.get_attribute('type') or 'text',
                    'name': await inp.get_attribute('name'),
                    'placeholder': await inp.get_attribute('placeholder'),
                }
                fields.append(field)
            return {'fields': fields} if fields else None
        except:
            return None

    async def handle_pagination(self, base_url, depth):
        """
        处理分页，自动翻页抓取所有页面数据
        """
        # 常见的分页按钮选择器
        next_selectors = [
            'a:has-text("下一页")',
            'button:has-text("下一页")',
            '[class*="next"]',
            '[class*="pagination"] a:last-child',
            '.ant-pagination-next',  # Ant Design
            '.el-pagination__next',  # Element UI
        ]

        page_count = 0
        max_pages = 50  # 最多翻页数

        while page_count < max_pages:
            # 尝试找到"下一页"按钮
            next_button = None
            for selector in next_selectors:
                try:
                    next_button = await self.page.query_selector(selector)
                    if next_button:
                        is_disabled = await next_button.get_attribute('disabled')
                        aria_disabled = await next_button.get_attribute('aria-disabled')
                        if not is_disabled and aria_disabled != 'true':
                            break
                        else:
                            next_button = None
                except:
                    continue

            if not next_button:
                logger.debug("没有更多分页")
                break

            # 点击下一页
            try:
                await next_button.click()
                await self.page.wait_for_timeout(2000)

                # 提取当前页数据
                page_data = await self.extract_page_data()
                content_hash = self.hash_data(page_data)

                if content_hash not in self.visited_hashes:
                    self.visited_hashes.add(content_hash)
                    page_data['url'] = f"{base_url}#page{page_count + 2}"
                    page_data['depth'] = depth
                    page_data['pagination'] = page_count + 2
                    self.all_data.append(page_data)
                    logger.info(f"✓ 抓取第 {page_count + 2} 页数据")
                    page_count += 1
                else:
                    logger.debug("分页内容重复，停止翻页")
                    break

            except Exception as e:
                logger.error(f"翻页失败: {e}")
                break

    async def discover_links(self):
        """
        发现当前页面的所有链接
        智能过滤外部链接、无效链接
        """
        links = set()
        base_url = self.page.url

        # 提取所有链接
        link_elements = await self.page.query_selector_all('a[href]')

        for elem in link_elements:
            href = await elem.get_attribute('href')
            if not href:
                continue

            # 处理相对链接
            full_url = urljoin(base_url, href)

            # 过滤条件
            parsed = urlparse(full_url)
            base_parsed = urlparse(base_url)

            # 只抓取同域名下的链接
            if parsed.netloc != base_parsed.netloc:
                continue

            # 过滤锚点、JavaScript 等
            if href.startswith('#') or href.startswith('javascript:'):
                continue

            # 过滤登出、删除等危险操作
            dangerous_keywords = ['logout', 'delete', 'remove', 'signout']
            if any(keyword in href.lower() for keyword in dangerous_keywords):
                continue

            links.add(full_url)

        return links

    def hash_data(self, data):
        """计算数据哈希，用于去重"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()

    async def crawl_all(self, start_url):
        """
        从起始 URL 开始，全量抓取
        """
        logger.info("=" * 60)
        logger.info("智能全量爬虫启动")
        logger.info(f"起始 URL: {start_url}")
        logger.info("=" * 60)

        try:
            await self.init()

            # 访问起始页面
            await self.page.goto(start_url, wait_until='networkidle')
            await self.page.wait_for_timeout(3000)

            # 发现菜单结构
            menu = await self.discover_menu_structure()

            # 抓取所有菜单页面
            for href, link_info in menu.items():
                full_url = urljoin(start_url, href)
                logger.info(f"\n开始抓取菜单: {link_info['text']} -> {full_url}")
                await self.crawl_page(full_url, depth=0, max_depth=2)

            logger.info("=" * 60)
            logger.info(f"抓取完成！")
            logger.info(f"总计访问: {len(self.visited_urls)} 个 URL")
            logger.info(f"总计抓取: {len(self.all_data)} 个页面数据")
            logger.info("=" * 60)

            return self.all_data

        except Exception as e:
            logger.error(f"爬虫失败: {e}", exc_info=True)
            raise
        finally:
            await self.close()


async def main():
    """测试"""
    # 测试配置
    config = {
        'name': '抖音来客',
        'login_url': 'https://laike.douyin.com/',
        'cookie_file': '../cookies/douyin_laike.json'
    }

    crawler = IntelligentCrawler(config, headless=False)

    try:
        data = await crawler.crawl_all('https://laike.douyin.com/')

        # 保存数据
        output_file = f'../data/full_crawl_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"\n数据已保存: {output_file}")
        logger.info(f"文件大小: {Path(output_file).stat().st_size / 1024:.2f} KB")

    except Exception as e:
        logger.error(f"执行失败: {e}")


if __name__ == '__main__':
    asyncio.run(main())

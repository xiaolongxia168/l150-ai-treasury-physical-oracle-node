#!/usr/bin/env python3
"""
Playwright自动化数据抓取脚本
运行前请确保已安装: pip install playwright
并安装浏览器: playwright install
"""

import asyncio
import json
import csv
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

class AutoScraper:
    def __init__(self):
        self.data_dir = Path.home() / ".openclaw/workspace/密室逃脱运营/数据"
        self.results = {}
        
    async def scrape_douyin(self, page):
        """抓取抖音来客数据"""
        print("🎵 抓取抖音数据...")
        
        # 等待页面加载
        await page.wait_for_load_state('networkidle')
        
        # 抓取视频数据
        video_data = []
        try:
            # 点击数据菜单
            await page.click('text=数据')
            await page.wait_for_timeout(2000)
            
            # 点击视频分析
            await page.click('text=视频分析')
            await page.wait_for_timeout(3000)
            
            # 提取视频列表数据
            videos = await page.query_selector_all('.video-item')  # 需要根据实际页面调整选择器
            
            for video in videos[:20]:  # 抓取前20条
                try:
                    title = await video.query_selector_eval('.video-title', 'el => el.textContent')
                    plays = await video.query_selector_eval('.play-count', 'el => el.textContent')
                    likes = await video.query_selector_eval('.like-count', 'el => el.textContent')
                    
                    video_data.append({
                        'title': title,
                        'plays': plays,
                        'likes': likes,
                        'scraped_at': datetime.now().isoformat()
                    })
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ 抖音数据抓取部分失败: {e}")
            
        self.results['douyin_videos'] = video_data
        return video_data
    
    async def scrape_meituan(self, page):
        """抓取美团开店宝数据"""
        print("🍜 抓取美团数据...")
        
        await page.wait_for_load_state('networkidle')
        
        meituan_data = []
        try:
            # 点击经营分析
            await page.click('text=经营分析')
            await page.wait_for_timeout(2000)
            
            # 抓取交易数据
            # 这里需要根据实际页面结构调整
            
        except Exception as e:
            print(f"⚠️ 美团数据抓取部分失败: {e}")
            
        self.results['meituan'] = meituan_data
        return meituan_data
    
    def save_results(self):
        """保存抓取结果"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存为JSON
        json_file = self.data_dir / f"scraped_data_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
            
        # 保存为CSV（如果有视频数据）
        if 'douyin_videos' in self.results:
            csv_file = self.data_dir / f"douyin_videos_{timestamp}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if self.results['douyin_videos']:
                    writer = csv.DictWriter(f, fieldnames=self.results['douyin_videos'][0].keys())
                    writer.writeheader()
                    writer.writerows(self.results['douyin_videos'])
                    
        print(f"✅ 数据已保存到: {self.data_dir}")
        return json_file

async def main():
    scraper = AutoScraper()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # 可见模式便于调试
        
        # 抓取抖音
        print("\n🌐 打开抖音来客...")
        page = await browser.new_page()
        await page.goto('https://e.douyin.com/')
        print("⏳ 请在浏览器中完成登录，然后按回车继续...")
        input()
        
        await scraper.scrape_douyin(page)
        
        # 抓取美团
        print("\n🌐 打开美团开店宝...")
        page2 = await browser.new_page()
        await page2.goto('https://e.waimai.meituan.com/')
        print("⏳ 请在浏览器中完成登录，然后按回车继续...")
        input()
        
        await scraper.scrape_meituan(page2)
        
        # 保存结果
        scraper.save_results()
        
        await browser.close()
        print("\n✅ 数据抓取完成！")

if __name__ == '__main__':
    asyncio.run(main())

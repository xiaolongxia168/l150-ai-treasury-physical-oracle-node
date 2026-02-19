#!/usr/bin/env python3
"""
抖音来客 + 美团开店宝 全自动化数据抓取系统
店铺: 有點方真人恐怖密室(解放西路店)
作者: OpenClaw Agent
创建时间: 2026-02-19
"""

import json
import os
import sys
import time
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 数据存储路径
DATA_DIR = Path("/Users/xiaolongxia/.openclaw/workspace/data/merchant-dashboard")
LOGS_DIR = Path("/Users/xiaolongxia/.openclaw/workspace/data/merchant-dashboard/logs")

# 确保目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

class MerchantDataScraper:
    """商家数据抓取器基类"""
    
    def __init__(self, platform: str, shop_name: str):
        self.platform = platform
        self.shop_name = shop_name
        self.data_file = DATA_DIR / f"{platform}_data.json"
        self.daily_file = DATA_DIR / f"{platform}_{datetime.now().strftime('%Y%m%d')}.json"
        
    def save_data(self, data: Dict[str, Any]) -> bool:
        """保存抓取的数据"""
        try:
            # 添加时间戳
            data['scraped_at'] = datetime.now().isoformat()
            data['platform'] = self.platform
            data['shop_name'] = self.shop_name
            
            # 保存最新数据
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 追加到每日数据
            daily_data = []
            if self.daily_file.exists():
                with open(self.daily_file, 'r', encoding='utf-8') as f:
                    daily_data = json.load(f)
            
            daily_data.append(data)
            with open(self.daily_file, 'w', encoding='utf-8') as f:
                json.dump(daily_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ {self.platform} 数据已保存")
            return True
            
        except Exception as e:
            logger.error(f"❌ {self.platform} 保存数据失败: {e}")
            return False

class DouyinLaikeScraper(MerchantDataScraper):
    """抖音来客数据抓取器"""
    
    def __init__(self):
        super().__init__("douyin_laike", "有点方恐怖密室")
        self.cdp_url = "http://127.0.0.1:18800"
        self.target_id = "BC46658819424548E9D3919CF3963E96"
        
    async def scrape(self) -> Dict[str, Any]:
        """抓取抖音来客数据"""
        logger.info("🎯 开始抓取抖音来客数据...")
        
        # 这里通过Playwright连接已打开的浏览器
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            # 连接到已运行的浏览器
            browser = await p.chromium.connect_over_cdp(self.cdp_url)
            
            # 获取指定页面
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            
            # 查找目标页面
            target_page = None
            for page in context.pages:
                if "life.douyin.com" in page.url:
                    target_page = page
                    break
            
            if not target_page:
                logger.error("❌ 未找到抖音来客页面")
                return {}
            
            # 刷新页面获取最新数据
            await target_page.reload(wait_until="networkidle")
            await asyncio.sleep(3)  # 等待数据加载
            
            # 抓取经营数据
            data = await target_page.evaluate("""
                () => {
                    const result = {};
                    
                    // 抓取成交金额
                    const dealAmount = document.querySelector('[class*="成交"]:not([class*="券"])');
                    if (dealAmount) {
                        const amountText = dealAmount.closest('div')?.textContent || '';
                        const match = amountText.match(/¥\s*([\d,.]+)/);
                        if (match) result.deal_amount = parseFloat(match[1].replace(',', ''));
                    }
                    
                    // 抓取成交券数
                    const dealCount = document.querySelector('[class*="成交券数"]');
                    if (dealCount) {
                        const countText = dealCount.closest('div')?.textContent || '';
                        const match = countText.match(/(\d+)/);
                        if (match) result.deal_count = parseInt(match[1]);
                    }
                    
                    // 抓取核销金额
                    const verifyAmount = document.querySelector('[class*="核销金额"]');
                    if (verifyAmount) {
                        const amountText = verifyAmount.closest('div')?.textContent || '';
                        const match = amountText.match(/¥\s*([\d,.]+)/);
                        if (match) result.verify_amount = parseFloat(match[1].replace(',', ''));
                    }
                    
                    // 抓取退款金额
                    const refundAmount = document.querySelector('[class*="退款金额"]');
                    if (refundAmount) {
                        const amountText = refundAmount.closest('div')?.textContent || '';
                        const match = amountText.match(/¥\s*([\d,.]+)/);
                        if (match) result.refund_amount = parseFloat(match[1].replace(',', ''));
                    }
                    
                    // 抓取商品访问人数
                    const visitCount = document.querySelector('[class*="访问人数"]');
                    if (visitCount) {
                        const visitText = visitCount.closest('div')?.textContent || '';
                        const match = visitText.match(/(\d+)/);
                        if (match) result.visit_count = parseInt(match[1]);
                    }
                    
                    // 抓取经营分
                    const scoreElement = document.querySelector('[class*="经营分"], [class*="总分"]');
                    if (scoreElement) {
                        const scoreText = scoreElement.textContent || '';
                        const match = scoreText.match(/(\d+)/);
                        if (match) result.business_score = parseInt(match[1]);
                    }
                    
                    // 抓取账户余额
                    const balanceElement = document.querySelector('[class*="账户总余额"], [class*="余额"]');
                    if (balanceElement) {
                        const balanceText = balanceElement.closest('div')?.textContent || '';
                        const match = balanceText.match(/¥\s*([\d,.]+)/);
                        if (match) result.account_balance = parseFloat(match[1].replace(',', ''));
                    }
                    
                    // 抓取本地推消耗
                    const adSpend = document.querySelector('[class*="总消耗"]');
                    if (adSpend) {
                        const spendText = adSpend.closest('div')?.textContent || '';
                        const match = spendText.match(/¥\s*([\d,.]+)/);
                        if (match) result.ad_spend = parseFloat(match[1].replace(',', ''));
                    }
                    
                    // 抓取消息数量
                    const msgElements = document.querySelectorAll('[class*="消息"], [class*="顾客咨询"]');
                    msgElements.forEach(el => {
                        const text = el.textContent || '';
                        if (text.includes('消息')) {
                            const match = text.match(/(\d+)/);
                            if (match) result.message_count = parseInt(match[1]);
                        }
                        if (text.includes('顾客咨询')) {
                            const match = text.match(/(\d+)/);
                            if (match) result.consultation_count = parseInt(match[1]);
                        }
                    });
                    
                    // 抓取团购商品数量
                    const productCount = document.querySelector('[class*="团购商品"]');
                    if (productCount) {
                        const text = productCount.textContent || '';
                        const match = text.match(/(\d+)/);
                        if (match) result.product_count = parseInt(match[1]);
                    }
                    
                    // 抓取违规状态
                    const violationStatus = document.querySelector('[class*="违规状态"]');
                    if (violationStatus) {
                        const text = violationStatus.closest('div')?.textContent || '';
                        result.violation_status = text.includes('正常') ? '正常' : '违规生效中';
                    }
                    
                    return result;
                }
            """)
            
            await browser.close()
            
            # 添加元数据
            data['shop_name'] = self.shop_name
            data['platform'] = 'douyin_laike'
            
            logger.info(f"✅ 抖音来客数据抓取完成: {len(data)} 个字段")
            return data
            
        except Exception as e:
            logger.error(f"❌ 抖音来客抓取失败: {e}")
            return {}

class MeituanDianpingScraper(MerchantDataScraper):
    """美团点评数据抓取器"""
    
    def __init__(self):
        super().__init__("meituan_dianping", "有點方真人恐怖密室(解放西路店)")
        self.cdp_url = "http://127.0.0.1:18800"
        self.target_id = "D1DB63DC8AC30B78DB4DA4B74D884A20"
        
    async def scrape(self) -> Dict[str, Any]:
        """抓取美团点评数据"""
        logger.info("🎯 开始抓取美团点评数据...")
        
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(self.cdp_url)
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            
            # 查找目标页面
            target_page = None
            for page in context.pages:
                if "dianping.com" in page.url or "meituan.com" in page.url:
                    target_page = page
                    break
            
            if not target_page:
                logger.error("❌ 未找到美团点评页面")
                return {}
            
            # 刷新页面
            await target_page.reload(wait_until="networkidle")
            await asyncio.sleep(3)
            
            # 抓取数据
            data = await target_page.evaluate("""
                () => {
                    const result = {};
                    
                    // 抓取访问人数
                    const visitElements = document.querySelectorAll('*');
                    visitElements.forEach(el => {
                        const text = el.textContent || '';
                        if (text.includes('访问人数')) {
                            const parent = el.closest('div');
                            if (parent) {
                                const numText = parent.textContent.match(/(\d+)/);
                                if (numText && !result.visit_count) {
                                    result.visit_count = parseInt(numText[1]);
                                }
                            }
                        }
                    });
                    
                    // 抓取下单金额
                    const orderAmount = [...document.querySelectorAll('*')].find(el => 
                        el.textContent?.includes('下单金额')
                    );
                    if (orderAmount) {
                        const parent = orderAmount.closest('div');
                        if (parent) {
                            const numText = parent.textContent.match(/(\d+)/);
                            if (numText) result.order_amount = parseInt(numText[1]);
                        }
                    }
                    
                    // 抓取核销金额
                    const verifyAmount = [...document.querySelectorAll('*')].find(el => 
                        el.textContent?.includes('核销金额')
                    );
                    if (verifyAmount) {
                        const parent = verifyAmount.closest('div');
                        if (parent) {
                            const numText = parent.textContent.match(/(\d+)/);
                            if (numText) result.verify_amount = parseInt(numText[1]);
                        }
                    }
                    
                    // 抓取经营评分
                    const scoreElements = document.querySelectorAll('*');
                    scoreElements.forEach(el => {
                        const text = el.textContent || '';
                        if (text.includes('当前评分') || text.includes('经营评分')) {
                            const parent = el.closest('div, span');
                            if (parent) {
                                const scoreMatch = parent.textContent.match(/(\d+\.?\d*)/);
                                if (scoreMatch && !result.business_score) {
                                    result.business_score = parseFloat(scoreMatch[1]);
                                }
                            }
                        }
                    });
                    
                    // 抓取新增评论数
                    const newComments = [...document.querySelectorAll('*')].find(el => 
                        el.textContent?.includes('新增评论数')
                    );
                    if (newComments) {
                        const parent = newComments.closest('div');
                        if (parent) {
                            const match = parent.textContent.match(/(\d+)/);
                            if (match) result.new_comments = parseInt(match[1]);
                        }
                    }
                    
                    // 抓取新增差评数
                    const newBadComments = [...document.querySelectorAll('*')].find(el => 
                        el.textContent?.includes('新增差评数')
                    );
                    if (newBadComments) {
                        const parent = newBadComments.closest('div');
                        if (parent) {
                            const match = parent.textContent.match(/(\d+)/);
                            if (match) result.new_bad_comments = parseInt(match[1]);
                        }
                    }
                    
                    // 抓取通知数量
                    const noticeElements = document.querySelectorAll('[href*="notice"], [class*="通知"]');
                    noticeElements.forEach(el => {
                        const text = el.textContent || '';
                        const match = text.match(/(\d+)/);
                        if (match && !result.notice_count) {
                            result.notice_count = parseInt(match[1]);
                        }
                    });
                    
                    // 抓取消息数量
                    const msgElements = document.querySelectorAll('[href*="im"], [class*="消息"]');
                    msgElements.forEach(el => {
                        const text = el.textContent || '';
                        const match = text.match(/(\d+)/);
                        if (match && !result.message_count) {
                            result.message_count = parseInt(match[1]);
                        }
                    });
                    
                    // 抓取数据更新时间
                    const updateTime = [...document.querySelectorAll('*')].find(el => 
                        el.textContent?.includes('数据更新时间')
                    );
                    if (updateTime) {
                        const match = updateTime.textContent.match(/(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})/);
                        if (match) result.data_update_time = match[1];
                    }
                    
                    return result;
                }
            """)
            
            await browser.close()
            
            data['shop_name'] = self.shop_name
            data['platform'] = 'meituan_dianping'
            
            logger.info(f"✅ 美团点评数据抓取完成: {len(data)} 个字段")
            return data
            
        except Exception as e:
            logger.error(f"❌ 美团点评抓取失败: {e}")
            return {}

async def main():
    """主函数 - 执行全量抓取"""
    logger.info("=" * 60)
    logger.info("🚀 商家数据全自动化抓取系统启动")
    logger.info("=" * 60)
    
    results = {}
    
    # 抓取抖音来客数据
    douyin_scraper = DouyinLaikeScraper()
    douyin_data = await douyin_scraper.scrape()
    if douyin_data:
        douyin_scraper.save_data(douyin_data)
        results['douyin_laike'] = douyin_data
    
    # 抓取美团点评数据
    meituan_scraper = MeituanDianpingScraper()
    meituan_data = await meituan_scraper.scrape()
    if meituan_data:
        meituan_scraper.save_data(meituan_data)
        results['meituan_dianping'] = meituan_data
    
    # 保存汇总报告
    summary = {
        'scraped_at': datetime.now().isoformat(),
        'total_platforms': len(results),
        'platforms': results
    }
    
    summary_file = DATA_DIR / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    # 生成CSV报告
    generate_csv_report(results)
    
    logger.info("=" * 60)
    logger.info(f"✅ 全量抓取完成！数据保存在: {DATA_DIR}")
    logger.info("=" * 60)
    
    return results

def generate_csv_report(results: Dict[str, Any]) -> None:
    """生成CSV格式报告"""
    import csv
    
    csv_file = DATA_DIR / f"report_{datetime.now().strftime('%Y%m%d')}.csv"
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['平台', '指标', '数值', '抓取时间'])
        
        for platform, data in results.items():
            for key, value in data.items():
                if key not in ['scraped_at', 'platform', 'shop_name']:
                    writer.writerow([
                        platform,
                        key,
                        value,
                        data.get('scraped_at', '')
                    ])
    
    logger.info(f"📊 CSV报告已生成: {csv_file}")

if __name__ == "__main__":
    asyncio.run(main())

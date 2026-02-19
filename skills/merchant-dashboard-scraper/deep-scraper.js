#!/usr/bin/env node
/**
 * 商家数据深度抓取系统 v2.0
 * 抖音来客 + 美团开店宝 - 全功能模块抓取
 * 
 * 深入抓取: 商品、流量、订单、评价、推广、客服等全维度数据
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
    cdpUrl: 'http://127.0.0.1:18800',
    dataDir: path.join(process.env.HOME, '.openclaw/workspace/data/merchant-dashboard'),
    screenshotDir: path.join(process.env.HOME, '.openclaw/workspace/data/merchant-dashboard/screenshots'),
    timeout: 30000,
    headless: false // 使用已打开的浏览器
};

// 确保目录存在
[CONFIG.dataDir, CONFIG.screenshotDir].forEach(dir => {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

// 日志工具
class Logger {
    static log(level, message, data = null) {
        const timestamp = new Date().toLocaleString('zh-CN');
        const logLine = `[${timestamp}] [${level}] ${message}`;
        console.log(logLine);
        if (data) console.log(JSON.stringify(data, null, 2));
        
        const logFile = path.join(CONFIG.dataDir, 'logs', `deep_scraper_${new Date().toISOString().split('T')[0]}.log`);
        fs.appendFileSync(logFile, logLine + (data ? '\n' + JSON.stringify(data) : '') + '\n');
    }
    static info(msg, data) { this.log('INFO', msg, data); }
    static error(msg, data) { this.log('ERROR', msg, data); }
    static warn(msg, data) { this.log('WARN', msg, data); }
    static success(msg, data) { this.log('SUCCESS', msg, data); }
}

// 抖音来客深度抓取器
class DouyinLaikeScraper {
    constructor(browser) {
        this.browser = browser;
        this.data = {
            platform: 'douyin_laike',
            shop_name: '有点方恐怖密室',
            scraped_at: new Date().toISOString(),
            overview: {},
            products: [],
            traffic: {},
            marketing: {},
            reviews: {},
            orders: [],
            violations: {},
            customer_service: {}
        };
    }

    async scrape() {
        Logger.info('🎯 开始深度抓取抖音来客数据...');
        
        try {
            // 获取已有页面
            const context = this.browser.contexts()[0];
            const pages = context.pages();
            
            // 查找抖音来客页面
            let douyinPage = pages.find(p => p.url().includes('life.douyin.com'));
            
            if (!douyinPage) {
                Logger.error('未找到抖音来客页面，请确保已登录');
                return null;
            }

            Logger.info(`找到抖音来客页面: ${await douyinPage.title()}`);

            // 1. 抓取首页概览数据
            await this.scrapeOverview(douyinPage);
            
            // 2. 抓取商品数据
            await this.scrapeProducts(douyinPage);
            
            // 3. 抓取流量数据
            await this.scrapeTraffic(douyinPage);
            
            // 4. 抓取营销数据
            await this.scrapeMarketing(douyinPage);
            
            // 5. 抓取评价数据
            await this.scrapeReviews(douyinPage);
            
            // 6. 抓取违规和客服数据
            await this.scrapeViolationsAndService(douyinPage);

            Logger.success('✅ 抖音来客深度抓取完成');
            return this.data;

        } catch (error) {
            Logger.error('抖音来客抓取失败', error.message);
            return null;
        }
    }

    async scrapeOverview(page) {
        Logger.info('📊 抓取首页概览数据...');
        
        try {
            // 等待页面加载完成
            await page.waitForLoadState('networkidle');
            await page.waitForTimeout(2000);

            // 提取概览数据
            const overview = await page.evaluate(() => {
                const data = {};
                
                // 尝试多种选择器获取数据
                const selectors = {
                    deal_amount: ['[class*="成交"] [class*="金额"]', '[class*="deal"] [class*="amount"]', '//text()[contains(.,"成交金额")]/following::*'],
                    deal_count: ['[class*="成交券数"]', '[class*="deal-count"]'],
                    visit_count: ['[class*="访问人数"]', '[class*="visitor"]'],
                    business_score: ['[class*="经营分"]', '[class*="score"]'],
                    account_balance: ['[class*="余额"]', '[class*="balance"]']
                };

                // 使用文本内容匹配
                document.querySelectorAll('*').forEach(el => {
                    const text = el.textContent || '';
                    
                    if (text.includes('成交金额') && text.includes('¥')) {
                        const match = text.match(/¥\s*([\d,.]+)/);
                        if (match) data.deal_amount = parseFloat(match[1].replace(/,/g, ''));
                    }
                    if (text.includes('成交券数')) {
                        const match = text.match(/(\d+)/);
                        if (match) data.deal_count = parseInt(match[1]);
                    }
                    if (text.includes('商品访问') || text.includes('访问人数')) {
                        const match = text.match(/(\d+)/);
                        if (match) data.visit_count = parseInt(match[1]);
                    }
                    if (text.includes('经营分')) {
                        const match = text.match(/(\d+)/);
                        if (match) data.business_score = parseInt(match[1]);
                    }
                    if (text.includes('账户') && text.includes('¥')) {
                        const match = text.match(/¥\s*([\d,.]+)/);
                        if (match) data.account_balance = parseFloat(match[1].replace(/,/g, ''));
                    }
                });

                return data;
            });

            this.data.overview = { ...this.data.overview, ...overview };
            Logger.success('首页概览数据抓取完成', overview);

        } catch (error) {
            Logger.warn('首页概览抓取失败', error.message);
        }
    }

    async scrapeProducts(page) {
        Logger.info('📦 抓取商品数据...');
        
        try {
            // 查找并点击"商品"或"商品管理"按钮
            const productLinks = await page.$$('a, button, [role="button"]');
            let productLink = null;
            
            for (const link of productLinks) {
                const text = await link.textContent();
                if (text && (text.includes('商品') || text.includes('套餐'))) {
                    productLink = link;
                    break;
                }
            }

            if (productLink) {
                await productLink.click();
                await page.waitForTimeout(3000);
                
                // 截图保存
                await page.screenshot({ 
                    path: path.join(CONFIG.screenshotDir, `douyin_products_${Date.now()}.png`),
                    fullPage: true 
                });

                // 提取商品列表数据
                const products = await page.evaluate(() => {
                    const items = [];
                    document.querySelectorAll('[class*="商品"], [class*="product"]').forEach(el => {
                        const text = el.textContent || '';
                        items.push({
                            text: text.substring(0, 200),
                            element: el.tagName
                        });
                    });
                    return items;
                });

                this.data.products = products;
                Logger.success(`抓取到 ${products.length} 个商品元素`);
            }

        } catch (error) {
            Logger.warn('商品数据抓取失败', error.message);
        }
    }

    async scrapeTraffic(page) {
        Logger.info('🌊 抓取流量数据...');
        
        try {
            // 查找数据中心/流量分析入口
            const dataLinks = await page.$$('a, button');
            let dataLink = null;
            
            for (const link of dataLinks) {
                const text = await link.textContent();
                if (text && (text.includes('数据') || text.includes('流量'))) {
                    dataLink = link;
                    break;
                }
            }

            if (dataLink) {
                await dataLink.click();
                await page.waitForTimeout(3000);
                
                await page.screenshot({ 
                    path: path.join(CONFIG.screenshotDir, `douyin_traffic_${Date.now()}.png`),
                    fullPage: true 
                });

                const traffic = await page.evaluate(() => {
                    const data = {};
                    document.querySelectorAll('*').forEach(el => {
                        const text = el.textContent || '';
                        if (text.includes('曝光')) {
                            const match = text.match(/(\d+)/);
                            if (match) data.exposure = parseInt(match[1]);
                        }
                        if (text.includes('点击')) {
                            const match = text.match(/(\d+)/);
                            if (match) data.clicks = parseInt(match[1]);
                        }
                    });
                    return data;
                });

                this.data.traffic = traffic;
                Logger.success('流量数据抓取完成', traffic);
            }

        } catch (error) {
            Logger.warn('流量数据抓取失败', error.message);
        }
    }

    async scrapeMarketing(page) {
        Logger.info('📢 抓取营销推广数据...');
        
        try {
            // 返回首页
            await page.goto('https://life.douyin.com/p/home');
            await page.waitForTimeout(3000);

            const marketing = await page.evaluate(() => {
                const data = {};
                document.querySelectorAll('*').forEach(el => {
                    const text = el.textContent || '';
                    if (text.includes('本地推')) {
                        data.has_local_promote = true;
                    }
                    if (text.includes('优惠券')) {
                        data.has_coupon = true;
                    }
                });
                return data;
            });

            this.data.marketing = marketing;
            Logger.success('营销数据抓取完成', marketing);

        } catch (error) {
            Logger.warn('营销数据抓取失败', error.message);
        }
    }

    async scrapeReviews(page) {
        Logger.info('⭐ 抓取评价数据...');
        
        try {
            const reviews = await page.evaluate(() => {
                const data = {
                    total_reviews: 0,
                    good_reviews: 0,
                    bad_reviews: 0,
                    keywords: []
                };

                document.querySelectorAll('*').forEach(el => {
                    const text = el.textContent || '';
                    
                    if (text.includes('评价') && text.match(/(\d+)/)) {
                        const match = text.match(/(\d+)/);
                        if (match) data.total_reviews = parseInt(match[1]);
                    }
                    if (text.includes('好评')) {
                        data.good_reviews++;
                    }
                    if (text.includes('差评')) {
                        data.bad_reviews++;
                    }
                });

                return data;
            });

            this.data.reviews = reviews;
            Logger.success('评价数据抓取完成', reviews);

        } catch (error) {
            Logger.warn('评价数据抓取失败', error.message);
        }
    }

    async scrapeViolationsAndService(page) {
        Logger.info('🚨 抓取违规和客服数据...');
        
        try {
            const info = await page.evaluate(() => {
                const data = {
                    violation_status: '正常',
                    violation_count: 0,
                    messages: 0,
                    consultations: 0
                };

                document.querySelectorAll('*').forEach(el => {
                    const text = el.textContent || '';
                    
                    if (text.includes('违规') && text.includes('生效')) {
                        data.violation_status = '违规生效中';
                    }
                    if (text.includes('消息')) {
                        const match = text.match(/(\d+)/);
                        if (match) data.messages = parseInt(match[1]);
                    }
                    if (text.includes('咨询')) {
                        const match = text.match(/(\d+)/);
                        if (match) data.consultations = parseInt(match[1]);
                    }
                });

                return data;
            });

            this.data.violations = { status: info.violation_status, count: info.violation_count };
            this.data.customer_service = { messages: info.messages, consultations: info.consultations };
            
            Logger.success('违规和客服数据抓取完成', info);

        } catch (error) {
            Logger.warn('违规和客服数据抓取失败', error.message);
        }
    }
}

// 美团开店宝深度抓取器
class MeituanDianpingScraper {
    constructor(browser) {
        this.browser = browser;
        this.data = {
            platform: 'meituan_dianping',
            shop_name: '有點方真人恐怖密室(解放西路店)',
            scraped_at: new Date().toISOString(),
            overview: {},
            traffic: {},
            transactions: {},
            reviews: {},
            marketing: {},
            competition: {}
        };
    }

    async scrape() {
        Logger.info('🎯 开始深度抓取美团开店宝数据...');
        
        try {
            const context = this.browser.contexts()[0];
            const pages = context.pages();
            
            let meituanPage = pages.find(p => p.url().includes('dianping.com') || p.url().includes('meituan.com'));
            
            if (!meituanPage) {
                Logger.error('未找到美团开店宝页面，请确保已登录');
                return null;
            }

            Logger.info(`找到美团页面: ${await meituanPage.title()}`);

            await this.scrapeOverview(meituanPage);
            await this.scrapeTraffic(meituanPage);
            await this.scrapeTransactions(meituanPage);
            await this.scrapeReviews(meituanPage);
            await this.scrapeMarketing(meituanPage);

            Logger.success('✅ 美团开店宝深度抓取完成');
            return this.data;

        } catch (error) {
            Logger.error('美团开店宝抓取失败', error.message);
            return null;
        }
    }

    async scrapeOverview(page) {
        Logger.info('📊 抓取美团概览数据...');
        
        try {
            await page.waitForTimeout(2000);

            const overview = await page.evaluate(() => {
                const data = {};
                
                document.querySelectorAll('*').forEach(el => {
                    const text = el.textContent || '';
                    
                    if (text.includes('访问人数')) {
                        const match = text.match(/(\d+)/);
                        if (match) data.visit_count = parseInt(match[1]);
                    }
                    if (text.includes('经营评分') || text.includes('评分')) {
                        const match = text.match(/(\d+\.?\d*)/);
                        if (match) data.business_score = parseFloat(match[1]);
                    }
                    if (text.includes('曝光')) {
                        const match = text.match(/(\d+)/);
                        if (match) data.exposure = parseInt(match[1]);
                    }
                });

                return data;
            });

            this.data.overview = overview;
            Logger.success('美团概览数据抓取完成', overview);

        } catch (error) {
            Logger.warn('美团概览抓取失败', error.message);
        }
    }

    async scrapeTraffic(page) {
        Logger.info('🌊 抓取美团流量数据...');
        
        try {
            await page.screenshot({ 
                path: path.join(CONFIG.screenshotDir, `meituan_overview_${Date.now()}.png`),
                fullPage: true 
            });

            const traffic = await page.evaluate(() => {
                const data = {
                    exposure: 0,
                    visits: 0,
                    click_rate: 0
                };

                document.querySelectorAll('*').forEach(el => {
                    const text = el.textContent || '';
                    if (text.includes('曝光')) data.exposure++;
                    if (text.includes('访问')) data.visits++;
                });

                return data;
            });

            this.data.traffic = traffic;
            Logger.success('美团流量数据抓取完成', traffic);

        } catch (error) {
            Logger.warn('美团流量抓取失败', error.message);
        }
    }

    async scrapeTransactions(page) {
        Logger.info('💰 抓取美团交易数据...');
        
        try {
            const transactions = await page.evaluate(() => {
                const data = {
                    order_amount: 0,
                    verify_amount: 0,
                    order_count: 0
                };

                document.querySelectorAll('*').forEach(el => {
                    const text = el.textContent || '';
                    
                    if (text.includes('下单金额') || text.includes('交易额')) {
                        const match = text.match(/(\d+)/);
                        if (match) data.order_amount = parseInt(match[1]);
                    }
                    if (text.includes('核销金额')) {
                        const match = text.match(/(\d+)/);
                        if (match) data.verify_amount = parseInt(match[1]);
                    }
                });

                return data;
            });

            this.data.transactions = transactions;
            Logger.success('美团交易数据抓取完成', transactions);

        } catch (error) {
            Logger.warn('美团交易抓取失败', error.message);
        }
    }

    async scrapeReviews(page) {
        Logger.info('⭐ 抓取美团评价数据...');
        
        try {
            const reviews = await page.evaluate(() => {
                const data = {
                    total_reviews: 0,
                    new_reviews: 0,
                    new_bad_reviews: 0,
                    score: 0
                };

                document.querySelectorAll('*').forEach(el => {
                    const text = el.textContent || '';
                    
                    if (text.includes('新增评论')) {
                        const match = text.match(/(\d+)/);
                        if (match) data.new_reviews = parseInt(match[1]);
                    }
                    if (text.includes('新增差评')) {
                        const match = text.match(/(\d+)/);
                        if (match) data.new_bad_reviews = parseInt(match[1]);
                    }
                    if (text.includes('评分')) {
                        const match = text.match(/(\d+\.?\d*)/);
                        if (match) data.score = parseFloat(match[1]);
                    }
                });

                return data;
            });

            this.data.reviews = reviews;
            Logger.success('美团评价数据抓取完成', reviews);

        } catch (error) {
            Logger.warn('美团评价抓取失败', error.message);
        }
    }

    async scrapeMarketing(page) {
        Logger.info('📢 抓取美团推广数据...');
        
        try {
            const marketing = await page.evaluate(() => {
                const data = {
                    has_promotion: false,
                    promotion_spend: 0
                };

                document.querySelectorAll('*').forEach(el => {
                    const text = el.textContent || '';
                    if (text.includes('推广') || text.includes('推广通')) {
                        data.has_promotion = true;
                    }
                });

                return data;
            });

            this.data.marketing = marketing;
            Logger.success('美团推广数据抓取完成', marketing);

        } catch (error) {
            Logger.warn('美团推广抓取失败', error.message);
        }
    }
}

// 智能分析引擎
class AnalysisEngine {
    static analyze(douyinData, meituanData) {
        Logger.info('🧠 启动智能分析引擎...');
        
        const analysis = {
            timestamp: new Date().toISOString(),
            alerts: [],
            opportunities: [],
            actions: []
        };

        // 抖音分析
        if (douyinData) {
            // 违规检测
            if (douyinData.violations?.status === '违规生效中') {
                analysis.alerts.push({
                    level: 'P0',
                    platform: '抖音来客',
                    issue: '存在违规处罚生效中',
                    impact: '可能影响流量和曝光',
                    action: '立即查看违规详情并整改'
                });
            }

            // 账户余额检测
            if (douyinData.overview?.account_balance < 500) {
                analysis.alerts.push({
                    level: 'P1',
                    platform: '抖音来客',
                    issue: '账户余额偏低',
                    value: `¥${douyinData.overview.account_balance}`,
                    action: '考虑充值或调整结算设置'
                });
            }

            // 转化率分析
            if (douyinData.overview?.visit_count > 0 && douyinData.overview?.deal_count === 0) {
                analysis.alerts.push({
                    level: 'P1',
                    platform: '抖音来客',
                    issue: '有流量无转化',
                    value: `${douyinData.overview.visit_count}访问，0成交`,
                    action: '优化商品详情页，调整价格或套餐设置'
                });
            }
        }

        // 美团分析
        if (meituanData) {
            // 评分检测
            if (meituanData.overview?.business_score < 60) {
                analysis.alerts.push({
                    level: 'P0',
                    platform: '美团点评',
                    issue: '经营评分偏低',
                    value: `${meituanData.overview.business_score}分`,
                    benchmark: '商圈均值约65分',
                    action: '主动邀请好评，及时回复差评，提升服务质量'
                });
            }

            // 流量检测
            if (meituanData.overview?.visit_count < 50) {
                analysis.opportunities.push({
                    platform: '美团点评',
                    type: '流量增长',
                    current: `${meituanData.overview.visit_count}人/日`,
                    potential: '100-150人/日',
                    action: '开启推广通投放，优化店铺关键词'
                });
            }
        }

        // 生成行动建议
        analysis.actions = this.generateActionPlan(analysis.alerts, analysis.opportunities);

        Logger.success('智能分析完成', {
            alerts: analysis.alerts.length,
            opportunities: analysis.opportunities.length,
            actions: analysis.actions.length
        });

        return analysis;
    }

    static generateActionPlan(alerts, opportunities) {
        const actions = [];

        // 按优先级排序
        const sortedAlerts = alerts.sort((a, b) => {
            const priority = { 'P0': 0, 'P1': 1, 'P2': 2 };
            return priority[a.level] - priority[b.level];
        });

        sortedAlerts.forEach(alert => {
            actions.push({
                priority: alert.level,
                title: `[${alert.platform}] ${alert.issue}`,
                description: alert.action,
                deadline: alert.level === 'P0' ? '24小时内' : '本周内'
            });
        });

        opportunities.forEach(opp => {
            actions.push({
                priority: 'P2',
                title: `[${opp.platform}] ${opp.type}机会`,
                description: opp.action,
                expected_impact: `从${opp.current}提升至${opp.potential}`,
                deadline: '本周内'
            });
        });

        return actions;
    }
}

// 报告生成器
class ReportGenerator {
    static generate(douyinData, meituanData, analysis) {
        const timestamp = new Date().toISOString();
        const report = {
            generated_at: timestamp,
            douyin_laike: douyinData,
            meituan_dianping: meituanData,
            analysis: analysis
        };

        // 保存JSON报告
        const reportFile = path.join(CONFIG.dataDir, `deep_report_${new Date().toISOString().split('T')[0]}.json`);
        fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));

        // 生成Markdown报告
        this.generateMarkdownReport(douyinData, meituanData, analysis);

        Logger.success('报告生成完成', { file: reportFile });
        return report;
    }

    static generateMarkdownReport(douyin, meituan, analysis) {
        const timestamp = new Date().toLocaleString('zh-CN');
        
        let md = `# 商家深度运营分析报告\n\n`;
        md += `**生成时间**: ${timestamp}\n\n`;
        md += `---\n\n`;

        // 告警摘要
        if (analysis.alerts.length > 0) {
            md += `## 🚨 重要告警 (${analysis.alerts.length}项)\n\n`;
            analysis.alerts.forEach(alert => {
                const emoji = alert.level === 'P0' ? '🔴' : alert.level === 'P1' ? '🟡' : '💡';
                md += `${emoji} **[${alert.level}] ${alert.platform}**\n`;
                md += `- **问题**: ${alert.issue}\n`;
                if (alert.value) md += `- **当前值**: ${alert.value}\n`;
                if (alert.benchmark) md += `- **参考值**: ${alert.benchmark}\n`;
                md += `- **建议**: ${alert.action}\n\n`;
            });
            md += `---\n\n`;
        }

        // 抖音数据
        if (douyin) {
            md += `## 📱 抖音来客数据\n\n`;
            md += `**店铺**: ${douyin.shop_name}\n\n`;
            if (douyin.overview) {
                md += `| 指标 | 数值 |\n`;
                md += `|------|------|\n`;
                Object.entries(douyin.overview).forEach(([k, v]) => {
                    md += `| ${k} | ${v} |\n`;
                });
            }
            md += `\n`;
        }

        // 美团数据
        if (meituan) {
            md += `## 🍜 美团点评数据\n\n`;
            md += `**店铺**: ${meituan.shop_name}\n\n`;
            if (meituan.overview) {
                md += `| 指标 | 数值 |\n`;
                md += `|------|------|\n`;
                Object.entries(meituan.overview).forEach(([k, v]) => {
                    md += `| ${k} | ${v} |\n`;
                });
            }
            md += `\n`;
        }

        // 行动计划
        if (analysis.actions.length > 0) {
            md += `## 📋 行动计划\n\n`;
            md += `| 优先级 | 任务 | 描述 | 截止日期 |\n`;
            md += `|--------|------|------|----------|\n`;
            analysis.actions.forEach(action => {
                md += `| ${action.priority} | ${action.title} | ${action.description} | ${action.deadline} |\n`;
            });
            md += `\n`;
        }

        const mdFile = path.join(CONFIG.dataDir, `analysis_report_${new Date().toISOString().split('T')[0]}.md`);
        fs.writeFileSync(mdFile, md);
        
        return mdFile;
    }
}

// 主函数
async function main() {
    Logger.info('='.repeat(60));
    Logger.info('🚀 商家数据深度抓取系统 v2.0 启动');
    Logger.info('='.repeat(60));

    let browser = null;
    let douyinData = null;
    let meituanData = null;

    try {
        // 连接到已打开的浏览器
        Logger.info(`连接到浏览器: ${CONFIG.cdpUrl}`);
        browser = await chromium.connectOverCDP(CONFIG.cdpUrl);
        Logger.success('浏览器连接成功');

        // 抓取抖音来客
        const douyinScraper = new DouyinLaikeScraper(browser);
        douyinData = await douyinScraper.scrape();

        // 抓取美团开店宝
        const meituanScraper = new MeituanDianpingScraper(browser);
        meituanData = await meituanScraper.scrape();

        // 智能分析
        const analysis = AnalysisEngine.analyze(douyinData, meituanData);

        // 生成报告
        const report = ReportGenerator.generate(douyinData, meituanData, analysis);

        // 保存数据
        if (douyinData) {
            fs.writeFileSync(
                path.join(CONFIG.dataDir, 'douyin_laike_deep.json'),
                JSON.stringify(douyinData, null, 2)
            );
        }
        if (meituanData) {
            fs.writeFileSync(
                path.join(CONFIG.dataDir, 'meituan_dianping_deep.json'),
                JSON.stringify(meituanData, null, 2)
            );
        }

        Logger.info('='.repeat(60));
        Logger.success('✅ 深度抓取任务全部完成');
        Logger.info('='.repeat(60));

        // 输出摘要
        console.log('\n📊 深度数据摘要:\n');
        if (douyinData) {
            console.log('抖音来客:');
            console.log(`  💰 成交金额: ¥${douyinData.overview?.deal_amount || 'N/A'}`);
            console.log(`  🎫 成交券数: ${douyinData.overview?.deal_count || 'N/A'}`);
            console.log(`  👥 访问人数: ${douyinData.overview?.visit_count || 'N/A'}`);
            console.log(`  📦 商品数量: ${douyinData.products?.length || 'N/A'}`);
            console.log(`  🚨 违规状态: ${douyinData.violations?.status || 'N/A'}`);
        }
        
        if (meituanData) {
            console.log('\n美团点评:');
            console.log(`  👁️ 访问人数: ${meituanData.overview?.visit_count || 'N/A'}`);
            console.log(`  ⭐ 经营评分: ${meituanData.overview?.business_score || 'N/A'}`);
            console.log(`  💬 新评论: ${meituanData.reviews?.new_reviews || 'N/A'}`);
        }

        console.log('\n🚨 分析结果:');
        console.log(`  告警: ${analysis.alerts.length}项`);
        console.log(`  机会: ${analysis.opportunities.length}项`);
        console.log(`  行动建议: ${analysis.actions.length}项`);

        return report;

    } catch (error) {
        Logger.error('程序异常', error.message);
        console.error(error);
        process.exit(1);
    } finally {
        if (browser) {
            // 不关闭浏览器，保持已打开的页面
            Logger.info('保持浏览器连接（不关闭）');
        }
    }
}

// 运行
main();

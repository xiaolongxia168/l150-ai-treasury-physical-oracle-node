#!/usr/bin/env node
/**
 * 商家数据自动化抓取系统
 * 抖音来客 + 美团开店宝
 * 
 * 使用方法: node scraper.js [douyin|meituan|all]
 */

const fs = require('fs');
const path = require('path');

// 数据存储路径
const DATA_DIR = path.join(process.env.HOME, '.openclaw/workspace/data/merchant-dashboard');
const LOGS_DIR = path.join(DATA_DIR, 'logs');

// 确保目录存在
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
if (!fs.existsSync(LOGS_DIR)) fs.mkdirSync(LOGS_DIR, { recursive: true });

// 日志函数
function log(level, message) {
    const timestamp = new Date().toISOString();
    const logLine = `[${timestamp}] [${level}] ${message}`;
    console.log(logLine);
    
    // 写入日志文件
    const logFile = path.join(LOGS_DIR, `scraper_${new Date().toISOString().split('T')[0]}.log`);
    fs.appendFileSync(logFile, logLine + '\n');
}

// 通过CDP获取页面数据
async function scrapeViaCDP(targetUrl, selectors) {
    try {
        // 使用系统curl命令获取CDP数据
        const { execSync } = require('child_process');
        
        // 首先获取可用页面列表
        const pagesJson = execSync('curl -s http://127.0.0.1:18800/json/list').toString();
        const pages = JSON.parse(pagesJson);
        
        // 查找目标页面
        const targetPage = pages.find(p => p.url.includes(targetUrl));
        if (!targetPage) {
            throw new Error(`未找到目标页面: ${targetUrl}`);
        }
        
        log('INFO', `找到目标页面: ${targetPage.title}`);
        
        // 连接到页面并执行JavaScript
        const wsUrl = targetPage.webSocketDebuggerUrl;
        
        // 使用简单的HTTP请求方式获取页面HTML
        const html = execSync(`curl -s "${targetPage.url}"`).toString();
        
        // 解析数据
        const data = {};
        
        // 使用正则表达式提取数据
        for (const [key, pattern] of Object.entries(selectors)) {
            const match = html.match(pattern);
            if (match) {
                data[key] = match[1];
            }
        }
        
        return data;
        
    } catch (error) {
        log('ERROR', `抓取失败: ${error.message}`);
        return null;
    }
}

// 抖音来客抓取
async function scrapeDouyin() {
    log('INFO', '🎯 开始抓取抖音来客数据...');
    
    const selectors = {
        deal_amount: /成交金额[\s\S]*?¥\s*([\d,.]+)/,
        deal_count: /成交券数[\s\S]*?(\d+)/,
        verify_amount: /核销金额[\s\S]*?¥\s*([\d,.]+)/,
        refund_amount: /退款金额[\s\S]*?¥\s*([\d,.]+)/,
        visit_count: /商品访问人数[\s\S]*?(\d+)/,
        business_score: /经营分[\s\S]*?(\d+)/,
        account_balance: /账户总余额[\s\S]*?¥\s*([\d,.]+)/
    };
    
    const data = await scrapeViaCDP('life.douyin.com', selectors);
    
    if (data) {
        data.platform = 'douyin_laike';
        data.shop_name = '有点方恐怖密室';
        data.scraped_at = new Date().toISOString();
        
        // 保存数据
        saveData('douyin_laike', data);
        log('INFO', '✅ 抖音来客数据抓取完成');
    }
    
    return data;
}

// 美团点评抓取
async function scrapeMeituan() {
    log('INFO', '🎯 开始抓取美团点评数据...');
    
    const selectors = {
        visit_count: /访问人数[\s\S]*?(\d+)/,
        order_amount: /下单金额[\s\S]*?(\d+)/,
        verify_amount: /核销金额[\s\S]*?(\d+)/,
        business_score: /当前评分[\s\S]*?(\d+\.?\d*)/,
        new_comments: /新增评论数[\s\S]*?(\d+)个/,
        new_bad_comments: /新增差评数[\s\S]*?(\d+)个/
    };
    
    const data = await scrapeViaCDP('dianping.com', selectors);
    
    if (data) {
        data.platform = 'meituan_dianping';
        data.shop_name = '有點方真人恐怖密室(解放西路店)';
        data.scraped_at = new Date().toISOString();
        
        // 保存数据
        saveData('meituan_dianping', data);
        log('INFO', '✅ 美团点评数据抓取完成');
    }
    
    return data;
}

// 保存数据
function saveData(platform, data) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    
    // 保存最新数据
    const latestFile = path.join(DATA_DIR, `${platform}_latest.json`);
    fs.writeFileSync(latestFile, JSON.stringify(data, null, 2));
    
    // 保存历史数据
    const dailyFile = path.join(DATA_DIR, `${platform}_${new Date().toISOString().split('T')[0]}.json`);
    let history = [];
    if (fs.existsSync(dailyFile)) {
        history = JSON.parse(fs.readFileSync(dailyFile, 'utf8'));
    }
    history.push(data);
    fs.writeFileSync(dailyFile, JSON.stringify(history, null, 2));
    
    log('INFO', `💾 数据已保存: ${latestFile}`);
}

// 生成报告
function generateReport(douyinData, meituanData) {
    const report = {
        generated_at: new Date().toISOString(),
        platforms: {
            douyin_laike: douyinData,
            meituan_dianping: meituanData
        }
    };
    
    const reportFile = path.join(DATA_DIR, `report_${new Date().toISOString().split('T')[0]}.json`);
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
    
    // 生成CSV
    generateCSV(douyinData, meituanData);
    
    return report;
}

// 生成CSV
function generateCSV(douyinData, meituanData) {
    const csvFile = path.join(DATA_DIR, `report_${new Date().toISOString().split('T')[0]}.csv`);
    
    let csv = '平台,指标,数值\n';
    
    if (douyinData) {
        Object.entries(douyinData).forEach(([key, value]) => {
            if (!['platform', 'shop_name', 'scraped_at'].includes(key)) {
                csv += `抖音来客,${key},${value}\n`;
            }
        });
    }
    
    if (meituanData) {
        Object.entries(meituanData).forEach(([key, value]) => {
            if (!['platform', 'shop_name', 'scraped_at'].includes(key)) {
                csv += `美团点评,${key},${value}\n`;
            }
        });
    }
    
    fs.writeFileSync(csvFile, csv);
    log('INFO', `📊 CSV报告已生成: ${csvFile}`);
}

// 主函数
async function main() {
    const args = process.argv.slice(2);
    const target = args[0] || 'all';
    
    log('INFO', '='.repeat(60));
    log('INFO', '🚀 商家数据全自动化抓取系统启动');
    log('INFO', '='.repeat(60));
    
    let douyinData = null;
    let meituanData = null;
    
    if (target === 'all' || target === 'douyin') {
        douyinData = await scrapeDouyin();
    }
    
    if (target === 'all' || target === 'meituan') {
        meituanData = await scrapeMeituan();
    }
    
    // 生成报告
    const report = generateReport(douyinData, meituanData);
    
    log('INFO', '='.repeat(60));
    log('INFO', '✅ 抓取任务完成');
    log('INFO', `📁 数据目录: ${DATA_DIR}`);
    log('INFO', '='.repeat(60));
    
    // 输出摘要
    console.log('\n📊 数据摘要:');
    if (douyinData) {
        console.log('\n抖音来客:');
        console.log(`  💰 成交金额: ¥${douyinData.deal_amount || 'N/A'}`);
        console.log(`  🎫 成交券数: ${douyinData.deal_count || 'N/A'}`);
        console.log(`  👥 访问人数: ${douyinData.visit_count || 'N/A'}`);
        console.log(`  💳 账户余额: ¥${douyinData.account_balance || 'N/A'}`);
    }
    
    if (meituanData) {
        console.log('\n美团点评:');
        console.log(`  👁️ 访问人数: ${meituanData.visit_count || 'N/A'}`);
        console.log(`  ⭐ 经营评分: ${meituanData.business_score || 'N/A'}`);
        console.log(`  💬 新评论: ${meituanData.new_comments || 'N/A'}`);
        console.log(`  👎 新差评: ${meituanData.new_bad_comments || 'N/A'}`);
    }
    
    return report;
}

main().catch(error => {
    log('ERROR', `程序异常: ${error.message}`);
    process.exit(1);
});

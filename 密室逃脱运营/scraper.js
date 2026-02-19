const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');

// 配置
const CONFIG = {
    douyin: {
        loginUrl: 'https://e.douyin.com/',
        dataUrl: 'https://e.douyin.com/aweme/v2/data/dashboard/',
    },
    meituan: {
        loginUrl: 'https://e.meituan.com/',
    },
    outputDir: '/Users/xiaolongxia/.openclaw/workspace/密室逃脱运营/数据'
};

/**
 * 抖音来客数据抓取
 */
async function fetchDouyinData() {
    console.log('🎵 开始抓取抖音来客数据...');
    
    const browser = await puppeteer.launch({
        headless: false,  // 首次登录需要可视化
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        
        // 设置视口
        await page.setViewport({ width: 1920, height: 1080 });
        
        // 访问抖音来客
        console.log('正在打开抖音来客...');
        await page.goto(CONFIG.douyin.loginUrl, { waitUntil: 'networkidle2', timeout: 60000 });
        
        // 等待用户登录（或检查是否已登录）
        console.log('请确保已登录抖音来客...');
        
        // 等待登录完成 - 检查是否有数据看板元素
        await page.waitForSelector('.dashboard-container, .data-overview, .content-data', { 
            timeout: 120000 
        }).catch(() => {
            console.log('⚠️ 等待超时，请手动登录后继续...');
        });
        
        // 抓取数据
        const data = await page.evaluate(() => {
            const result = {
                timestamp: new Date().toISOString(),
                videoData: {},
                conversionData: {},
                fanData: {}
            };
            
            // 尝试提取视频数据
            const videoElements = document.querySelectorAll('.video-data-item, .data-item');
            videoElements.forEach(el => {
                const label = el.querySelector('.label, .data-label')?.textContent?.trim();
                const value = el.querySelector('.value, .data-value')?.textContent?.trim();
                if (label && value) {
                    result.videoData[label] = value;
                }
            });
            
            return result;
        });
        
        // 保存数据
        const outputFile = path.join(CONFIG.outputDir, `douyin_auto_${Date.now()}.json`);
        await fs.mkdir(CONFIG.outputDir, { recursive: true });
        await fs.writeFile(outputFile, JSON.stringify(data, null, 2));
        
        console.log('✅ 抖音数据已保存:', outputFile);
        return data;
        
    } catch (error) {
        console.error('❌ 抖音数据抓取失败:', error.message);
        throw error;
    } finally {
        await browser.close();
    }
}

/**
 * 美团开店宝数据抓取
 */
async function fetchMeituanData() {
    console.log('🦘 开始抓取美团开店宝数据...');
    
    const browser = await puppeteer.launch({
        headless: false,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1920, height: 1080 });
        
        console.log('正在打开美团开店宝...');
        await page.goto(CONFIG.meituan.loginUrl, { waitUntil: 'networkidle2', timeout: 60000 });
        
        console.log('请确保已登录美团开店宝...');
        
        // 等待数据看板加载
        await page.waitForSelector('.dashboard, .data-panel, .shop-data', { 
            timeout: 120000 
        }).catch(() => {
            console.log('⚠️ 等待超时，请手动登录后继续...');
        });
        
        // 抓取数据
        const data = await page.evaluate(() => {
            const result = {
                timestamp: new Date().toISOString(),
                trafficData: {},
                orderData: {},
                ratingData: {}
            };
            
            // 提取流量数据
            const trafficElements = document.querySelectorAll('.traffic-item, .flow-item');
            trafficElements.forEach(el => {
                const label = el.querySelector('.label')?.textContent?.trim();
                const value = el.querySelector('.value')?.textContent?.trim();
                if (label && value) {
                    result.trafficData[label] = value;
                }
            });
            
            return result;
        });
        
        // 保存数据
        const outputFile = path.join(CONFIG.outputDir, `meituan_auto_${Date.now()}.json`);
        await fs.writeFile(outputFile, JSON.stringify(data, null, 2));
        
        console.log('✅ 美团数据已保存:', outputFile);
        return data;
        
    } catch (error) {
        console.error('❌ 美团数据抓取失败:', error.message);
        throw error;
    } finally {
        await browser.close();
    }
}

/**
 * 竞品数据抓取
 */
async function fetchCompetitorData(competitorName, platform) {
    console.log(`🔍 开始抓取竞品数据: ${competitorName} @ ${platform}...`);
    
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1920, height: 1080 });
        
        let url;
        if (platform === 'douyin') {
            // 抖音搜索URL
            url = `https://www.douyin.com/search/${encodeURIComponent(competitorName)}`;
        } else if (platform === 'meituan') {
            // 美团搜索URL
            url = `https://www.meituan.com/search/${encodeURIComponent(competitorName)}`;
        } else {
            throw new Error('不支持的平台: ' + platform);
        }
        
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
        
        // 等待内容加载
        await page.waitForTimeout(3000);
        
        // 抓取公开数据
        const data = await page.evaluate(() => {
            const result = {
                timestamp: new Date().toISOString(),
                videos: [],
                stats: {}
            };
            
            // 提取视频数据（抖音）
            const videoElements = document.querySelectorAll('[data-e2e="search-card-video"]');
            videoElements.forEach((el, index) => {
                if (index < 10) {  // 只取前10条
                    const title = el.querySelector('.title, .desc')?.textContent?.trim();
                    const likes = el.querySelector('.like-count, .thumb-count')?.textContent?.trim();
                    if (title) {
                        result.videos.push({ title, likes: likes || '0' });
                    }
                }
            });
            
            return result;
        });
        
        // 保存数据
        const competitorDir = path.join(CONFIG.outputDir, '竞品');
        await fs.mkdir(competitorDir, { recursive: true });
        
        const outputFile = path.join(competitorDir, `${competitorName}_${platform}_${Date.now()}.json`);
        await fs.writeFile(outputFile, JSON.stringify(data, null, 2));
        
        console.log('✅ 竞品数据已保存:', outputFile);
        return data;
        
    } catch (error) {
        console.error(`❌ 竞品数据抓取失败 (${competitorName}):`, error.message);
        throw error;
    } finally {
        await browser.close();
    }
}

// 命令行入口
async function main() {
    const args = process.argv.slice(2);
    const command = args[0];
    
    switch (command) {
        case 'douyin':
            await fetchDouyinData();
            break;
            
        case 'meituan':
            await fetchMeituanData();
            break;
            
        case 'competitor':
            const name = args[1];
            const platform = args[2] || 'douyin';
            if (!name) {
                console.error('请提供竞品名称: node scraper.js competitor <名称> [平台]');
                process.exit(1);
            }
            await fetchCompetitorData(name, platform);
            break;
            
        default:
            console.log(`
密室逃脱数据抓取工具

用法:
  node scraper.js <command> [options]

命令:
  douyin                  抓取抖音来客数据
  meituan                 抓取美团开店宝数据
  competitor <名称> [平台] 抓取竞品数据 (平台: douyin/meituan)

示例:
  node scraper.js douyin
  node scraper.js meituan
  node scraper.js competitor "XXX密室逃脱" douyin
            `);
    }
}

main().catch(console.error);

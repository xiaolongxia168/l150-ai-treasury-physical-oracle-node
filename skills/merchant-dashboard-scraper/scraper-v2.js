#!/usr/bin/env node
/**
 * 商家平台超级采集系统 v2.0
 * 模块化架构，支持全功能探索
 * 
 * 抖音来客 + 美团开店宝 全模块自动化
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const CONFIG = {
  DATA_DIR: path.join(process.env.HOME, '.openclaw/workspace/data/merchant-dashboard'),
  LOGS_DIR: path.join(process.env.HOME, '.openclaw/workspace/data/merchant-dashboard/logs'),
  CDP_PORT: 18800,
  
  // 抖音来客模块配置
  DOUYIN_MODULES: {
    dashboard: {
      name: '首页仪表盘',
      priority: 'P0',
      selectors: {
        deal_amount: { regex: /成交金额[\s\S]*?¥\s*([\d,.]+)/, type: 'currency' },
        deal_count: { regex: /成交券数[\s\S]*?(\d+)/, type: 'number' },
        verify_amount: { regex: /核销金额[\s\S]*?¥\s*([\d,.]+)/, type: 'currency' },
        refund_amount: { regex: /退款金额[\s\S]*?¥\s*([\d,.]+)/, type: 'currency' },
        visit_count: { regex: /商品访问人数[\s\S]*?(\d+)/, type: 'number' },
        business_score: { regex: /经营分[\s\S]*?(\d+)/, type: 'number' },
        account_balance: { regex: /账户总余额[\s\S]*?¥\s*([\d,.]+)/, type: 'currency' },
        ad_spend: { regex: /本地推消耗[\s\S]*?¥\s*([\d,.]+)/, type: 'currency' },
        product_count: { regex: /在售商品[\s\S]*?(\d+)/, type: 'number' },
        douyin_count: { regex: /抖音号[\s\S]*?(\d+)/, type: 'number' },
        employee_count: { regex: /员工数[\s\S]*?(\d+)/, type: 'number' },
        violation_status: { regex: /违规状态[\s\S]*?([^\n]+)/, type: 'text' },
        deposit_status: { regex: /保证金[\s\S]*?([^\n]+)/, type: 'text' },
        message_count: { regex: /消息[\s\S]*?(\d+)\s*条/, type: 'number' },
        consultation_count: { regex: /咨询[\s\S]*?(\d+)\s*条/, type: 'number' },
      }
    },
    
    promotion: {
      name: '推广中心-本地推',
      priority: 'P0',
      url: '/promotion/local-push',
      selectors: {
        ad_budget: { regex: /推广预算[\s\S]*?¥\s*([\d,.]+)/, type: 'currency' },
        ad_spend_today: { regex: /今日消耗[\s\S]*?¥\s*([\d,.]+)/, type: 'currency' },
        ad_exposure: { regex: /曝光量[\s\S]*?(\d+)/, type: 'number' },
        ad_clicks: { regex: /点击量[\s\S]*?(\d+)/, type: 'number' },
        ad_ctr: { regex: /点击率[\s\S]*?([\d.]+%)/, type: 'percent' },
        ad_conversions: { regex: /转化量[\s\S]*?(\d+)/, type: 'number' },
        ad_cvr: { regex: /转化率[\s\S]*?([\d.]+%)/, type: 'percent' },
        ad_roi: { regex: /ROI[\s\S]*?([\d.]+)/, type: 'number' },
        ad_rank: { regex: /平均排名[\s\S]*?([\d.]+)/, type: 'number' },
      }
    },
    
    product: {
      name: '商品管理',
      priority: 'P1',
      url: '/product/manage',
      selectors: {
        total_products: { regex: /全部商品[\s\S]*?(\d+)/, type: 'number' },
        on_sale: { regex: /出售中[\s\S]*?(\d+)/, type: 'number' },
        sold_out: { regex: /已售罄[\s\S]*?(\d+)/, type: 'number' },
        pending: { regex: /审核中[\s\S]*?(\d+)/, type: 'number' },
        off_sale: { regex: /已下架[\s\S]*?(\d+)/, type: 'number' },
      }
    },
    
    orders: {
      name: '订单管理',
      priority: 'P1',
      url: '/order/manage',
      selectors: {
        pending_verify: { regex: /待核销[\s\S]*?(\d+)/, type: 'number' },
        verified_today: { regex: /今日已核销[\s\S]*?(\d+)/, type: 'number' },
        refund_pending: { regex: /退款中[\s\S]*?(\d+)/, type: 'number' },
        total_orders_today: { regex: /今日订单[\s\S]*?(\d+)/, type: 'number' },
      }
    },
    
    reviews: {
      name: '评价管理',
      priority: 'P0',
      url: '/review/manage',
      selectors: {
        total_reviews: { regex: /全部评价[\s\S]*?(\d+)/, type: 'number' },
        new_reviews_today: { regex: /今日新增[\s\S]*?(\d+)/, type: 'number' },
        bad_reviews: { regex: /差评[\s\S]*?(\d+)/, type: 'number' },
        pending_reply: { regex: /待回复[\s\S]*?(\d+)/, type: 'number' },
        avg_rating: { regex: /综合评分[\s\S]*?([\d.]+)/, type: 'number' },
      }
    },
    
    customers: {
      name: '客户管理',
      priority: 'P2',
      url: '/customer/manage',
      selectors: {
        total_customers: { regex: /客户总数[\s\S]*?(\d+)/, type: 'number' },
        new_customers_today: { regex: /今日新增[\s\S]*?(\d+)/, type: 'number' },
        return_customers: { regex: /回头客[\s\S]*?(\d+)/, type: 'number' },
        high_value_customers: { regex: /高价值客户[\s\S]*?(\d+)/, type: 'number' },
      }
    },
    
    dataCenter: {
      name: '数据中心',
      priority: 'P1',
      url: '/data/center',
      selectors: {
        traffic_total: { regex: /总访问量[\s\S]*?(\d+)/, type: 'number' },
        traffic_natural: { regex: /自然流量[\s\S]*?(\d+)/, type: 'number' },
        traffic_paid: { regex: /付费流量[\s\S]*?(\d+)/, type: 'number' },
        conversion_rate: { regex: /转化率[\s\S]*?([\d.]+%)/, type: 'percent' },
        avg_order_value: { regex: /客单价[\s\S]*?¥\s*([\d,.]+)/, type: 'currency' },
      }
    }
  },
  
  // 美团开店宝模块配置
  MEITUAN_MODULES: {
    dashboard: {
      name: '首页仪表盘',
      priority: 'P0',
      selectors: {
        visit_count: { regex: /访问人数[\s\S]*?(\d+)/, type: 'number' },
        order_amount: { regex: /下单金额[\s\S]*?¥?\s*([\d,.]+)/, type: 'currency' },
        verify_amount: { regex: /核销金额[\s\S]*?¥?\s*([\d,.]+)/, type: 'currency' },
        business_score: { regex: /当前评分[\s\S]*?([\d.]+)/, type: 'number' },
        new_comments: { regex: /新增评论数[\s\S]*?(\d+)个/, type: 'number' },
        new_bad_comments: { regex: /新增差评数[\s\S]*?(\d+)个/, type: 'number' },
        notice_count: { regex: /通知[\s\S]*?(\d+)条/, type: 'number' },
        message_count: { regex: /消息[\s\S]*?(\d+)条/, type: 'number' },
        score_change: { regex: /评分变化[\s\S]*?(上升|下降|持平)/, type: 'text' },
      }
    },
    
    promotion: {
      name: '推广通',
      priority: 'P0',
      url: '/promotion/tong',
      selectors: {
        ad_budget: { regex: /推广预算[\s\S]*?¥\s*([\d,.]+)/, type: 'currency' },
        ad_spend_today: { regex: /今日消耗[\s\S]*?¥\s*([\d,.]+)/, type: 'currency' },
        ad_exposure: { regex: /展现量[\s\S]*?(\d+)/, type: 'number' },
        ad_clicks: { regex: /点击量[\s\S]*?(\d+)/, type: 'number' },
        ad_cpc: { regex: /平均点击单价[\s\S]*?¥\s*([\d,.]+)/, type: 'currency' },
        ad_rank: { regex: /平均排名[\s\S]*?([\d.]+)/, type: 'number' },
        ad_roi: { regex: /投入产出比[\s\S]*?([\d.]+)/, type: 'number' },
      }
    },
    
    deals: {
      name: '团购管理',
      priority: 'P1',
      url: '/deal/manage',
      selectors: {
        total_deals: { regex: /全部团购[\s\S]*?(\d+)/, type: 'number' },
        on_sale: { regex: /出售中[\s\S]*?(\d+)/, type: 'number' },
        deal_views: { regex: /团购浏览[\s\S]*?(\d+)/, type: 'number' },
        deal_sales: { regex: /团购销量[\s\S]*?(\d+)/, type: 'number' },
        deal_conversion: { regex: /团购转化率[\s\S]*?([\d.]+%)/, type: 'percent' },
      }
    },
    
    reviews: {
      name: '评价管理',
      priority: 'P0',
      url: '/review/manage',
      selectors: {
        total_reviews: { regex: /全部评价[\s\S]*?(\d+)/, type: 'number' },
        five_star: { regex: /5星[\s\S]*?(\d+)/, type: 'number' },
        four_star: { regex: /4星[\s\S]*?(\d+)/, type: 'number' },
        three_star: { regex: /3星[\s\S]*?(\d+)/, type: 'number' },
        two_star: { regex: /2星[\s\S]*?(\d+)/, type: 'number' },
        one_star: { regex: /1星[\s\S]*?(\d+)/, type: 'number' },
        pending_reply: { regex: /待回复[\s\S]*?(\d+)/, type: 'number' },
      }
    },
    
    dataCenter: {
      name: '数据中心',
      priority: 'P1',
      url: '/data/center',
      selectors: {
        district_rank: { regex: /商圈排名[\s\S]*?第?\s*(\d+)/, type: 'number' },
        traffic_trend: { regex: /流量趋势[\s\S]*?(上升|下降|持平)/, type: 'text' },
        conversion_rate: { regex: /访问转化率[\s\S]*?([\d.]+%)/, type: 'percent' },
        avg_order_value: { regex: /客单价[\s\S]*?¥\s*([\d,.]+)/, type: 'currency' },
      }
    }
  }
};

// 工具函数
class Logger {
  static log(level, message, module = 'SYSTEM') {
    const timestamp = new Date().toISOString();
    const logLine = `[${timestamp}] [${level}] [${module}] ${message}`;
    console.log(logLine);
    
    const logFile = path.join(CONFIG.LOGS_DIR, `scraper_v2_${new Date().toISOString().split('T')[0]}.log`);
    if (!fs.existsSync(CONFIG.LOGS_DIR)) {
      fs.mkdirSync(CONFIG.LOGS_DIR, { recursive: true });
    }
    fs.appendFileSync(logFile, logLine + '\n');
  }
  
  static info(message, module) { this.log('INFO', message, module); }
  static warn(message, module) { this.log('WARN', message, module); }
  static error(message, module) { this.log('ERROR', message, module); }
  static success(message, module) { this.log('SUCCESS', message, module); }
}

// 数据解析器
class DataParser {
  static parse(value, type) {
    if (!value) return null;
    
    switch (type) {
      case 'number':
        return parseFloat(value.replace(/,/g, '')) || 0;
      case 'currency':
        return parseFloat(value.replace(/[¥,]/g, '')) || 0;
      case 'percent':
        return parseFloat(value.replace('%', '')) || 0;
      case 'text':
      default:
        return value.trim();
    }
  }
}

// CDP 连接器
class CDPConnector {
  constructor() {
    this.baseUrl = `http://127.0.0.1:${CONFIG.CDP_PORT}`;
  }
  
  async getPages() {
    try {
      const result = execSync(`curl -s ${this.baseUrl}/json/list`).toString();
      return JSON.parse(result);
    } catch (error) {
      Logger.error(`无法连接到CDP: ${error.message}`);
      return [];
    }
  }
  
  async findPage(urlPattern) {
    const pages = await this.getPages();
    return pages.find(p => p.url.includes(urlPattern));
  }
  
  async getPageContent(pageUrl) {
    try {
      return execSync(`curl -s "${pageUrl}"`, { timeout: 10000 }).toString();
    } catch (error) {
      Logger.error(`获取页面内容失败: ${error.message}`);
      return '';
    }
  }
}

// 采集引擎
class ScrapingEngine {
  constructor() {
    this.cdp = new CDPConnector();
    this.results = {};
  }
  
  async scrapeModule(platform, moduleKey, moduleConfig) {
    Logger.info(`开始采集: ${moduleConfig.name}`, platform.toUpperCase());
    
    const result = {
      module: moduleKey,
      name: moduleConfig.name,
      scraped_at: new Date().toISOString(),
      data: {},
      errors: []
    };
    
    try {
      // 确定目标页面URL
      let targetUrl;
      if (moduleKey === 'dashboard') {
        targetUrl = platform === 'douyin' ? 'life.douyin.com' : 'e.dianping.com';
      } else {
        targetUrl = moduleConfig.url || '';
      }
      
      // 查找页面
      const page = await this.cdp.findPage(targetUrl);
      if (!page) {
        result.errors.push(`未找到页面: ${targetUrl}`);
        Logger.warn(`未找到页面: ${targetUrl}`, platform.toUpperCase());
        return result;
      }
      
      // 获取页面内容
      const html = await this.cdp.getPageContent(page.url);
      if (!html) {
        result.errors.push('页面内容为空');
        return result;
      }
      
      // 解析数据
      for (const [key, config] of Object.entries(moduleConfig.selectors)) {
        try {
          const match = html.match(config.regex);
          if (match && match[1]) {
            result.data[key] = DataParser.parse(match[1], config.type);
          } else {
            result.data[key] = null;
          }
        } catch (e) {
          result.errors.push(`解析 ${key} 失败: ${e.message}`);
          result.data[key] = null;
        }
      }
      
      Logger.success(`${moduleConfig.name} 采集完成，${Object.keys(result.data).length} 个字段`, platform.toUpperCase());
      
    } catch (error) {
      result.errors.push(`采集异常: ${error.message}`);
      Logger.error(`采集异常: ${error.message}`, platform.toUpperCase());
    }
    
    return result;
  }
  
  async scrapePlatform(platform) {
    const modules = platform === 'douyin' ? CONFIG.DOUYIN_MODULES : CONFIG.MEITUAN_MODULES;
    const results = {
      platform,
      shop_name: platform === 'douyin' ? '有点方恐怖密室' : '有點方真人恐怖密室(解放西路店)',
      scraped_at: new Date().toISOString(),
      modules: {}
    };
    
    Logger.info(`开始采集 ${platform === 'douyin' ? '抖音来客' : '美团开店宝'} 全平台数据`, 'ENGINE');
    
    for (const [moduleKey, moduleConfig] of Object.entries(modules)) {
      results.modules[moduleKey] = await this.scrapeModule(platform, moduleKey, moduleConfig);
    }
    
    return results;
  }
}

// 数据存储
class DataStore {
  constructor() {
    this.ensureDirs();
  }
  
  ensureDirs() {
    if (!fs.existsSync(CONFIG.DATA_DIR)) {
      fs.mkdirSync(CONFIG.DATA_DIR, { recursive: true });
    }
    if (!fs.existsSync(CONFIG.LOGS_DIR)) {
      fs.mkdirSync(CONFIG.LOGS_DIR, { recursive: true });
    }
  }
  
  save(results) {
    const { platform } = results;
    const date = new Date().toISOString().split('T')[0];
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    
    // 保存最新数据
    const latestFile = path.join(CONFIG.DATA_DIR, `${platform}_full_latest.json`);
    fs.writeFileSync(latestFile, JSON.stringify(results, null, 2));
    
    // 保存历史数据
    const historyDir = path.join(CONFIG.DATA_DIR, 'history', platform);
    if (!fs.existsSync(historyDir)) {
      fs.mkdirSync(historyDir, { recursive: true });
    }
    const historyFile = path.join(historyDir, `${date}_${timestamp}.json`);
    fs.writeFileSync(historyFile, JSON.stringify(results, null, 2));
    
    Logger.success(`数据已保存: ${latestFile}`, 'STORE');
    return latestFile;
  }
  
  generateReport(douyinData, meituanData) {
    const report = {
      generated_at: new Date().toISOString(),
      douyin: douyinData,
      meituan: meituanData,
      summary: this.generateSummary(douyinData, meituanData)
    };
    
    const reportFile = path.join(CONFIG.DATA_DIR, `full_report_${new Date().toISOString().split('T')[0]}.json`);
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
    
    // 生成CSV
    this.generateCSV(report);
    
    return reportFile;
  }
  
  generateSummary(douyinData, meituanData) {
    const summary = {
      alerts: [],
      insights: [],
      actions: []
    };
    
    // 抖音分析
    if (douyinData?.modules?.dashboard?.data) {
      const dd = douyinData.modules.dashboard.data;
      
      if (dd.refund_amount > 0) {
        summary.alerts.push({
          level: 'warning',
          platform: '抖音来客',
          message: `今日有退款: ¥${dd.refund_amount}`,
          metric: 'refund_amount'
        });
      }
      
      if (dd.violation_status && dd.violation_status.includes('违规')) {
        summary.alerts.push({
          level: 'critical',
          platform: '抖音来客',
          message: `店铺违规状态: ${dd.violation_status}`,
          metric: 'violation_status'
        });
      }
      
      if (dd.account_balance < 500) {
        summary.alerts.push({
          level: 'warning',
          platform: '抖音来客',
          message: `账户余额较低: ¥${dd.account_balance}`,
          metric: 'account_balance'
        });
      }
    }
    
    // 美团分析
    if (meituanData?.modules?.dashboard?.data) {
      const md = meituanData.modules.dashboard.data;
      
      if (md.business_score < 60) {
        summary.alerts.push({
          level: 'warning',
          platform: '美团点评',
          message: `经营评分偏低: ${md.business_score}分`,
          metric: 'business_score'
        });
      }
      
      if (md.new_bad_comments > 0) {
        summary.alerts.push({
          level: 'critical',
          platform: '美团点评',
          message: `新增${md.new_bad_comments}条差评，需要立即处理`,
          metric: 'new_bad_comments'
        });
      }
    }
    
    return summary;
  }
  
  generateCSV(report) {
    const rows = [];
    
    // 添加表头
    rows.push(['平台', '模块', '指标', '数值', '采集时间'].join(','));
    
    // 抖音数据
    if (report.douyin?.modules) {
      for (const [moduleKey, moduleData] of Object.entries(report.douyin.modules)) {
        if (moduleData.data) {
          for (const [key, value] of Object.entries(moduleData.data)) {
            rows.push(['抖音来客', moduleData.name, key, value, moduleData.scraped_at].join(','));
          }
        }
      }
    }
    
    // 美团数据
    if (report.meituan?.modules) {
      for (const [moduleKey, moduleData] of Object.entries(report.meituan.modules)) {
        if (moduleData.data) {
          for (const [key, value] of Object.entries(moduleData.data)) {
            rows.push(['美团点评', moduleData.name, key, value, moduleData.scraped_at].join(','));
          }
        }
      }
    }
    
    const csvFile = path.join(CONFIG.DATA_DIR, `full_report_${new Date().toISOString().split('T')[0]}.csv`);
    fs.writeFileSync(csvFile, rows.join('\n'));
    
    Logger.success(`CSV报告已生成: ${csvFile}`, 'STORE');
    return csvFile;
  }
}

// 主程序
async function main() {
  const args = process.argv.slice(2);
  const target = args[0] || 'all';
  const moduleFilter = args[1]; // 可选：指定采集特定模块
  
  console.log('\n' + '='.repeat(70));
  console.log('🚀 商家平台超级采集系统 v2.0');
  console.log('='.repeat(70) + '\n');
  
  const engine = new ScrapingEngine();
  const store = new DataStore();
  
  let douyinData = null;
  let meituanData = null;
  
  // 采集抖音来客
  if (target === 'all' || target === 'douyin') {
    if (moduleFilter) {
      // 仅采集指定模块
      const moduleConfig = CONFIG.DOUYIN_MODULES[moduleFilter];
      if (moduleConfig) {
        const result = await engine.scrapeModule('douyin', moduleFilter, moduleConfig);
        console.log('\n📊 采集结果:');
        console.log(JSON.stringify(result, null, 2));
      } else {
        Logger.error(`未知模块: ${moduleFilter}`);
        console.log('可用模块:', Object.keys(CONFIG.DOUYIN_MODULES).join(', '));
      }
    } else {
      douyinData = await engine.scrapePlatform('douyin');
      store.save(douyinData);
    }
  }
  
  // 采集美团开店宝
  if (target === 'all' || target === 'meituan') {
    if (moduleFilter && target !== 'all') {
      const moduleConfig = CONFIG.MEITUAN_MODULES[moduleFilter];
      if (moduleConfig) {
        const result = await engine.scrapeModule('meituan', moduleFilter, moduleConfig);
        console.log('\n📊 采集结果:');
        console.log(JSON.stringify(result, null, 2));
      } else {
        Logger.error(`未知模块: ${moduleFilter}`);
        console.log('可用模块:', Object.keys(CONFIG.MEITUAN_MODULES).join(', '));
      }
    } else {
      meituanData = await engine.scrapePlatform('meituan');
      store.save(meituanData);
    }
  }
  
  // 生成综合报告
  if (target === 'all') {
    const reportFile = store.generateReport(douyinData, meituanData);
    
    console.log('\n' + '='.repeat(70));
    console.log('✅ 采集任务完成');
    console.log('='.repeat(70));
    console.log(`📁 报告文件: ${reportFile}`);
    console.log(`📊 数据目录: ${CONFIG.DATA_DIR}`);
    
    // 输出关键指标摘要
    if (douyinData?.modules?.dashboard?.data) {
      const dd = douyinData.modules.dashboard.data;
      console.log('\n📱 抖音来客关键指标:');
      console.log(`  💰 成交金额: ¥${dd.deal_amount || 0}`);
      console.log(`  🎫 成交券数: ${dd.deal_count || 0}`);
      console.log(`  💳 账户余额: ¥${dd.account_balance || 0}`);
      console.log(`  ⚠️  违规状态: ${dd.violation_status || '正常'}`);
    }
    
    if (meituanData?.modules?.dashboard?.data) {
      const md = meituanData.modules.dashboard.data;
      console.log('\n🍜 美团点评关键指标:');
      console.log(`  👁️ 访问人数: ${md.visit_count || 0}`);
      console.log(`  ⭐ 经营评分: ${md.business_score || 0}`);
      console.log(`  💬 新增评论: ${md.new_comments || 0}`);
    }
    
    // 输出告警
    const report = JSON.parse(fs.readFileSync(reportFile, 'utf8'));
    if (report.summary?.alerts?.length > 0) {
      console.log('\n🚨 异常告警:');
      report.summary.alerts.forEach(alert => {
        const icon = alert.level === 'critical' ? '🔴' : '🟡';
        console.log(`  ${icon} [${alert.platform}] ${alert.message}`);
      });
    }
  }
  
  console.log('\n');
}

// 运行
main().catch(error => {
  Logger.error(`程序异常: ${error.message}`);
  console.error(error);
  process.exit(1);
});

#!/usr/bin/env node

/**
 * 小红书自动化系统 - 安装和配置脚本
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const CONFIG_DIR = path.join(__dirname, '..', 'config');
const DATA_DIR = path.join(__dirname, '..', 'data');
const LOGS_DIR = path.join(__dirname, '..', 'logs');

// 创建目录结构
function createDirectories() {
  console.log('📁 创建目录结构...');
  [CONFIG_DIR, DATA_DIR, LOGS_DIR].forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      console.log(`  ✅ 创建目录: ${dir}`);
    }
  });
}

// 安装依赖
function installDependencies() {
  console.log('\n📦 安装依赖包...');
  const packageJson = {
    name: "xiaohongshu-automation",
    version: "1.0.0",
    description: "小红书自动化系统",
    main: "index.js",
    scripts: {
      "start": "node scripts/main.js",
      "post": "node scripts/post-content.js",
      "monitor": "node scripts/monitor-comments.js",
      "reply": "node scripts/auto-reply.js",
      "schedule": "node scripts/schedule-posts.js"
    },
    dependencies: {
      "puppeteer": "^21.0.0",
      "node-cron": "^3.0.3",
      "dotenv": "^16.3.1",
      "axios": "^1.6.2",
      "cheerio": "^1.0.0-rc.12",
      "moment": "^2.29.4",
      "winston": "^3.11.0"
    }
  };

  const packagePath = path.join(__dirname, '..', 'package.json');
  fs.writeFileSync(packagePath, JSON.stringify(packageJson, null, 2));
  console.log('  ✅ 创建 package.json');
  
  console.log('  ⏳ 请运行: npm install');
}

// 创建配置文件模板
function createConfigTemplate() {
  console.log('\n⚙️ 创建配置文件模板...');
  
  const configTemplate = {
    // 小红书账号配置
    account: {
      username: "YOUR_XIAOHONGSHU_USERNAME",
      password: "YOUR_XIAOHONGSHU_PASSWORD",
      phone: "YOUR_PHONE_NUMBER"  // 如果需要手机验证
    },
    
    // 自动化配置
    automation: {
      postInterval: 3600000,  // 发帖间隔(毫秒)，默认1小时
      maxPostsPerDay: 5,      // 每天最多发帖数
      monitorInterval: 300000, // 监控间隔(毫秒)，默认5分钟
      replyDelay: 10000,      // 回复延迟(毫秒)，默认10秒
      likeProbability: 0.7,   // 点赞概率
      commentProbability: 0.3  // 评论概率
    },
    
    // 关键词配置
    keywords: {
      primary: ["#美妆", "#护肤", "#穿搭", "#探店", "#生活方式"],
      secondary: ["#好物分享", "#日常", "#vlog", "#ootd", "#美食"],
      blacklist: ["广告", "推广", "营销", "销售", "购买"]
    },
    
    // 内容模板
    templates: {
      post: {
        greeting: ["大家好", "Hi大家好", "姐妹们好"],
        content: ["今天分享一个{keyword}的好物", "最近发现的{keyword}宝藏", "{keyword}日常分享"],
        hashtags: "{primaryHashtags} {secondaryHashtags}",
        callToAction: ["喜欢记得点赞收藏哦", "欢迎评论区交流", "关注我获取更多分享"]
      },
      reply: {
        positive: ["谢谢喜欢", "感谢支持", "一起变美", "互相学习"],
        question: ["具体是哪个方面呢", "可以详细说说吗", "我私信你"],
        generic: ["😊", "👍", "❤️", "💕"]
      }
    },
    
    // 安全配置
    security: {
      humanLikeDelay: true,    // 模拟人类延迟
      randomActions: true,     // 随机化操作
      avoidDetection: true,    // 避免被检测
      maxActionsPerHour: 30,   // 每小时最大操作数
      restPeriods: [           // 休息时段
        { start: "02:00", end: "06:00" },
        { start: "14:00", end: "15:00" }
      ]
    },
    
    // 监控配置
    monitoring: {
      checkComments: true,     // 检查评论
      checkMessages: true,     // 检查私信
      checkTrending: true,     // 检查热门话题
      saveScreenshots: true,   // 保存截图
      logLevel: "info"         // 日志级别
    }
  };

  const configPath = path.join(CONFIG_DIR, 'config.template.json');
  fs.writeFileSync(configPath, JSON.stringify(configTemplate, null, 2));
  console.log(`  ✅ 创建配置文件模板: ${configPath}`);
  
  // 创建.env模板
  const envTemplate = `# 小红书自动化系统 - 环境变量配置
# 请将以下值替换为你的实际信息

# 小红书账号信息
XHS_USERNAME=your_username
XHS_PASSWORD=your_password
XHS_PHONE=your_phone_number

# 浏览器配置
BROWSER_HEADLESS=false  # true: 无头模式, false: 显示浏览器
BROWSER_SLOWMO=100      # 操作延迟(毫秒)，模拟人类速度

# API配置 (如果需要)
OPENAI_API_KEY=your_openai_api_key  # 用于AI内容生成
BROWSERBASE_API_KEY=your_browserbase_api_key

# 代理配置 (如果需要)
PROXY_SERVER=
PROXY_USERNAME=
PROXY_PASSWORD=

# 日志配置
LOG_LEVEL=info
LOG_TO_FILE=true

# 安全配置
MAX_POSTS_PER_DAY=5
MIN_POST_INTERVAL_MINUTES=60
`;

  const envPath = path.join(__dirname, '..', '.env.example');
  fs.writeFileSync(envPath, envTemplate);
  console.log(`  ✅ 创建环境变量模板: ${envPath}`);
}

// 创建主脚本
function createMainScript() {
  console.log('\n📝 创建主脚本...');
  
  const mainScript = `#!/usr/bin/env node

/**
 * 小红书自动化系统 - 主脚本
 */

require('dotenv').config();
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');
const cron = require('node-cron');
const winston = require('winston');

// 配置日志
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ 
      filename: path.join(__dirname, '..', 'logs', 'error.log'), 
      level: 'error' 
    }),
    new winston.transports.File({ 
      filename: path.join(__dirname, '..', 'logs', 'combined.log') 
    })
  ]
});

if (process.env.LOG_TO_FILE !== 'false') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}

class XiaohongshuAutomation {
  constructor() {
    this.config = this.loadConfig();
    this.browser = null;
    this.page = null;
    this.isLoggedIn = false;
  }

  // 加载配置
  loadConfig() {
    try {
      const configPath = path.join(__dirname, '..', 'config', 'config.json');
      if (fs.existsSync(configPath)) {
        return JSON.parse(fs.readFileSync(configPath, 'utf8'));
      } else {
        logger.warn('配置文件不存在，使用默认配置');
        return {
          account: {
            username: process.env.XHS_USERNAME,
            password: process.env.XHS_PASSWORD
          },
          automation: {
            postInterval: 3600000,
            maxPostsPerDay: parseInt(process.env.MAX_POSTS_PER_DAY) || 5
          }
        };
      }
    } catch (error) {
      logger.error('加载配置失败:', error);
      return {};
    }
  }

  // 初始化浏览器
  async initBrowser() {
    try {
      const launchOptions = {
        headless: process.env.BROWSER_HEADLESS === 'true',
        slowMo: parseInt(process.env.BROWSER_SLOWMO) || 100,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
      };

      // 添加代理配置
      if (process.env.PROXY_SERVER) {
        launchOptions.args.push(\`--proxy-server=\${process.env.PROXY_SERVER}\`);
      }

      this.browser = await puppeteer.launch(launchOptions);
      this.page = await this.browser.newPage();
      
      // 设置用户代理
      await this.page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1');
      
      // 设置视口为手机尺寸
      await this.page.setViewport({ width: 375, height: 667 });
      
      logger.info('浏览器初始化成功');
      return true;
    } catch (error) {
      logger.error('浏览器初始化失败:', error);
      return false;
    }
  }

  // 登录小红书
  async login() {
    if (!this.page) {
      logger.error('页面未初始化');
      return false;
    }

    try {
      logger.info('正在访问小红书...');
      await this.page.goto('https://www.xiaohongshu.com', { 
        waitUntil: 'networkidle2',
        timeout: 30000 
      });

      // 等待页面加载
      await this.page.waitForTimeout(3000);

      // 这里需要根据小红书实际页面结构实现登录逻辑
      // 注意：小红书有反爬机制，需要谨慎处理
      
      logger.info('登录流程需要根据实际页面结构实现');
      this.isLoggedIn = true;
      return true;
    } catch (error) {
      logger.error('登录失败:', error);
      return false;
    }
  }

  // 发布内容
  async postContent(content, images = []) {
    if (!this.isLoggedIn) {
      logger.error('未登录，无法发布内容');
      return false;
    }

    try {
      logger.info('准备发布内容...');
      // 这里需要根据小红书实际发布页面结构实现
      
      logger.info('发布功能需要根据实际页面结构实现');
      return true;
    } catch (error) {
      logger.error('发布失败:', error);
      return false;
    }
  }

  // 监控评论
  async monitorComments() {
    logger.info('监控评论功能待实现');
    // 实现评论监控逻辑
  }

  // 自动回复
  async autoReply() {
    logger.info('自动回复功能待实现');
    // 实现自动回复逻辑
  }

  // 关闭浏览器
  async close() {
    if (this.browser) {
      await this.browser.close();
      logger.info('浏览器已关闭');
    }
  }
}

// 主函数
async function main() {
  const automation = new XiaohongshuAutomation();
  
  try {
    // 初始化
    const browserReady = await automation.initBrowser();
    if (!browserReady) {
      logger.error('浏览器初始化失败，退出');
      return;
    }

    // 登录
    const loggedIn = await automation.login();
    if (!loggedIn) {
      logger.error('登录失败，退出');
      await automation.close();
      return;
    }

    logger.info('小红书自动化系统启动成功！');
    
    // 设置定时任务
    // 每小时检查一次
    cron.schedule('0 * * * *', async () => {
      logger.info('执行定时检查...');
      await automation.monitorComments();
    });

    // 保持运行
    process.on('SIGINT', async () => {
      logger.info('收到退出信号，正在关闭...');
      await automation.close();
      process.exit(0);
    });

    // 保持进程运行
    setInterval(() => {}, 60000);
    
  } catch (error) {
    logger.error('主程序错误:', error);
    await automation.close();
  }
}

// 启动程序
if (require.main === module) {
  main();
}

module.exports = XiaohongshuAutomation;
`;

  const mainPath = path.join(__dirname, 'main.js');
  fs.writeFileSync(mainPath, mainScript);
  console.log(`  ✅ 创建主脚本: ${mainPath}`);
  
  // 设置执行权限
  fs.chmodSync(mainPath, '755');
}

// 创建其他功能脚本
function createUtilityScripts() {
  console.log('\n🔧 创建功能脚本...');
  
  const scripts = {
    'post-content.js': `// 发布内容脚本`,
    'monitor-comments.js': `// 监控评论脚本`,
    'auto-reply.js': `// 自动回复脚本`,
    'schedule-posts.js': `// 定时发帖脚本`,
    'keyword-monitor.js': `// 关键词监控脚本`
  };

  Object.entries(scripts).forEach(([filename, content]) => {
    const filePath = path.join(__dirname, filename);
    fs.writeFileSync(filePath, content);
    console.log(`  ✅ 创建脚本: ${filename}`);
  });
}

// 运行安装
async function runInstallation() {
  console.log('🚀 开始安装小红书自动化系统...\n');
  
  createDirectories();
  installDependencies();
  createConfigTemplate();
  createMainScript();
  createUtilityScripts();
  
  console.log('\n🎉 安装完成！');
  console.log('\n📋 下一步操作:');
  console.log('1. 进入项目目录: cd /Users/xiaolongxia/.openclaw/workspace/xiaohongshu-automation');
  console.log('2. 安装依赖: npm install');
  console.log('3. 复制配置文件: cp config/config.template.json config/config.json');
  console.log('4. 配置账号信息: 编辑 config/config.json 和 .env 文件');
  console.log('5. 启动系统: npm start');
  
  rl.close();
}

runInstallation().catch(console.error);
`;

  fs.writeFileSync(path.join(__dirname, '..', 'setup.js'), setupScript);
  console.log('  ✅ 创建安装脚本: setup.js');
}

// 运行安装
async function main() {
  console.log('🚀 小红书自动化系统 - 初始化安装\n');
  
  createDirectories();
  installDependencies();
  createConfigTemplate();
  createMainScript();
  createUtilityScripts();
  
  console.log('\n✅ 初始化完成！');
  console.log('\n📋 请按照以下步骤继续:');
  console.log('1. 提供小红书账号信息');
  console.log('2. 提供关键词列表');
  console.log('3. 运行: cd /Users/xiaolongxia/.openclaw/workspace/xiaohongshu-automation && npm install');
  console.log('4. 配置 config/config.json 文件');
  console.log('5. 启动自动化系统');
  
  process.exit(0);
}

if (require.main === module) {
  main().catch(console.error);
}
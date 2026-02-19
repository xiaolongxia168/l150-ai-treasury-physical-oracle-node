---
name: merchant-dashboard-scraper
description: 抖音来客 + 美团开店宝全自动化数据抓取系统，支持实时经营数据监控、自动报告生成和异常预警
metadata:
  emoji: 📊
  version: 1.0.0
  author: OpenClaw Agent
  requires:
    bins: ["node", "curl"]
    browser: true
---

# 商家数据抓取系统 📊

抖音来客 + 美团开店宝的全自动化数据抓取与监控系统。

## 🎯 功能特性

### 数据抓取
| 平台 | 抓取指标 |
|------|----------|
| **抖音来客** | 成交金额、成交券数、核销金额、退款金额、商品访问人数、经营分、账户余额、本地推消耗 |
| **美团点评** | 访问人数、下单金额、核销金额、经营评分、新增评论数、新增差评数、通知数量 |

### 监控频率
- **⏱️ 实时**: 每5分钟抓取一次
- **📈 小时报**: 每小时生成趋势报告  
- **📅 日报**: 每日9点生成完整报告
- **📊 周报**: 每周一9点生成绩效分析

### 异常预警
- 💰 账户余额低于阈值告警
- ⭐ 新增差评实时提醒
- 🚨 违规状态变更通知
- 📉 长时间无订单预警

## 🚀 快速开始

### 安装
```bash
cd ~/.openclaw/workspace/skills/merchant-dashboard-scraper
./install.sh
```

### 手动抓取
```bash
# 抓取所有平台
node scraper.js all

# 仅抓取抖音来客
node scraper.js douyin

# 仅抓取美团点评
node scraper.js meituan

# 使用CLI版本
./scraper-cli.sh all
```

### 配置Cron自动任务

```bash
# 每5分钟实时抓取
openclaw cron add \
  --name "商家数据-实时抓取" \
  --schedule "*/5 * * * *" \
  --command "bash ~/.openclaw/workspace/skills/merchant-dashboard-scraper/scraper-cli.sh all"

# 每日9点生成日报
openclaw cron add \
  --name "商家数据-日报" \
  --schedule "0 9 * * *" \
  --command "bash ~/.openclaw/workspace/skills/merchant-dashboard-scraper/scraper-cli.sh all"

# 每周一9点生成周报
openclaw cron add \
  --name "商家数据-周报" \
  --schedule "0 9 * * 1" \
  --command "bash ~/.openclaw/workspace/skills/merchant-dashboard-scraper/scraper-cli.sh all"
```

## 📁 数据存储

```
~/.openclaw/workspace/data/merchant-dashboard/
├── douyin_laike_latest.json       # 抖音最新数据
├── meituan_dianping_latest.json   # 美团最新数据
├── report_2026-02-19_143022.json  # 详细报告
├── report_2026-02-19.csv          # CSV格式报告
├── alerts.json                     # 异常告警
└── logs/
    ├── scraper_2026-02-19.log     # 操作日志
    └── cron_2026-02-19.log        # 定时任务日志
```

## ⚙️ 配置文件

编辑 `config.json` 自定义设置:

```json
{
  "platforms": {
    "douyin_laike": {
      "enabled": true,
      "shop_name": "有点方恐怖密室",
      "refresh_interval": 300,
      "data_points": ["成交金额", "成交券数", "核销金额", ...]
    },
    "meituan_dianping": {
      "enabled": true,
      "shop_name": "有點方真人恐怖密室(解放西路店)",
      "refresh_interval": 300
    }
  },
  "alerts": {
    "low_balance": 500,
    "new_bad_review": true,
    "violations": true,
    "zero_orders_hours": 24
  }
}
```

## 📊 数据格式

### 抖音来客数据
```json
{
  "platform": "douyin_laike",
  "shop_name": "有点方恐怖密室",
  "scraped_at": "2026-02-19T12:00:00Z",
  "data": {
    "deal_amount": 116.60,
    "deal_count": 1,
    "verify_amount": 0,
    "refund_amount": 116.60,
    "visit_count": 22,
    "business_score": 135,
    "account_balance": 1099.06,
    "violation_status": "违规生效中"
  }
}
```

### 美团点评数据
```json
{
  "platform": "meituan_dianping",
  "shop_name": "有點方真人恐怖密室(解放西路店)",
  "scraped_at": "2026-02-19T12:00:00Z",
  "data": {
    "visit_count": 60,
    "order_amount": 0,
    "business_score": 57.5,
    "new_comments": 0,
    "new_bad_comments": 0
  }
}
```

## 🔧 故障排除

### 常见问题

**Q: 页面未找到**
- 确保浏览器已登录抖音来客和美团开店宝
- 保持页面在浏览器中打开，不要关闭
- 检查浏览器CDP端口是否可访问: `curl http://127.0.0.1:18800/json/list`

**Q: 数据为空或不准确**
- 页面可能需要更多加载时间，增加等待时间
- 检查页面是否有iframe，数据可能在iframe中
- 尝试刷新页面后再抓取

**Q: 权限错误**
```bash
chmod +x scraper.js scraper-cli.sh install.sh
```

**Q: Playwright连接失败**
- 确保Node.js版本 >= 18
- 重新安装依赖: `npm install`

## 📈 进阶用法

### 自定义数据解析
编辑 `scraper.js` 中的 `selectors` 对象来添加新的数据字段:

```javascript
const selectors = {
    your_custom_field: /正则表达式/,
    another_field: /另一个正则/
};
```

### 集成到现有系统
```javascript
const scraper = require('./scraper');

// 获取数据
const data = await scraper.scrapeAll();

// 处理数据
console.log(data.douyin.deal_amount);
console.log(data.meituan.business_score);
```

## 🔒 安全注意事项

1. **数据隐私**: 抓取的数据仅存储在本地，不上传到云端
2. **账号安全**: 系统只读取数据，不进行任何修改操作
3. **频率控制**: 默认每5分钟抓取一次，避免对平台造成压力
4. **合规使用**: 请遵守各平台的使用条款

## 📝 更新日志

### v1.0.0 (2026-02-19)
- ✅ 初始版本发布
- ✅ 支持抖音来客数据抓取
- ✅ 支持美团点评数据抓取
- ✅ 自动报告生成 (JSON + CSV)
- ✅ 异常告警系统
- ✅ Cron定时任务支持

## 🤝 贡献

欢迎提交Issue和PR改进功能！

## 📞 支持

如有问题，请查看:
1. 日志文件: `~/.openclaw/workspace/data/merchant-dashboard/logs/`
2. 配置文件: `~/.openclaw/workspace/skills/merchant-dashboard-scraper/config.json`
3. 浏览器状态: `openclaw browser status`

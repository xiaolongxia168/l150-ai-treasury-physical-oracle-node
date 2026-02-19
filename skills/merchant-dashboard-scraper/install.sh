#!/bin/bash
# 商家数据抓取系统安装脚本
# 抖音来客 + 美团开店宝自动化

set -e

echo "🚀 商家数据抓取系统安装中..."

# 创建工作目录
DATA_DIR="$HOME/.openclaw/workspace/data/merchant-dashboard"
SKILL_DIR="$HOME/.openclaw/workspace/skills/merchant-dashboard-scraper"

mkdir -p "$DATA_DIR"/{logs,reports}
mkdir -p "$SKILL_DIR"

echo "✅ 目录结构创建完成"

# 检查依赖
echo "🔍 检查依赖..."

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "⚠️ 未安装Node.js，正在安装..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install node
    else
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
        sudo apt-get install -y nodejs
    fi
fi

# 检查Playwright (可选，用于高级抓取)
if command -v npm &> /dev/null; then
    echo "📦 安装Playwright (用于高级浏览器自动化)..."
    cd "$SKILL_DIR"
    npm init -y 2>/dev/null || true
    npm install playwright --save 2>/dev/null || echo "⚠️ Playwright安装失败，基础功能仍可用"
fi

echo "✅ 依赖检查完成"

# 创建配置文件
cat > "$SKILL_DIR/config.json" << 'EOF'
{
  "platforms": {
    "douyin_laike": {
      "enabled": true,
      "shop_name": "有点方恐怖密室",
      "cdp_url": "http://127.0.0.1:18800",
      "refresh_interval": 300,
      "data_points": [
        "成交金额",
        "成交券数",
        "核销金额",
        "退款金额",
        "商品访问人数",
        "经营分",
        "账户余额",
        "本地推消耗"
      ]
    },
    "meituan_dianping": {
      "enabled": true,
      "shop_name": "有點方真人恐怖密室(解放西路店)",
      "cdp_url": "http://127.0.0.1:18800",
      "refresh_interval": 300,
      "data_points": [
        "访问人数",
        "下单金额",
        "核销金额",
        "经营评分",
        "新增评论数",
        "新增差评数",
        "通知数量",
        "消息数量"
      ]
    }
  },
  "schedules": {
    "realtime": "*/5 * * * *",
    "hourly": "0 * * * *",
    "daily": "0 9 * * *",
    "weekly": "0 9 * * 1"
  },
  "alerts": {
    "low_balance": 500,
    "new_bad_review": true,
    "violations": true,
    "zero_orders_hours": 24
  }
}
EOF

echo "✅ 配置文件创建完成"

# 创建定时任务脚本
cat > "$SKILL_DIR/run-scraper.sh" << 'EOF'
#!/bin/bash
# 商家数据抓取定时任务

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$HOME/.openclaw/workspace/data/merchant-dashboard/logs/cron-$(date +%Y%m%d).log"

echo "[$(date)] 开始执行抓取任务" >> "$LOG_FILE"

cd "$SCRIPT_DIR"
node scraper.js all >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[$(date)] 抓取任务完成 ✓" >> "$LOG_FILE"
else
    echo "[$(date)] 抓取任务失败 ✗" >> "$LOG_FILE"
fi
EOF

chmod +x "$SKILL_DIR/run-scraper.sh"
chmod +x "$SKILL_DIR/scraper.js"
chmod +x "$SKILL_DIR/scraper.py"

echo "✅ 执行脚本权限设置完成"

# 创建SKILL.md
cat > "$SKILL_DIR/SKILL.md" << 'EOF'
---
name: merchant-dashboard-scraper
description: 抖音来客 + 美团开店宝全自动化数据抓取系统，支持实时经营数据监控、自动报告生成和异常预警
metadata:
  emoji: 📊
  version: 1.0.0
  author: OpenClaw Agent
---

# 商家数据抓取系统

抖音来客 + 美团开店宝的全自动化数据抓取与监控系统。

## 功能特性

### 1. 数据抓取
- **抖音来客**: 成交金额、券数、核销、退款、访问人数、经营分、账户余额
- **美团点评**: 访问人数、下单金额、核销金额、评分、评论数、差评数

### 2. 监控频率
- **实时**: 每5分钟抓取一次
- **小时报**: 每小时生成趋势报告
- **日报**: 每日9点生成完整报告
- **周报**: 每周一9点生成绩效分析

### 3. 异常预警
- 账户余额低于阈值
- 新增差评提醒
- 违规状态变更
- 长时间无订单预警

## 快速开始

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
```

### 配置Cron任务
```bash
# 每5分钟实时抓取
openclaw cron add --name "商家数据-实时抓取" --schedule "*/5 * * * *" \
  --command "node ~/.openclaw/workspace/skills/merchant-dashboard-scraper/scraper.js all"

# 每日报告
openclaw cron add --name "商家数据-日报" --schedule "0 9 * * *" \
  --command "node ~/.openclaw/workspace/skills/merchant-dashboard-scraper/reporter.js daily"
```

## 数据存储

```
~/.openclaw/workspace/data/merchant-dashboard/
├── douyin_laike_latest.json    # 抖音最新数据
├── meituan_dianping_latest.json # 美团最新数据
├── report_2026-02-19.json      # 每日报告
├── report_2026-02-19.csv       # CSV格式报告
└── logs/
    └── scraper_2026-02-19.log  # 操作日志
```

## 配置文件

编辑 `config.json` 自定义设置:

```json
{
  "platforms": {
    "douyin_laike": {
      "enabled": true,
      "refresh_interval": 300
    }
  },
  "alerts": {
    "low_balance": 500,
    "new_bad_review": true
  }
}
```

## 故障排除

1. **页面未找到**: 确保浏览器已登录并保持抖音/美团页面打开
2. **数据为空**: 检查页面是否加载完成，可能需要增加等待时间
3. **权限错误**: 确保脚本有执行权限: `chmod +x scraper.js`
EOF

echo "✅ SKILL.md 创建完成"

# 测试运行
echo "🧪 测试运行..."
cd "$SKILL_DIR"
node scraper.js all || echo "⚠️ 测试运行失败，请检查浏览器状态"

echo ""
echo "🎉 安装完成！"
echo "📁 数据目录: $DATA_DIR"
echo "🔧 配置目录: $SKILL_DIR"
echo ""
echo "使用方法:"
echo "  node $SKILL_DIR/scraper.js all      # 抓取所有平台"
echo "  node $SKILL_DIR/scraper.js douyin   # 仅抓取抖音"
echo "  node $SKILL_DIR/scraper.js meituan  # 仅抓取美团"
echo ""

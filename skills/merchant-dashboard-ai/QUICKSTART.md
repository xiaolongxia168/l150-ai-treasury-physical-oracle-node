# 🚀 商家后台智能助手 - 快速启动指南

## ⚡ 30 秒快速开始

```bash
cd /Users/xiaolongxia/.openclaw/workspace/skills/merchant-dashboard-ai

# 1. 安装依赖
pip3 install playwright pandas schedule requests
playwright install chromium

# 2. 首次登录（会打开浏览器）
python3 scripts/login_assistant.py --platform douyin_laike

# 3. 启动智能全量抓取
python3 scripts/intelligent_crawler.py
```

## 🎯 核心功能

### ✅ 智能全量抓取（NEW!）
**自动点击所有菜单，抓取整个商家后台的所有数据！**

```python
# intelligent_crawler.py 会自动：
✓ 发现所有菜单入口（导航、侧边栏等）
✓ 递归点击进入所有子页面
✓ 自动翻页抓取分页数据
✓ 提取表格、列表、统计数字、图表
✓ 智能去重，避免重复抓取
✓ 处理动态加载内容
```

### 📊 数据提取能力

| 数据类型 | 自动识别 | 示例 |
|---------|---------|------|
| **表格数据** | ✅ | 订单列表、商品列表、财务报表 |
| **列表数据** | ✅ | 评价列表、客户列表 |
| **统计数字** | ✅ | GMV、订单量、转化率 |
| **图表数据** | ✅ | ECharts、Chart.js 图表 |
| **表单结构** | ✅ | 功能入口分析 |
| **分页内容** | ✅ | 自动翻页，抓取全部 |

## 🎬 使用演示

### 场景 1：首次使用

```bash
# Step 1: 登录抖音来客
python3 scripts/login_assistant.py --platform douyin_laike

# 按提示操作：
# 1. 浏览器会自动打开
# 2. 手动输入账号密码
# 3. 完成验证码
# 4. 登录成功后回到终端按 Enter
# 5. Cookie 自动保存

# Step 2: 开始全量抓取
python3 scripts/intelligent_crawler.py

# 爬虫会自动：
# ✓ 访问首页
# ✓ 发现所有菜单（订单、商品、财务...）
# ✓ 点击每个菜单
# ✓ 抓取表格数据
# ✓ 自动翻页到最后一页
# ✓ 提取所有数据
```

### 场景 2：定时自动抓取

```bash
# 使用 auto_pilot.py 实现定时抓取
python3 scripts/auto_pilot.py

# 或者集成到 cron（推荐）
# 编辑 crontab
crontab -e

# 添加：每小时抓取一次
0 * * * * cd /Users/xiaolongxia/.openclaw/workspace/skills/merchant-dashboard-ai && python3 scripts/intelligent_crawler.py
```

### 场景 3：查看抓取结果

```bash
# 查看抓取的数据文件
ls -lh data/

# 示例输出：
# full_crawl_20260219_163045.json  (2.3 MB)
# ↑ 包含所有页面的全部数据

# 查看数据内容
cat data/full_crawl_*.json | jq '.[] | {url, tables, lists}' | head -50

# 统计抓取结果
cat data/full_crawl_*.json | jq 'length'  # 抓取的页面数
cat data/full_crawl_*.json | jq '.[].tables | length' | awk '{s+=$1} END {print s}'  # 表格总数
```

## 🧠 智能抓取策略

### 1. 自动菜单发现
```python
# 爬虫会尝试这些选择器：
- nav a                  # 顶部导航
- .sidebar a             # 侧边栏
- .menu a                # 菜单
- [role="navigation"] a  # 语义化导航
- aside a                # 侧边栏
```

### 2. 智能去重
```python
# 基于内容哈希去重
- 相同内容的页面只抓取一次
- 自动跳过已访问的 URL
- 分页内容重复自动停止
```

### 3. 分页处理
```python
# 自动识别并点击"下一页"
next_selectors = [
    'a:has-text("下一页")',
    'button:has-text("下一页")',
    '[class*="next"]',
    '.ant-pagination-next',
    '.el-pagination__next'
]
```

### 4. 数据提取
```python
# 自动提取：
- 所有 <table> 数据
- 所有 <ul>/<ol> 列表
- 统计数字（class*="stat|metric|count"）
- ECharts/Chart.js 图表
- 表单结构
```

## 📁 数据存储结构

```
data/
├── full_crawl_20260219_163045.json  # 完整抓取数据
│   [
│     {
│       "url": "https://laike.douyin.com/order/list",
│       "title": "订单管理",
│       "depth": 1,
│       "pagination": 1,
│       "tables": [
│         {
│           "headers": ["订单号", "金额", "状态", "时间"],
│           "rows": [["12345", "99.00", "已完成", "2026-02-19"], ...],
│           "row_count": 50
│         }
│       ],
│       "lists": [...],
│       "statistics": ["今日订单: 123", "GMV: 12,345"],
│       "charts": [...]
│     },
│     ...
│   ]
└── ...
```

## ⚙️ 高级配置

### 自定义抓取深度

```python
# 编辑 intelligent_crawler.py
await crawler.crawl_page(url, depth=0, max_depth=3)  # 改为 5 或更大
```

### 自定义抓取范围

```python
# 编辑配置，只抓取特定类型数据
config = {
    'scraping': {
        'data_types': [
            'orders',      # 只抓订单
            'finance'      # 和财务
        ]
    }
}
```

### 关闭无头模式（调试）

```python
crawler = IntelligentCrawler(config, headless=False)  # 可以看到浏览器操作
```

## 🛠️ 故障排除

### 问题 1：登录失败
```bash
# 解决：清除旧 Cookie，重新登录
rm -rf cookies/*
python3 scripts/login_assistant.py --platform douyin_laike --headless false
```

### 问题 2：抓取不完整
```bash
# 解决：关闭无头模式，查看实际页面
# 编辑 intelligent_crawler.py，设置 headless=False
```

### 问题 3：被反爬虫拦截
```bash
# 解决：增加延迟，降低抓取频率
# 编辑 intelligent_crawler.py
await self.page.wait_for_timeout(5000)  # 增加到 5 秒
```

### 问题 4：数据量太大
```bash
# 解决：分批抓取
# 修改 max_depth 参数，先抓取浅层数据
```

## 🎯 最佳实践

### 1. 首次使用
```bash
# 建议关闭无头模式，观察抓取过程
headless = False
```

### 2. 生产环境
```bash
# 使用无头模式 + 定时任务
headless = True
# 配置 cron 每天凌晨抓取
```

### 3. 数据分析
```bash
# 抓取后立即进行 AI 分析
python3 scripts/intelligent_crawler.py && python3 scripts/ai_analyzer.py
```

## 🚀 集成到 OpenClaw

### 创建 Cron 任务

在 OpenClaw 中配置定时任务：

```javascript
// 在 OpenClaw workspace/AGENTS.md 或配置中添加
{
  "cron_tasks": [
    {
      "name": "merchant-full-crawl",
      "schedule": "0 2 * * *",  // 每天凌晨 2 点
      "command": "cd /Users/xiaolongxia/.openclaw/workspace/skills/merchant-dashboard-ai && python3 scripts/intelligent_crawler.py"
    }
  ]
}
```

## 📊 数据分析示例

```python
# 读取抓取的数据
import json

with open('data/full_crawl_20260219.json', 'r') as f:
    data = json.load(f)

# 统计分析
total_pages = len(data)
total_tables = sum(len(page.get('tables', [])) for page in data)
total_rows = sum(
    sum(table.get('row_count', 0) for table in page.get('tables', []))
    for page in data
)

print(f"抓取页面: {total_pages}")
print(f"表格数量: {total_tables}")
print(f"数据行数: {total_rows}")
```

## 💡 下一步

1. ✅ 完成首次登录
2. ✅ 运行全量抓取
3. ✅ 查看抓取结果
4. 🔄 配置定时任务
5. 🧠 启用 AI 分析
6. 📊 生成可视化报告

---

**你的智能商家助手已就绪！** 🎉

**有问题？** 查看完整文档 `SKILL.md` 或查看日志 `logs/`

# 商家后台智能助手 🏪

自动化抓取抖音来客、美团开店宝全量数据，AI 智能分析优化建议。

## 🚀 快速开始（3 步上手）

### 第一步：安装依赖

```bash
cd /Users/xiaolongxia/.openclaw/workspace/skills/merchant-dashboard-ai

# 安装 Python 依赖
pip3 install playwright pandas schedule requests

# 安装浏览器
playwright install chromium
```

### 第二步：首次登录

```bash
# 登录抖音来客（会打开浏览器窗口）
python3 scripts/login_assistant.py --platform douyin_laike

# 登录美团开店宝
python3 scripts/login_assistant.py --platform meituan_kaidian
```

**操作步骤：**
1. 浏览器自动打开登录页
2. 手动输入账号密码
3. 完成验证码（如果有）
4. 登录成功后，回到终端按 Enter
5. Cookie 自动保存，后续无需重复登录

### 第三步：启动自动抓取

```bash
# 运行一次全量抓取
python3 scripts/auto_pilot.py

# 或者启动定时任务（推荐）
python3 scripts/scheduler.py --daemon
```

## ✅ 完成！

现在系统会自动：
- ✅ 每小时增量抓取最新数据
- ✅ 每天凌晨2点全量抓取
- ✅ 早上8点生成 AI 分析报告
- ✅ 异常情况实时预警

## 📊 查看数据

```bash
# 查看抓取的数据
ls -lh data/raw/

# 查看 AI 分析报告
cat data/analysis/insights_*.md

# 查看日志
tail -f logs/auto_pilot.log
```

## 🎯 核心功能

### 1. 全量数据抓取
自动抓取所有页面的全部数据：
- 订单、商品、客户、财务、营销、评价、物流

### 2. AI 智能分析
- 趋势分析、用户洞察、问题诊断、优化建议

### 3. 自动化报告
- 每日简报、周报月报、实时预警

### 4. 智能学习
- 根据历史数据优化策略

## 🛠️ 常用命令

```bash
# 手动触发全量抓取
python3 scripts/auto_pilot.py

# 生成今日分析报告
python3 scripts/ai_analyzer.py --report daily

# 查看配置
cat config.json

# 清除 Cookie 重新登录
rm -rf cookies/*
python3 scripts/login_assistant.py --platform douyin_laike
```

## 📖 完整文档

查看 `SKILL.md` 获取详细文档和高级功能。

## 🆘 遇到问题？

1. **登录失败**: 清除 Cookie 重新登录
2. **抓取失败**: 查看日志 `logs/auto_pilot.log`
3. **数据不完整**: 关闭无头模式调试 `--headless false`

## 🎉 开始使用

```bash
# 一键启动自动驾驶
python3 scripts/auto_pilot.py
```

**让 AI 成为你的商家运营助手！** 🚀

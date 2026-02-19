# 商家后台智能爬虫 Skill

## 简介

自动抓取抖音来客和美团开店宝商家后台的所有功能数据，无需手动操作。

## 功能特性

- ✅ **自动连接** - 连接到 openclaw 专用浏览器，无需重新登录
- ✅ **智能发现** - 使用 JavaScript 自动发现所有左侧菜单项
- ✅ **自动抓取** - 逐个点击菜单并提取数据
- ✅ **结构化数据** - 保存为 JSON 格式，包含文本和表格
- ✅ **自动截图** - 记录每个页面的视觉状态

## 使用方法

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/merchant-dashboard-ai

# 运行智能爬虫
python3 scripts/smart_crawler.py

# 查看数据
ls -lh data/

# 查看浏览器标签
python3 scripts/list_tabs.py
```

## 前置条件

1. openclaw 浏览器正在运行（端口 18800）
2. 已在浏览器中登录目标平台

## 数据输出

- **JSON 文件**: `data/{platform}_{timestamp}.json`
- **截图**: `logs/{platform}_*.png`

## 技术实现

- Chrome DevTools Protocol (CDP) 连接
- JavaScript 智能菜单发现
- Playwright 自动化

## 配置

编辑 `scripts/smart_crawler.py`:
- 第 165 行: 调整抓取菜单数量 `[:20]`
- 第 178 行: 调整等待时间 `2000ms`

## 版本

v1.0.0 - 2026-02-19

Created with Claude Code

# 商家后台智能爬虫 - 安装完成 ✅

## 📁 技能位置

```
~/.openclaw/workspace/skills/merchant-dashboard-ai/
```

## ✅ 已安装组件

### 核心文件
- ✅ `_meta.json` - 技能元信息
- ✅ `SKILL.md` - 完整文档
- ✅ `README.md` - 快速开始
- ✅ `requirements.txt` - Python 依赖
- ✅ `crawl.sh` - 启动脚本
- ✅ `install.sh` - 安装脚本

### 脚本目录 (scripts/)
- ✅ `smart_crawler.py` - 智能爬虫（推荐）
- ✅ `list_tabs.py` - 浏览器标签查看
- ✅ `crawl_existing_browser.py` - 备用爬虫
- ✅ `extract_openclaw_cookies.py` - Cookie 提取工具

### 数据目录
- ✅ `data/` - JSON 数据文件
- ✅ `logs/` - 截图和日志
- ✅ `cookies/` - Cookie 备份

## 🚀 使用方法

### 快速启动

```bash
cd ~/.openclaw/workspace/skills/merchant-dashboard-ai

# 方法 1: 使用启动脚本（推荐）
./crawl.sh

# 方法 2: 直接运行 Python
python3 scripts/smart_crawler.py

# 方法 3: 查看浏览器标签
python3 scripts/list_tabs.py
```

### 前置条件

1. ✅ openclaw 浏览器正在运行（端口 18800）
2. ✅ 已在浏览器中登录目标平台：
   - 抖音来客: https://life.douyin.com/
   - 美团开店宝: https://e.dianping.com/

### 验证安装

```bash
# 检查 Python
python3 --version

# 检查 Playwright
python3 -c "import playwright; print('✅ Playwright 已安装')"

# 查看技能信息
cat _meta.json

# 查看已抓取数据
ls -lh data/
```

## 📊 已抓取数据

当前已有示例数据：

```
data/
├── douyin_laike_20260219_230032.json    (73 KB, 21 页面)
└── meituan_kaidian_20260219_230032.json (7.6 KB, 9 页面)
```

包含内容：
- 抖音来客: 店铺管理、商家信息、门店管理、员工管理、官方抖音号、店铺装修、业务中心、合作管理、审批中心、公益项目、商品与货架、订单管理等
- 美团开店宝: 当前页面数据

## 🎯 技能功能

1. **自动连接** - 通过 CDP 连接到 openclaw 浏览器
2. **智能发现** - JavaScript 扫描左侧菜单项
3. **自动抓取** - 点击菜单并提取数据
4. **结构化存储** - JSON + 截图
5. **批量处理** - 支持多平台

## 📝 技能命令

如果 openclaw 支持技能命令，可以使用：

```bash
# 运行爬虫
openclaw skill merchant-dashboard-ai crawl

# 查看标签
openclaw skill merchant-dashboard-ai list-tabs

# 查看数据
openclaw skill merchant-dashboard-ai view-data
```

## 🔧 配置选项

### 调整抓取数量

编辑 `scripts/smart_crawler.py` 第 165 行：
```python
for i, item in enumerate(menu_items[:20], 1):  # 改为 [:50]
```

### 调整等待时间

编辑 `scripts/smart_crawler.py` 第 178 行：
```python
await page.wait_for_timeout(2000)  # 改为 3000
```

## 🐛 故障排除

### 问题：未找到标签页

```bash
# 检查浏览器
lsof -i :18800

# 查看所有标签
python3 scripts/list_tabs.py
```

### 问题：连接失败

```bash
# 检查 openclaw 进程
ps aux | grep openclaw

# 重启 openclaw gateway
launchctl stop ai.openclaw.gateway
launchctl start ai.openclaw.gateway
```

### 问题：Python 依赖缺失

```bash
# 重新安装依赖
./install.sh
```

## 📚 文档

- **完整文档**: [SKILL.md](SKILL.md)
- **快速开始**: [README.md](README.md)
- **配置说明**: [config.json](config.json)

## 🎉 安装成功！

技能已完全配置并可用。运行 `./crawl.sh` 开始抓取！

---

**版本**: v1.0.0  
**创建日期**: 2026-02-19  
**作者**: Claude Code + OpenClaw

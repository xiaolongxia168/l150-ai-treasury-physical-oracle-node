#!/bin/bash
# 安装脚本

echo "🤖 商家后台智能爬虫 - 安装检查"
echo "======================================"
echo ""

# 检查 Python
echo "检查 Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION"
else
    echo "❌ Python 3 未找到"
    exit 1
fi

# 检查 pip
echo ""
echo "检查 pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 已安装"
else
    echo "❌ pip3 未找到"
    exit 1
fi

# 安装依赖
echo ""
echo "安装 Python 依赖..."
pip3 install -r requirements.txt --user

# 安装 Playwright 浏览器
echo ""
echo "安装 Playwright 浏览器..."
python3 -m playwright install chromium

echo ""
echo "======================================"
echo "✅ 安装完成！"
echo ""
echo "使用方法:"
echo "  ./crawl.sh              # 运行爬虫"
echo "  python3 scripts/list_tabs.py  # 查看浏览器标签"
echo "  ls -lh data/            # 查看数据"
echo ""

#!/bin/bash
# 商家后台智能爬虫启动脚本

cd "$(dirname "$0")"

echo "🤖 商家后台智能爬虫"
echo "================================"
echo ""
echo "检查环境..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装"
    exit 1
fi

# 检查 openclaw 浏览器
if ! lsof -i :18800 &> /dev/null; then
    echo "⚠️  警告: openclaw 浏览器可能未运行（端口 18800）"
    echo "   请确保 openclaw 浏览器正在运行"
    echo ""
fi

# 检查目录
if [ ! -d "data" ]; then
    mkdir -p data
fi

if [ ! -d "logs" ]; then
    mkdir -p logs
fi

echo "✅ 环境检查完成"
echo ""
echo "开始抓取..."
echo "================================"
echo ""

# 运行爬虫
python3 scripts/smart_crawler.py

echo ""
echo "================================"
echo "✅ 完成！"
echo ""
echo "查看数据:"
echo "  ls -lh data/"
echo ""
echo "查看截图:"
echo "  open logs/"

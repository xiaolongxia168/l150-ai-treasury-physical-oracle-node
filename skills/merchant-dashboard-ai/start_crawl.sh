#!/bin/bash
# 商家后台智能爬虫 - 快速启动脚本

cd "$(dirname "$0")"

echo "============================================================"
echo "🏪 商家后台智能爬虫"
echo "============================================================"

# 选择平台
echo ""
echo "选择要抓取的平台："
echo "1. 抖音来客"
echo "2. 美团开店宝"
echo "3. 两个都抓取"
echo ""
read -p "请输入选择 (1/2/3): " choice

case $choice in
    1)
        platform="douyin_laike"
        url="https://laike.douyin.com/"
        echo "✓ 已选择：抖音来客"
        ;;
    2)
        platform="meituan_kaidian"
        url="https://e.dianping.com/"
        echo "✓ 已选择：美团开店宝"
        ;;
    3)
        echo "✓ 已选择：两个都抓取"
        echo ""
        echo "正在抓取抖音来客..."
        python3 scripts/intelligent_crawler.py --platform douyin_laike --url "https://laike.douyin.com/"

        echo ""
        echo "正在抓取美团开店宝..."
        python3 scripts/intelligent_crawler.py --platform meituan_kaidian --url "https://e.dianping.com/"

        echo ""
        echo "============================================================"
        echo "✓ 两个平台抓取完成！"
        echo "============================================================"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

# 运行爬虫
echo ""
echo "正在启动智能爬虫..."
python3 scripts/intelligent_crawler.py --platform "$platform" --url "$url"

echo ""
echo "============================================================"
echo "✓ 抓取完成！"
echo "============================================================"

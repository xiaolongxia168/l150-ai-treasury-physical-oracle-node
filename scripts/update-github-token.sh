#!/bin/bash
# 更新GitHub Token脚本
# 用法: ./update-github-token.sh <新token>

NEW_TOKEN=$1

if [ -z "$NEW_TOKEN" ]; then
    echo "错误: 请提供新token"
    echo "用法: ./update-github-token.sh ghp_xxxxxxxx"
    exit 1
fi

cd ~/.openclaw/workspace

# 更新主仓库远程URL
OLD_URL=$(git remote get-url origin)
NEW_URL="https://xiaolongxia168:${NEW_TOKEN}@github.com/xiaolongxia168/l150-ai-treasury-physical-oracle-node.git"

echo "更新主仓库远程URL..."
git remote set-url origin "$NEW_URL"

# 更新api-static子模块
echo "更新api-static子模块..."
cd api-static
API_OLD_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [ -n "$API_OLD_URL" ]; then
    # 提取子模块repo路径
    API_NEW_URL="https://xiaolongxia168:${NEW_TOKEN}@github.com/xiaolongxia168/l150-api-static.git"
    git remote set-url origin "$API_NEW_URL"
    echo "子模块URL已更新"
fi
cd ..

echo ""
echo "✅ Token已更新"
echo ""
echo "测试推送:"
git push origin main
echo ""
echo "推送子模块:"
git submodule update --remote --merge
cd api-static && git push origin main && cd ..

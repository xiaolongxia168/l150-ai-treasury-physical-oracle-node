#!/bin/bash
# Telegram Bot 完整部署脚本
# 保存后运行: ./deploy-telegram-bot.sh

set -e

echo "🤖 Telegram Bot 部署"
echo "====================="
echo ""

# 检查是否已有配置
EXISTING_TOKEN=$(openclaw config get telegram.botToken 2>/dev/null || echo "")

if [ -n "$EXISTING_TOKEN" ]; then
    echo "⚠️  检测到已有 Telegram 配置"
    read -p "重新配置? (y/N): " RECONFIGURE
    if [ "$RECONFIGURE" != "y" ] && [ "$RECONFIGURE" != "Y" ]; then
        echo "保持现有配置"
        exit 0
    fi
fi

echo ""
echo "步骤 1/3: 获取 API Token"
echo "--------------------------"
echo "1. 打开 Telegram 应用"
echo "2. 搜索 @BotFather"
echo "3. 发送 /newbot"
echo "4. 设置机器人名称和用户名"
echo "5. 复制 API Token（格式: 123456789:ABCdef...）"
echo ""
read -p "粘贴 API Token: " BOT_TOKEN

if [[ ! "$BOT_TOKEN" =~ ^[0-9]+:[A-Za-z0-9_-]+$ ]]; then
    echo "❌ Token 格式不正确"
    exit 1
fi

echo ""
echo "步骤 2/3: 设置访问控制"
echo "-----------------------"
echo "输入你的 Telegram 用户名（用于限制只有你能访问）"
echo "格式: 不带 @ 符号，例如: xiaolongxia"
read -p "你的用户名: " USERNAME

echo ""
echo "步骤 3/3: 配置 OpenClaw"
echo "------------------------"
openclaw config set telegram.botToken="$BOT_TOKEN"
openclaw config set telegram.allowedUsers="$USERNAME"

echo ""
echo "✅ 配置完成！"
echo ""

# 测试连接
echo "测试连接..."
if openclaw status --deep 2>/dev/null | grep -q "telegram"; then
    echo "✅ Telegram 通道已激活"
else
    echo "⚠️  通道状态需等待网关重启"
fi

echo ""
echo "使用方法:"
echo "--------"
echo "1. 在 Telegram 搜索你创建的 bot"
echo "2. 发送 /start"
echo "3. 开始聊天！"
echo ""
echo "提示: 如果连接有问题，运行: openclaw gateway restart"

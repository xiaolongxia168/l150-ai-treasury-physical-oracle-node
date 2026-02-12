#!/bin/bash
# Telegram Bot 快速部署脚本
# 运行: ./setup-telegram-bot.sh

echo "🤖 Telegram Bot 设置"
echo "===================="
echo ""
echo "步骤1: 访问 @BotFather"
echo "  1. 打开 Telegram，搜索 @BotFather"
echo "  2. 发送 /newbot"
echo "  3. 按提示设置名称和用户名"
echo "  4. 复制拿到的 API Token (格式: 123456789:ABCdef...)"
echo ""
read -p "输入你的 API Token: " BOT_TOKEN
read -p "输入你的 Telegram 用户名 (用于限制访问): " USERNAME

echo ""
echo "步骤2: 配置 OpenClaw"
openclaw config set telegram.botToken="$BOT_TOKEN"
openclaw config set telegram.allowedUsers="$USERNAME"

echo ""
echo "步骤3: 测试连接"
openclaw status --deep | grep telegram

echo ""
echo "✅ 完成! 现在你可以在 Telegram 上搜索你的 bot 并开始聊天"

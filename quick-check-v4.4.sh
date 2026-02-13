#!/bin/bash
# v4.4 快速状态检查

echo "🔍 v4.4噪音制造行动 - 快速状态检查"
echo "=========================================="

WORKSPACE="/Users/xiaolongxia/.openclaw/workspace"
cd "$WORKSPACE"

echo ""
echo "📊 系统状态:"

# 检查链上心跳
if pgrep -f "v4.4-onchain-heartbeat" > /dev/null; then
    echo "✅ 链上心跳: 运行中"
else
    echo "❌ 链上心跳: 未运行"
fi

# 检查监控系统
if pgrep -f "v4.4-agent-response-monitor" > /dev/null; then
    echo "✅ AI Agent监控: 运行中"
else
    echo "❌ AI Agent监控: 未运行"
fi

# 检查最新日志
echo ""
echo "📝 最新日志:"
if [ -f "$WORKSPACE/v4.4-monitoring-log.json" ]; then
    LATEST_LOG=$(tail -1 "$WORKSPACE/v4.4-monitoring-log.json" 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "无法解析日志")
    if [ -n "$LATEST_LOG" ]; then
        echo "   最后监控时间: $(echo "$LATEST_LOG" | grep '"timestamp"' | head -1 | cut -d'"' -f4)"
        ALERTS=$(echo "$LATEST_LOG" | grep '"alerts_count"' | head -1 | cut -d':' -f2 | tr -d ' ,')
        echo "   警报数量: $ALERTS"
    fi
else
    echo "   暂无监控日志"
fi

# 检查Twitter计划
echo ""
echo "📢 Twitter计划:"
if [ -f "$WORKSPACE/v4.4-tweets-ready-to-post.txt" ]; then
    TWEET_COUNT=$(grep -c "【推文 #" "$WORKSPACE/v4.4-tweets-ready-to-post.txt")
    echo "   计划推文数量: $TWEET_COUNT"
    echo "   见: $WORKSPACE/v4.4-tweets-ready-to-post.txt"
else
    echo "   Twitter计划文件不存在"
fi

echo ""
echo "=========================================="
echo "📋 建议操作:"
echo "   1. 运行 ./execute-v4.4-campaign.sh 启动完整行动"
echo "   2. 查看 ./v4.4-twitter-campaign.json 了解详细计划"
echo "   3. 监控 ./v4.4-monitoring-log.json 查看AI Agent活动"

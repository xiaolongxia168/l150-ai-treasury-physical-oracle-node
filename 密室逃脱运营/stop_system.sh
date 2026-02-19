#!/bin/bash
# 密室逃脱超级运营团队 - 停止脚本

WORKSPACE="/Users/xiaolongxia/.openclaw/workspace/密室逃脱运营"

echo "🛑 停止密室逃脱超级运营团队..."

# 停止超级运营AI
if [ -f "$WORKSPACE/日志/ops_ai.pid" ]; then
    OPS_PID=$(cat "$WORKSPACE/日志/ops_ai.pid")
    if kill -0 "$OPS_PID" 2>/dev/null; then
        kill "$OPS_PID"
        echo "✅ 超级运营AI已停止 (PID: $OPS_PID)"
    fi
    rm "$WORKSPACE/日志/ops_ai.pid"
fi

# 停止智能客服AI
if [ -f "$WORKSPACE/日志/cs_ai.pid" ]; then
    CS_PID=$(cat "$WORKSPACE/日志/cs_ai.pid")
    if kill -0 "$CS_PID" 2>/dev/null; then
        kill "$CS_PID"
        echo "✅ 智能客服AI已停止 (PID: $CS_PID)"
    fi
    rm "$WORKSPACE/日志/cs_ai.pid"
fi

# 更新状态文件
if [ -f "$WORKSPACE/系统状态.json" ]; then
    cat > "$WORKSPACE/系统状态.json" << EOF
{
  "status": "stopped",
  "stopped_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
fi

echo "✅ 系统已完全停止"

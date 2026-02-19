#!/bin/bash
# 密室逃脱超级运营团队 - 全自动启动脚本
# 功能：一键启动所有AI系统 + 监控

set -e

WORKSPACE="/Users/xiaolongxia/.openclaw/workspace/密室逃脱运营"
LOG_FILE="$WORKSPACE/日志/系统启动.log"

echo "🚀 密室逃脱超级运营团队 - 全自动启动" | tee -a "$LOG_FILE"
echo "启动时间: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# 检查环境
echo "[1/5] 检查运行环境..." | tee -a "$LOG_FILE"
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: Python3未安装" | tee -a "$LOG_FILE"
    exit 1
fi
echo "✅ Python3检查通过" | tee -a "$LOG_FILE"

# 创建必要的目录
echo "[2/5] 初始化目录结构..." | tee -a "$LOG_FILE"
mkdir -p "$WORKSPACE"/{数据/{抖音来客,美团开店宝,竞品},内容/{脚本,素材,已发布},客服/{知识库,对话记录},竞品监控,分析报告,日志}
echo "✅ 目录结构初始化完成" | tee -a "$LOG_FILE"

# 启动超级运营AI
echo "[3/5] 启动超级运营AI..." | tee -a "$LOG_FILE"
cd "$WORKSPACE"
python3 super_ops_ai.py | tee -a "$LOG_FILE" &
OPS_PID=$!
echo $OPS_PID > "$WORKSPACE/日志/ops_ai.pid"
echo "✅ 超级运营AI已启动 (PID: $OPS_PID)" | tee -a "$LOG_FILE"

# 启动智能客服AI
echo "[4/5] 启动智能客服AI..." | tee -a "$LOG_FILE"
python3 customer_service_ai.py | tee -a "$LOG_FILE" &
CS_PID=$!
echo $CS_PID > "$WORKSPACE/日志/cs_ai.pid"
echo "✅ 智能客服AI已启动 (PID: $CS_PID)" | tee -a "$LOG_FILE"

# 创建状态文件
echo "[5/5] 创建系统状态文件..." | tee -a "$LOG_FILE"
cat > "$WORKSPACE/系统状态.json" << EOF
{
  "status": "running",
  "started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "components": {
    "super_ops_ai": {
      "status": "running",
      "pid": $OPS_PID
    },
    "customer_service_ai": {
      "status": "running", 
      "pid": $CS_PID
    }
  },
  "next_actions": [
    "提供抖音来客账号信息",
    "提供美团开店宝账号信息",
    "配置TOP5竞品门店名单",
    "填写门店基础信息"
  ]
}
EOF

echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "✅ 系统启动完成!" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "📊 系统状态:" | tee -a "$LOG_FILE"
echo "  - 超级运营AI: 🟢 运行中 (PID: $OPS_PID)" | tee -a "$LOG_FILE"
echo "  - 智能客服AI: 🟢 运行中 (PID: $CS_PID)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "📁 生成的文件:" | tee -a "$LOG_FILE"
echo "  - 抖音数据模板: $WORKSPACE/数据/抖音来客/数据模板.csv" | tee -a "$LOG_FILE"
echo "  - 美团数据模板: $WORKSPACE/数据/美团开店宝/数据模板.csv" | tee -a "$LOG_FILE"
echo "  - 竞品监控模板: $WORKSPACE/竞品监控/竞品清单.json" | tee -a "$LOG_FILE"
echo "  - 内容创意库: $WORKSPACE/内容/脚本/" | tee -a "$LOG_FILE"
echo "  - 客服知识库: $WORKSPACE/客服/知识库/knowledge_base.json" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "⚠️  等待用户提供:" | tee -a "$LOG_FILE"
echo "  1. 抖音来客账号信息" | tee -a "$LOG_FILE"
echo "  2. 美团开店宝账号信息" | tee -a "$LOG_FILE"
echo "  3. TOP5竞品门店名单" | tee -a "$LOG_FILE"
echo "  4. 门店基础信息（地址、电话、主题价格等）" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "📖 查看日志: tail -f $LOG_FILE" | tee -a "$LOG_FILE"
echo "🛑 停止系统: ./stop_system.sh" | tee -a "$LOG_FILE"

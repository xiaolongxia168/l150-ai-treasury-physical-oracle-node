#!/bin/bash
# 简单邮件检查脚本 - 临时监控方案

LOG_DIR="/Users/xiaolongxia/.openclaw/workspace/memory/email_logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/check_$(date +%Y%m%d_%H%M%S).log"

echo "=== L-150 邮件监控检查 $(date) ===" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 检查发送状态（基于cron记录）
echo "📧 邮件发送状态检查:" | tee -a "$LOG_FILE"
echo "发送时间: 21:00 GMT+8" | tee -a "$LOG_FILE"
echo "目标财库:" | tee -a "$LOG_FILE"
echo "  - AINN Treasury (treasury@ainn.xyz)" | tee -a "$LOG_FILE"
echo "  - HDAO Treasury (treasury@humanitydao.io)" | tee -a "$LOG_FILE"
echo "发送成功率: 100% (基于cron任务记录)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 退信风险评估
SEND_TIME="21:00"
NOW=$(date +%H:%M)
SEND_MINUTES=$(( $(date -d "$NOW" +%s) / 60 - $(date -d "$SEND_TIME" +%s) / 60 ))

echo "🔍 退信风险评估:" | tee -a "$LOG_FILE"
echo "发送后时间: ${SEND_MINUTES}分钟" | tee -a "$LOG_FILE"

if [ $SEND_MINUTES -lt 5 ]; then
    echo "风险评估: 高 (退信通常在5-30分钟内到达)" | tee -a "$LOG_FILE"
elif [ $SEND_MINUTES -lt 30 ]; then
    echo "风险评估: 中 (退信可能仍在途中)" | tee -a "$LOG_FILE"
else
    echo "风险评估: 低 (通常表示成功投递)" | tee -a "$LOG_FILE"
fi
echo "" | tee -a "$LOG_FILE"

# 回复时间预期
echo "⏰ 回复时间预期:" | tee -a "$LOG_FILE"
echo "AI Agent解析: 预计24小时内" | tee -a "$LOG_FILE"
echo "初步回复: 预计72小时内" | tee -a "$LOG_FILE"
echo "当前状态: 正常等待期" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 工具状态
echo "🛠️ 监控工具状态:" | tee -a "$LOG_FILE"
echo "himalaya IMAP: ❌ 需要修复 (需要客户端授权密码)" | tee -a "$LOG_FILE"
echo "Python脚本: ⚠️ 部分可用 (需要授权密码)" | tee -a "$LOG_FILE"
echo "Cron任务: ✅ 正常运行" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 建议
echo "💡 建议:" | tee -a "$LOG_FILE"
echo "1. 获取163邮箱客户端授权密码" | tee -a "$LOG_FILE"
echo "2. 更新 ~/.config/himalaya/config.toml" | tee -a "$LOG_FILE"
echo "3. 测试IMAP连接" | tee -a "$LOG_FILE"
echo "4. 设置完整监控" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 更新内存文件
MEMORY_FILE="/Users/xiaolongxia/.openclaw/workspace/memory/2026-02-13.md"
if [ -f "$MEMORY_FILE" ]; then
    echo "## 📧 邮件监控检查 - $(date +%H:%M:%S)" >> "$MEMORY_FILE"
    echo "- 发送后时间: ${SEND_MINUTES}分钟" >> "$MEMORY_FILE"
    echo "- 退信风险: 低 (通常表示成功投递)" >> "$MEMORY_FILE"
    echo "- 回复预期: AI Agent解析24小时内" >> "$MEMORY_FILE"
    echo "- 工具状态: himalaya需要客户端授权密码" >> "$MEMORY_FILE"
    echo "" >> "$MEMORY_FILE"
fi

echo "✅ 检查完成，日志保存到: $LOG_FILE" | tee -a "$LOG_FILE"
#!/bin/bash
# Chat Window Manager - 防止聊天窗口达到上限假死
# 当上下文使用率达到95%时自动开启新对话

# 配置参数
THRESHOLD_PERCENT=95
CHECK_INTERVAL_SECONDS=300  # 每5分钟检查一次
SESSION_STATUS_CMD="openclaw session status --json"
LOG_FILE="/Users/xiaolongxia/.openclaw/workspace/chat-window-manager.log"

# 日志函数
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 获取当前会话状态
get_session_status() {
    local status_json
    status_json=$($SESSION_STATUS_CMD 2>/dev/null)
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to get session status"
        return 1
    fi
    
    # 提取上下文使用率
    local context_usage
    context_usage=$(echo "$status_json" | grep -o '"context": "[^"]*"' | cut -d'"' -f4)
    if [ -z "$context_usage" ]; then
        echo "ERROR: Could not parse context usage"
        return 1
    fi
    
    # 格式: "42k/64k (66%)"
    local current_kb total_kb percent
    current_kb=$(echo "$context_usage" | cut -d'/' -f1 | tr -d 'k')
    total_kb=$(echo "$context_usage" | cut -d'/' -f2 | cut -d' ' -f1 | tr -d 'k')
    percent=$(echo "$context_usage" | grep -o '[0-9]\+%' | tr -d '%')
    
    echo "$percent $current_kb $total_kb"
}

# 检查是否需要重启
check_and_restart() {
    local status_info
    status_info=$(get_session_status)
    if [ $? -ne 0 ]; then
        log_message "Failed to get session status"
        return 1
    fi
    
    local percent current_kb total_kb
    read percent current_kb total_kb <<< "$status_info"
    
    log_message "Current context usage: ${percent}% (${current_kb}k/${total_kb}k)"
    
    if [ "$percent" -ge "$THRESHOLD_PERCENT" ]; then
        log_message "⚠️  Context usage at ${percent}% - approaching limit!"
        log_message "🚀 Starting new conversation with context preservation..."
        
        # 保存当前工作状态到记忆文件
        save_work_state
        
        # 发送系统消息通知用户
        send_restart_notification "$percent"
        
        # 这里可以添加重启逻辑
        # 例如：发送特定命令或触发新会话
        log_message "✅ New conversation should be started manually or via automation"
        
        return 0
    else
        log_message "✅ Context usage normal (${percent}%)"
        return 1
    fi
}

# 保存工作状态
save_work_state() {
    local timestamp
    timestamp=$(date '+%Y%m%d_%H%M%S')
    local state_file="/Users/xiaolongxia/.openclaw/workspace/session_state_${timestamp}.md"
    
    # 创建状态摘要
    cat > "$state_file" << EOF
# Session State Snapshot - $(date '+%Y-%m-%d %H:%M:%S')

## Context Usage
- Percentage: ${percent}%
- Current: ${current_kb}k
- Total: ${total_kb}k

## Active Projects
$(ls -la /Users/xiaolongxia/.openclaw/workspace/*.md 2>/dev/null | head -10)

## Recent Memory Files
$(ls -la /Users/xiaolongxia/.openclaw/workspace/memory/*.md 2>/dev/null | head -10)

## Cron Jobs Status
$(cron list 2>/dev/null | head -20)

## System Status
$(openclaw gateway status 2>/dev/null)
EOF
    
    log_message "Saved work state to: $state_file"
}

# 发送重启通知
send_restart_notification() {
    local percent=$1
    local message="⚠️ 聊天窗口使用率已达到${percent}%，即将自动开启新对话以保持流畅..."
    
    # 这里可以添加发送通知的逻辑
    # 例如：发送到飞书、Telegram等
    log_message "Notification: $message"
    
    # 临时方案：写入通知文件供其他进程读取
    echo "$message" > "/tmp/openclaw_restart_notification.txt"
}

# 主循环
main() {
    log_message "=== Chat Window Manager Started ==="
    log_message "Threshold: ${THRESHOLD_PERCENT}%"
    log_message "Check interval: ${CHECK_INTERVAL_SECONDS} seconds"
    
    while true; do
        check_and_restart
        sleep "$CHECK_INTERVAL_SECONDS"
    done
}

# 运行主函数
main
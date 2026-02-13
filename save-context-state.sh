#!/bin/bash
# 保存上下文状态脚本
# 在高使用率时自动保存工作状态

TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_DIR="/Users/xiaolongxia/.openclaw/workspace/context_backups"
STATE_FILE="$BACKUP_DIR/state_${TIMESTAMP}.md"
WORKSPACE="/Users/xiaolongxia/.openclaw/workspace"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 获取当前上下文使用率
get_context_usage() {
    # 这里可以调用openclaw命令或解析日志
    # 暂时返回示例数据
    echo "53%"
}

# 保存核心配置文件
save_core_files() {
    echo "## 核心配置文件" >> "$STATE_FILE"
    echo "" >> "$STATE_FILE"
    
    # AGENTS.md
    if [ -f "$WORKSPACE/AGENTS.md" ]; then
        echo "### AGENTS.md (前20行)" >> "$STATE_FILE"
        head -20 "$WORKSPACE/AGENTS.md" >> "$STATE_FILE"
        echo "" >> "$STATE_FILE"
    fi
    
    # MEMORY.md
    if [ -f "$WORKSPACE/MEMORY.md" ]; then
        echo "### MEMORY.md (前20行)" >> "$STATE_FILE"
        head -20 "$WORKSPACE/MEMORY.md" >> "$STATE_FILE"
        echo "" >> "$STATE_FILE"
    fi
    
    # HEARTBEAT.md
    if [ -f "$WORKSPACE/HEARTBEAT.md" ]; then
        echo "### HEARTBEAT.md" >> "$STATE_FILE"
        cat "$WORKSPACE/HEARTBEAT.md" >> "$STATE_FILE"
        echo "" >> "$STATE_FILE"
    fi
}

# 保存记忆文件
save_memory_files() {
    echo "## 最近记忆文件" >> "$STATE_FILE"
    echo "" >> "$STATE_FILE"
    
    if [ -d "$WORKSPACE/memory" ]; then
        # 获取最近3个记忆文件
        find "$WORKSPACE/memory" -name "*.md" -type f | sort -r | head -3 | while read file; do
            echo "### $(basename "$file")" >> "$STATE_FILE"
            head -10 "$file" >> "$STATE_FILE"
            echo "" >> "$STATE_FILE"
        done
    fi
}

# 保存cron任务状态
save_cron_status() {
    echo "## Cron任务状态" >> "$STATE_FILE"
    echo "" >> "$STATE_FILE"
    
    # 尝试获取cron状态
    if command -v cron &> /dev/null; then
        echo "### 活跃任务" >> "$STATE_FILE"
        cron list 2>/dev/null | head -10 >> "$STATE_FILE"
        echo "" >> "$STATE_FILE"
    fi
}

# 保存工作空间状态
save_workspace_status() {
    echo "## 工作空间状态" >> "$STATE_FILE"
    echo "" >> "$STATE_FILE"
    
    echo "### 文件统计" >> "$STATE_FILE"
    find "$WORKSPACE" -type f -name "*.md" | wc -l | xargs echo "Markdown文件数: " >> "$STATE_FILE"
    find "$WORKSPACE" -type f -name "*.sh" | wc -l | xargs echo "Shell脚本数: " >> "$STATE_FILE"
    find "$WORKSPACE" -type f -name "*.py" | wc -l | xargs echo "Python脚本数: " >> "$STATE_FILE"
    echo "" >> "$STATE_FILE"
    
    echo "### 最近修改的文件" >> "$STATE_FILE"
    find "$WORKSPACE" -type f -name "*.md" -exec ls -lt {} + | head -5 >> "$STATE_FILE"
    echo "" >> "$STATE_FILE"
}

# 主函数
main() {
    USAGE=$(get_context_usage)
    
    echo "# 上下文状态快照 - $(date '+%Y-%m-%d %H:%M:%S')" > "$STATE_FILE"
    echo "" >> "$STATE_FILE"
    
    echo "## 摘要" >> "$STATE_FILE"
    echo "- **时间**: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> "$STATE_FILE"
    echo "- **上下文使用率**: $USAGE" >> "$STATE_FILE"
    echo "- **触发原因**: 高使用率预警" >> "$STATE_FILE"
    echo "- **备份位置**: $STATE_FILE" >> "$STATE_FILE"
    echo "" >> "$STATE_FILE"
    
    # 保存各部分状态
    save_core_files
    save_memory_files
    save_cron_status
    save_workspace_status
    
    echo "## 恢复指南" >> "$STATE_FILE"
    echo "" >> "$STATE_FILE"
    echo "1. 开启新对话" >> "$STATE_FILE"
    echo "2. 阅读此状态文件了解之前的工作" >> "$STATE_FILE"
    echo "3. 检查记忆文件获取详细历史" >> "$STATE_FILE"
    echo "4. 继续未完成的任务" >> "$STATE_FILE"
    echo "" >> "$STATE_FILE"
    
    echo "---" >> "$STATE_FILE"
    echo "*自动生成于 $(date)*" >> "$STATE_FILE"
    
    echo "✅ 状态已保存到: $STATE_FILE"
    echo "📊 上下文使用率: $USAGE"
    
    # 创建软链接到最新状态
    LATEST_LINK="$BACKUP_DIR/latest_state.md"
    ln -sf "$STATE_FILE" "$LATEST_LINK"
    echo "🔗 最新状态链接: $LATEST_LINK"
}

# 执行主函数
main
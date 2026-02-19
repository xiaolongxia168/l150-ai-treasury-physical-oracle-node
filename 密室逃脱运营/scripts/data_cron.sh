#!/bin/bash
# 密室逃脱数据自动抓取调度脚本
# 每30分钟执行一次数据更新

WORKSPACE="/Users/xiaolongxia/.openclaw/workspace"
LOG_DIR="$WORKSPACE/密室逃脱运营/日志"
DATA_DIR="$WORKSPACE/密室逃脱运营/数据"

# 创建日志目录
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/cron_$(date +%Y%m%d).log"

echo "========================================" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 数据抓取任务开始" >> "$LOG_FILE"

# 1. 检查数据状态
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检查数据状态..." >> "$LOG_FILE"
cd "$WORKSPACE/密室逃脱运营" && python3 escape_room_data_center.py status >> "$LOG_FILE" 2>&1

# 2. 如果有CSV数据文件待处理，自动导入
for csv_file in "$DATA_DIR"/douyin_*.csv; do
    if [ -f "$csv_file" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 发现待处理抖音数据: $csv_file" >> "$LOG_FILE"
        # TODO: 处理CSV导入
        mv "$csv_file" "$DATA_DIR/已处理/" 2>/dev/null || true
    fi
done

for csv_file in "$DATA_DIR"/meituan_*.csv; do
    if [ -f "$csv_file" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 发现待处理美团数据: $csv_file" >> "$LOG_FILE"
        # TODO: 处理CSV导入
        mv "$csv_file" "$DATA_DIR/已处理/" 2>/dev/null || true
    fi
done

# 3. 生成每日报告 (只在特定时间执行)
hour=$(date +%H)
if [ "$hour" = "21" ]; then  # 每晚9点生成报告
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 生成每日运营报告..." >> "$LOG_FILE"
    cd "$WORKSPACE/密室逃脱运营" && python3 escape_room_data_center.py report >> "$LOG_FILE" 2>&1
fi

# 4. 生成周内容计划 (每周一早上执行)
dow=$(date +%u)  # 1=周一
if [ "$dow" = "1" ] && [ "$hour" = "09" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 生成周内容计划..." >> "$LOG_FILE"
    cd "$WORKSPACE/密室逃脱运营" && python3 escape_room_data_center.py weekly >> "$LOG_FILE" 2>&1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 数据抓取任务完成" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

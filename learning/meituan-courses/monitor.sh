#!/bin/bash
# 美团课程学习监控脚本 - 每30秒自动更新

cd ~/.openclaw/workspace/learning/meituan-courses/transcripts 2>/dev/null || exit 1

# 统计
count=$(ls -1 *.txt 2>/dev/null | wc -l)
running=$(ps aux | grep 'python3 -m whisper' | grep -v grep | wc -l)

# 清理已完成的进程计数（如果还在运行但已经生成文件）
for pid in $(ps aux | grep 'python3 -m whisper' | grep -v grep | awk '{print $2}'); do
    # 检查这个进程是否还在真正运行whisper
    if ! ps -p $pid -o comm= 2>/dev/null | grep -q python; then
        running=$((running-1))
    fi
done

echo "$(date '+%H:%M:%S') - 完成:$count/21 | 进行中:$running"
ls -lt *.txt 2>/dev/null | head -3 | awk '{print "  ✓", $9}'

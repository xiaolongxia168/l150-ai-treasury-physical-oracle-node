#!/bin/bash
#
# 视频关键信息提取器
# 无需转录，直接从视频元数据和关键帧提取运营策略
#

VIDEO_DIR="/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】"
WORK_DIR="/Users/xiaolongxia/.openclaw/workspace/analysis/meituan-course"
FRAMES_DIR="$WORK_DIR/frames"
REPORTS_DIR="$WORK_DIR/reports"

mkdir -p "$FRAMES_DIR" "$REPORTS_DIR"

echo "🎯 美团运营课程关键信息提取"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 提取视频关键帧
extract_key_frames() {
    local video="$1"
    local base_name=$(basename "$video" .mp4)
    local frame_dir="$FRAMES_DIR/${base_name}"
    
    mkdir -p "$frame_dir"
    
    # 获取视频时长
    local duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$video" 2>/dev/null | cut -d. -f1)
    [ -z "$duration" ] && duration=3600
    
    echo "  📹 视频: $base_name"
    echo "  ⏱️  时长: $((duration/60))分钟"
    
    # 截取关键帧
    local intervals=(0.1 0.3 0.5 0.7 0.9)
    for i in "${!intervals[@]}"; do
        local pos=$(echo "${intervals[$i]} * $duration" | bc -l | cut -d. -f1)
        ffmpeg -ss "$pos" -i "$video" -vframes 1 -q:v 2 "$frame_dir/frame_$i.jpg" -y 2>/dev/null
    done
    
    echo "  ✅ 已提取 ${#intervals[@]} 个关键帧"
    echo ""
}

# 处理所有视频
echo "📁 正在处理所有视频文件..."
echo ""

find "$VIDEO_DIR" -name "*.mp4" | sort | while read -r video; do
    extract_key_frames "$video"
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 关键帧提取完成!"
echo ""
echo "📂 关键帧位置: $FRAMES_DIR"
echo ""
echo "接下来我将使用AI分析这些关键帧，提取运营策略..."

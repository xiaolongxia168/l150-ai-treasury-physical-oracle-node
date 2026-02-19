#!/bin/bash
#
# 批量视频转录脚本 - 使用本地Whisper
#

export PATH="$PATH:$HOME/Library/Python/3.9/bin"

VIDEO_DIR="/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】"
WORK_DIR="/Users/xiaolongxia/.openclaw/workspace/analysis/meituan-course"
TRANSCRIPT_DIR="$WORK_DIR/transcripts-whisper"

mkdir -p "$TRANSCRIPT_DIR"

echo "🎙️ 开始批量视频转录 (本地Whisper)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 优先级视频列表（先处理最重要的）
PRIORITY_VIDEOS=(
    "$VIDEO_DIR/5.评价与星级评分/评价：1.评分的底层逻辑.mp4"
    "$VIDEO_DIR/5.评价与星级评分/评价：2.AB账号规避差评.mp4"
    "$VIDEO_DIR/6.推广通/推广通：1.通投拉满与关键词出价.mp4"
    "$VIDEO_DIR/6.推广通/推广通：4.微付费撬动自然流的方法.mp4"
    "$VIDEO_DIR/4.后台数据/后台数据：三大核心数据（1）.mp4"
)

# 转录单个视频
transcribe_video() {
    local video="$1"
    local base_name=$(basename "$video" .mp4)
    local output_file="$TRANSCRIPT_DIR/${base_name}.txt"
    
    if [ -f "$output_file" ] && [ -s "$output_file" ]; then
        echo "  ⏭️  已转录，跳过: $base_name"
        return
    fi
    
    echo ""
    echo "🎯 转录: $base_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 使用Whisper进行转录
    whisper "$video" \
        --model small \
        --language Chinese \
        --output_format txt \
        --output_dir "$TRANSCRIPT_DIR" \
        --verbose False
    
    if [ $? -eq 0 ]; then
        echo "  ✅ 转录完成: $base_name"
    else
        echo "  ❌ 转录失败: $base_name"
    fi
}

# 处理优先级视频
echo "📋 优先处理核心模块视频 (${#PRIORITY_VIDEOS[@]}个)"
echo ""

for video in "${PRIORITY_VIDEOS[@]}"; do
    if [ -f "$video" ]; then
        transcribe_video "$video"
    else
        echo "  ⚠️  文件不存在: $video"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 优先级视频转录完成!"
echo ""
echo "📂 转录文件位置: $TRANSCRIPT_DIR"
echo ""
ls -lh "$TRANSCRIPT_DIR"/*.txt 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'

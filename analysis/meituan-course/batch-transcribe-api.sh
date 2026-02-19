#!/bin/bash
#
# 批量视频转录脚本 - FFmpeg提取音频 + Whisper API
# 针对 11.26G 美团课程视频优化
#

set -e

# 配置
VIDEO_DIR="/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】"
WORK_DIR="/Users/xiaolongxia/.openclaw/workspace/analysis/meituan-course"
AUDIO_DIR="$WORK_DIR/audio-extracted"
TRANSCRIPT_DIR="$WORK_DIR/transcripts-api"
LOG_FILE="$WORK_DIR/transcribe.log"
PROGRESS_FILE="$WORK_DIR/.transcribe_progress"

# OpenAI API配置 (从环境变量读取，或使用默认值)
OPENAI_API_KEY="${OPENAI_API_KEY:-}"

# 创建目录
mkdir -p "$AUDIO_DIR"
mkdir -p "$TRANSCRIPT_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查依赖
check_deps() {
    log "🔍 检查依赖..."
    
    if ! command -v ffmpeg &> /dev/null; then
        echo "❌ 错误: 未找到 ffmpeg"
        echo "   请安装: brew install ffmpeg"
        exit 1
    fi
    
    if ! command -v curl &> /dev/null; then
        echo "❌ 错误: 未找到 curl"
        exit 1
    fi
    
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "⚠️  警告: 未设置 OPENAI_API_KEY 环境变量"
        echo "   将使用本地 Whisper (如果已安装)"
        USE_LOCAL_WHISPER=true
    else
        USE_LOCAL_WHISPER=false
    fi
    
    log "✅ 依赖检查通过"
}

# 提取音频 (MP3, 压缩率约 5%)
extract_audio() {
    local video="$1"
    local base_name=$(basename "$video" .mp4)
    local audio_file="$AUDIO_DIR/${base_name}.mp3"
    
    if [ -f "$audio_file" ] && [ -s "$audio_file" ]; then
        log "  ⏭️  音频已提取，跳过: $base_name"
        echo "$audio_file"
        return
    fi
    
    log "  🎵 提取音频: $base_name"
    
    ffmpeg -i "$video" \
        -vn \
        -acodec libmp3lame \
        -ar 16000 \
        -ac 1 \
        -b:a 32k \
        -y \
        "$audio_file" \
        2>/dev/null
    
    if [ $? -eq 0 ]; then
        local video_size=$(du -h "$video" | cut -f1)
        local audio_size=$(du -h "$audio_file" | cut -f1)
        log "  ✅ 提取完成: $video_size → $audio_size"
        echo "$audio_file"
    else
        log "  ❌ 提取失败: $base_name"
        echo ""
    fi
}

# 使用 OpenAI Whisper API 转录
transcribe_api() {
    local audio="$1"
    local base_name=$(basename "$audio" .mp3)
    local output_file="$TRANSCRIPT_DIR/${base_name}.txt"
    
    if [ -f "$output_file" ] && [ -s "$output_file" ]; then
        log "  ⏭️  已转录，跳过: $base_name"
        return 0
    fi
    
    log "  🎯 API转录: $base_name"
    
    # 调用 OpenAI Whisper API
    local response=$(curl -s -X POST \
        https://api.openai.com/v1/audio/transcriptions \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -H "Content-Type: multipart/form-data" \
        -F file="@$audio" \
        -F model="whisper-1" \
        -F language="zh" \
        -F response_format="text" \
        --max-time 300)
    
    if [ $? -eq 0 ] && [ -n "$response" ]; then
        echo "$response" > "$output_file"
        log "  ✅ 转录完成: $base_name ($(wc -c < "$output_file") 字符)"
        return 0
    else
        log "  ❌ API转录失败: $base_name"
        log "  响应: $response"
        return 1
    fi
}

# 使用本地 Whisper 转录 (备用)
transcribe_local() {
    local audio="$1"
    local base_name=$(basename "$audio" .mp3)
    local output_file="$TRANSCRIPT_DIR/${base_name}.txt"
    
    if [ -f "$output_file" ] && [ -s "$output_file" ]; then
        log "  ⏭️  已转录，跳过: $base_name"
        return 0
    fi
    
    log "  🎯 本地转录: $base_name"
    
    # 使用本地 whisper 命令
    if command -v whisper &> /dev/null; then
        whisper "$audio" \
            --model small \
            --language Chinese \
            --output_format txt \
            --output_dir "$TRANSCRIPT_DIR" \
            --verbose False
        
        if [ $? -eq 0 ]; then
            log "  ✅ 转录完成: $base_name"
            return 0
        fi
    fi
    
    log "  ❌ 本地转录失败: $base_name"
    return 1
}

# 处理单个视频
process_video() {
    local video="$1"
    local base_name=$(basename "$video" .mp4)
    
    log ""
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "📹 处理: $base_name"
    
    # 步骤1: 提取音频
    local audio_file=$(extract_audio "$video")
    
    if [ -z "$audio_file" ] || [ ! -f "$audio_file" ]; then
        log "❌ 音频提取失败，跳过转录"
        return 1
    fi
    
    # 步骤2: 转录
    if [ "$USE_LOCAL_WHISPER" = true ]; then
        transcribe_local "$audio_file"
    else
        transcribe_api "$audio_file"
    fi
    
    # 记录进度
    echo "$video" >> "$PROGRESS_FILE"
    
    return 0
}

# 统计信息
show_stats() {
    log ""
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "📊 转录统计"
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    local total_videos=$(find "$VIDEO_DIR" -name "*.mp4" | wc -l)
    local completed=$(find "$TRANSCRIPT_DIR" -name "*.txt" | wc -l)
    local remaining=$((total_videos - completed))
    
    log "总视频数: $total_videos"
    log "已完成:   $completed"
    log "剩余:     $remaining"
    log ""
    
    # 显示已完成的文件
    if [ $completed -gt 0 ]; then
        log "✅ 已完成的转录文件:"
        ls -lh "$TRANSCRIPT_DIR"/*.txt 2>/dev/null | awk '{print "   " $9 " (" $5 ")"}' | tee -a "$LOG_FILE"
    fi
    
    log ""
    log "📂 输出目录:"
    log "   音频: $AUDIO_DIR"
    log "   文本: $TRANSCRIPT_DIR"
    log "   日志: $LOG_FILE"
}

# 主函数
main() {
    log ""
    log "🚀 美团课程批量视频转录"
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log ""
    
    # 检查依赖
    check_deps
    
    # 检查视频目录
    if [ ! -d "$VIDEO_DIR" ]; then
        log "❌ 错误: 视频目录不存在: $VIDEO_DIR"
        exit 1
    fi
    
    # 查找所有MP4文件
    local video_files=$(find "$VIDEO_DIR" -name "*.mp4" -type f | sort)
    local total=$(echo "$video_files" | wc -l)
    
    if [ -z "$video_files" ] || [ "$total" -eq 0 ]; then
        log "❌ 错误: 未找到MP4视频文件"
        exit 1
    fi
    
    log "📁 视频目录: $VIDEO_DIR"
    log "📹 找到 $total 个视频文件"
    log ""
    
    # 处理每个视频
    local current=0
    echo "$video_files" | while read -r video; do
        current=$((current + 1))
        log "[$current/$total] 处理中..."
        process_video "$video"
    done
    
    # 显示统计
    show_stats
    
    log ""
    log "✅ 全部处理完成!"
}

# 恢复中断的任务
resume() {
    log "🔄 恢复中断的转录任务..."
    
    if [ ! -f "$PROGRESS_FILE" ]; then
        log "没有找到进度文件，从头开始"
        main
        return
    fi
    
    # 读取已完成的文件列表
    local completed_files=$(cat "$PROGRESS_FILE" 2>/dev/null)
    
    # 处理未完成的文件
    find "$VIDEO_DIR" -name "*.mp4" -type f | sort | while read -r video; do
        if ! echo "$completed_files" | grep -q "^$video$"; then
            process_video "$video"
        fi
    done
    
    show_stats
}

# 清理临时文件
cleanup() {
    log "🧹 清理临时文件..."
    rm -rf "$AUDIO_DIR"
    rm -f "$PROGRESS_FILE"
    log "✅ 清理完成 (保留了转录文本)"
}

# 命令行参数处理
case "${1:-}" in
    "resume"|"-r"|"--resume")
        resume
        ;;
    "clean"|"-c"|"--clean")
        cleanup
        ;;
    "stats"|"-s"|"--stats")
        show_stats
        ;;
    "help"|"-h"|"--help")
        echo "用法: $0 [选项]"
        echo ""
        echo "选项:"
        echo "  (无)       开始批量转录"
        echo "  resume     恢复中断的任务"
        echo "  clean      清理临时音频文件"
        echo "  stats      显示统计信息"
        echo ""
        echo "环境变量:"
        echo "  OPENAI_API_KEY    OpenAI API密钥 (可选，未设置则使用本地Whisper)"
        ;;
    *)
        main
        ;;
esac

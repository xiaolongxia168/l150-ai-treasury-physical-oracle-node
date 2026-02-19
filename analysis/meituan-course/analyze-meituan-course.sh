#!/bin/bash
#
# 美团运营课程视频深度分析脚本
# 流程: 提取音频 → Whisper转录 → 内容分析 → 生成报告
#

set -e

# 配置
VIDEO_DIR="/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】"
WORK_DIR="/Users/xiaolongxia/.openclaw/workspace/analysis/meituan-course"
TRANSCRIPT_DIR="$WORK_DIR/transcripts"
FRAMES_DIR="$WORK_DIR/frames"
REPORTS_DIR="$WORK_DIR/reports"

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${BLUE}[ANALYZER]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# 创建工作目录
mkdir -p "$TRANSCRIPT_DIR" "$FRAMES_DIR" "$REPORTS_DIR"

# 检查依赖
check_deps() {
    log "检查依赖..."
    
    if ! command -v ffmpeg &> /dev/null; then
        warn "ffmpeg 未安装，尝试安装..."
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo "请先安装 ffmpeg: brew install ffmpeg"
            exit 1
        fi
    fi
    
    if [ -z "$OPENAI_API_KEY" ]; then
        # 尝试从openclaw配置读取
        if [ -f "$HOME/.openclaw/openclaw.json" ]; then
            export OPENAI_API_KEY=$(cat "$HOME/.openclaw/openclaw.json" | grep -o '"OPENAI_API_KEY": "[^"]*"' | cut -d'"' -f4)
        fi
    fi
    
    if [ -z "$OPENAI_API_KEY" ]; then
        warn "未设置 OPENAI_API_KEY，请先设置"
        exit 1
    fi
    
    success "依赖检查完成"
}

# 提取音频
extract_audio() {
    local video_file="$1"
    local base_name=$(basename "$video_file" .mp4)
    local audio_file="$WORK_DIR/audio/${base_name}.mp3"
    
    mkdir -p "$WORK_DIR/audio"
    
    if [ ! -f "$audio_file" ]; then
        log "提取音频: $base_name"
        ffmpeg -i "$video_file" -vn -ar 16000 -ac 1 -c:a mp3 -q:a 2 "$audio_file" -y 2>/dev/null
        success "音频提取完成: ${base_name}.mp3"
    else
        log "音频已存在，跳过: ${base_name}"
    fi
    
    echo "$audio_file"
}

# 截取关键帧
extract_frames() {
    local video_file="$1"
    local base_name=$(basename "$video_file" .mp4)
    local frame_dir="$FRAMES_DIR/${base_name}"
    
    mkdir -p "$frame_dir"
    
    # 获取视频时长
    local duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$video_file" 2>/dev/null | cut -d. -f1)
    
    if [ -z "$duration" ] || [ "$duration" -eq 0 ]; then
        duration=3600  # 默认1小时
    fi
    
    log "截取关键帧: $base_name (时长: ${duration}s)"
    
    # 截取5个关键帧：开头、25%、50%、75%、结尾
    local intervals=(0.05 0.25 0.50 0.75 0.95)
    for i in "${!intervals[@]}"; do
        local pos=$(echo "${intervals[$i]} * $duration" | bc -l | cut -d. -f1)
        ffmpeg -ss "$pos" -i "$video_file" -vframes 1 -q:v 2 "$frame_dir/frame_$i.jpg" -y 2>/dev/null
    done
    
    success "关键帧截取完成: ${base_name} (5帧)"
    echo "$frame_dir"
}

# 转录音频 (使用OpenAI Whisper API)
transcribe_audio() {
    local audio_file="$1"
    local base_name=$(basename "$audio_file" .mp3)
    local transcript_file="$TRANSCRIPT_DIR/${base_name}.txt"
    
    if [ ! -f "$transcript_file" ]; then
        log "转录音频: $base_name"
        
        # 使用OpenAI Whisper API
        curl -s https://api.openai.com/v1/audio/transcriptions \
            -H "Authorization: Bearer $OPENAI_API_KEY" \
            -H "Content-Type: multipart/form-data" \
            -F file="@$audio_file" \
            -F model="whisper-1" \
            -F language="zh" \
            -F response_format="text" \
            -F timestamp_granularities[]=word \
            > "$transcript_file"
        
        success "转录完成: ${base_name}"
    else
        log "转录已存在，跳过: ${base_name}"
    fi
    
    echo "$transcript_file"
}

# 分析视频内容
analyze_video() {
    local video_file="$1"
    local base_name=$(basename "$video_file" .mp4)
    
    log "开始分析视频: $base_name"
    
    # 提取音频
    local audio_file=$(extract_audio "$video_file")
    
    # 截取关键帧
    local frame_dir=$(extract_frames "$video_file")
    
    # 转录音频
    local transcript_file=$(transcribe_audio "$audio_file")
    
    success "视频分析完成: $base_name"
    
    # 返回结果信息
    echo "{\"video\": \"$video_file\", \"audio\": \"$audio_file\", \"transcript\": \"$transcript_file\", \"frames\": \"$frame_dir\"}"
}

# 处理所有视频
process_all() {
    log "开始处理所有视频..."
    
    # 获取所有视频文件
    local videos=()
    while IFS= read -r -d '' video; do
        videos+=("$video")
    done < <(find "$VIDEO_DIR" -name "*.mp4" -print0 | sort)
    
    local total=${#videos[@]}
    log "找到 $total 个视频文件"
    
    # 处理每个视频
    local results_file="$WORK_DIR/processing_results.json"
    echo "{" > "$results_file"
    
    for i in "${!videos[@]}"; do
        local idx=$((i + 1))
        local video="${videos[$i]}"
        local base_name=$(basename "$video" .mp4)
        
        log "[$idx/$total] 处理视频: $base_name"
        
        # 分析视频
        local result=$(analyze_video "$video")
        
        # 保存结果
        echo "  \"$base_name\": $result" >> "$results_file"
        if [ $idx -lt $total ]; then
            echo "," >> "$results_file"
        fi
        
        log "[$idx/$total] 完成: $base_name"
        echo ""
    done
    
    echo "}" >> "$results_file"
    
    success "所有视频处理完成！"
    log "结果文件: $results_file"
}

# 生成综合分析报告
generate_report() {
    log "生成综合分析报告..."
    
    local report_file="$REPORTS_DIR/meituan_course_analysis.md"
    
    cat > "$report_file" << 'EOF'
# 美团运营课程深度分析报告

## 📊 分析概览

**课程名称**: 巅峰流量·实体团购操盘手【正式版】
**视频数量**: 21个
**总大小**: 11.26GB
**分析时间**: $(date '+%Y-%m-%d %H:%M:%S')

## 📚 课程模块结构

EOF

    # 添加模块列表
    find "$VIDEO_DIR" -type d -mindepth 1 | sort | while read -r dir; do
        local module_name=$(basename "$dir")
        local video_count=$(find "$dir" -name "*.mp4" | wc -l)
        echo "### $module_name ($video_count个视频)" >> "$report_file"
        find "$dir" -name "*.mp4" -exec basename {} \; | sed 's/.mp4$//' | sed 's/^/- /' >> "$report_file"
        echo "" >> "$report_file"
    done
    
    echo "" >> "$report_file"
    echo "## 📝 详细内容分析" >> "$report_file"
    echo "" >> "$report_file"
    
    # 为每个转录文件添加内容摘要
    for transcript in "$TRANSCRIPT_DIR"/*.txt; do
        if [ -f "$transcript" ]; then
            local base_name=$(basename "$transcript" .txt)
            echo "### $base_name" >> "$report_file"
            echo "" >> "$report_file"
            echo "```" >> "$report_file"
            head -100 "$transcript" >> "$report_file"
            echo "..." >> "$report_file"
            echo "```" >> "$report_file"
            echo "" >> "$report_file"
        fi
    done
    
    success "分析报告生成完成: $report_file"
}

# 显示帮助
show_help() {
    cat << 'EOF'
美团运营课程视频深度分析工具

用法: ./analyze-meituan-course.sh [命令]

命令:
  all         处理所有视频并生成报告 (默认)
  check       检查依赖环境
  list        列出所有视频文件
  clean       清理临时文件
  help        显示帮助信息

示例:
  ./analyze-meituan-course.sh all      # 完整分析流程
  ./analyze-meituan-course.sh list     # 查看视频列表
  ./analyze-meituan-course.sh check    # 检查环境

EOF
}

# 列出视频
list_videos() {
    log "视频文件列表:"
    echo ""
    find "$VIDEO_DIR" -name "*.mp4" | sort | nl -w2 -s'. ' | while read -r line; do
        local file=$(echo "$line" | sed 's/^[^.]*\. //')
        local size=$(ls -lh "$file" 2>/dev/null | awk '{print $5}')
        local name=$(basename "$file")
        echo "  $line ($size)"
    done
    echo ""
    local total=$(find "$VIDEO_DIR" -name "*.mp4" | wc -l)
    log "总计: $total 个视频文件"
}

# 清理临时文件
clean_temp() {
    log "清理临时文件..."
    rm -rf "$WORK_DIR/audio"
    rm -rf "$FRAMES_DIR"
    success "临时文件已清理"
    log "保留文件: 转录文本($TRANSCRIPT_DIR) 和 报告($REPORTS_DIR)"
}

# 主函数
main() {
    case "${1:-all}" in
        all)
            check_deps
            process_all
            generate_report
            ;;
        check)
            check_deps
            ;;
        list)
            list_videos
            ;;
        clean)
            clean_temp
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "未知命令: $1"
            show_help
            exit 1
            ;;
    esac
}

# 运行
main "$@"

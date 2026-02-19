#!/bin/bash
#
# 智能视频分析系统 - 适用于大文件处理
# 支持自动分块、Whisper转录、内容分析
#

set -e

VIDEO_DIR="/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】"
WORK_DIR="/Users/xiaolongxia/.openclaw/workspace/analysis/meituan-course"
TRANSCRIPT_DIR="$WORK_DIR/transcripts"
CHUNKS_DIR="$WORK_DIR/chunks"
REPORTS_DIR="$WORK_DIR/reports"

mkdir -p "$TRANSCRIPT_DIR" "$CHUNKS_DIR" "$REPORTS_DIR"

# API配置
OPENAI_API_KEY="${OPENAI_API_KEY:-$(cat "$HOME/.openclaw/openclaw.json" 2>/dev/null | grep -o '"OPENAI_API_KEY": "[^"]*"' | cut -d'"' -f4)}"

if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ 错误: 未设置 OPENAI_API_KEY"
    exit 1
fi

echo "🚀 美团运营课程智能分析系统"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${BLUE}[AI]${NC} $1"; }
success() { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; }

# 获取视频信息
get_video_info() {
    local video="$1"
    ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$video" 2>/dev/null
}

# 智能分块策略
# 每个块约10分钟，保证转录质量同时避免API限制
CHUNK_DURATION=600  # 10分钟

extract_and_chunk() {
    local video="$1"
    local base_name=$(basename "$video" .mp4)
    local audio_dir="$WORK_DIR/audio/${base_name}"
    
    mkdir -p "$audio_dir"
    
    # 获取视频时长
    local duration=$(get_video_info "$video" | cut -d. -f1)
    if [ -z "$duration" ] || [ "$duration" -eq 0 ]; then
        duration=3600
    fi
    
    local minutes=$((duration / 60))
    log "视频时长: ${minutes}分钟 (${duration}秒)"
    
    # 计算需要多少个块
    local num_chunks=$(( (duration + CHUNK_DURATION - 1) / CHUNK_DURATION ))
    log "将分为 ${num_chunks} 个音频块处理"
    
    # 提取并切分音频
    local chunk_files=()
    for ((i=0; i<num_chunks; i++)); do
        local start_time=$((i * CHUNK_DURATION))
        local chunk_file="$audio_dir/chunk_$(printf %03d $i).mp3"
        
        if [ ! -f "$chunk_file" ]; then
            log "提取音频块 $((i+1))/${num_chunks}..."
            ffmpeg -ss "$start_time" -t "$CHUNK_DURATION" -i "$video" \
                -vn -ar 16000 -ac 1 -c:a libmp3lame -q:a 2 \
                "$chunk_file" -y 2>/dev/null
        fi
        
        chunk_files+=("$chunk_file")
    done
    
    success "音频提取完成: ${#chunk_files[@]} 个块"
    echo "${chunk_files[@]}"
}

# 转录单个音频块
transcribe_chunk() {
    local chunk_file="$1"
    local chunk_name=$(basename "$chunk_file" .mp3)
    local transcript_file="$TRANSCRIPT_DIR/${chunk_name}.txt"
    
    if [ -f "$transcript_file" ] && [ -s "$transcript_file" ]; then
        log "转录已存在，跳过: $chunk_name"
        echo "$transcript_file"
        return
    fi
    
    log "正在转录: $chunk_name"
    
    local retry_count=0
    local max_retries=3
    
    while [ $retry_count -lt $max_retries ]; do
        local response=$(curl -s -w "\n%{http_code}" https://api.openai.com/v1/audio/transcriptions \
            -H "Authorization: Bearer $OPENAI_API_KEY" \
            -H "Content-Type: multipart/form-data" \
            -F file="@$chunk_file" \
            -F model="whisper-1" \
            -F language="zh" \
            -F response_format="text" \
            -F prompt="这是一段关于美团运营、团购推广、实体店获客的教学视频")
        
        local http_code=$(echo "$response" | tail -n1)
        local body=$(echo "$response" | sed '$d')
        
        if [ "$http_code" = "200" ]; then
            echo "$body" > "$transcript_file"
            success "转录成功: $chunk_name"
            echo "$transcript_file"
            return
        else
            retry_count=$((retry_count + 1))
            warn "转录失败 (HTTP $http_code)，第 ${retry_count} 次重试..."
            sleep 2
        fi
    done
    
    error "转录失败: $chunk_name (已重试 $max_retries 次)"
    echo ""
}

# 合并同一视频的所有转录
merge_transcripts() {
    local video_base="$1"
    local output_file="$TRANSCRIPT_DIR/${video_base}_完整转录.txt"
    
    log "合并转录: $video_base"
    
    > "$output_file"
    local chunk_count=0
    
    for chunk in "$TRANSCRIPT_DIR"/chunk_*.txt; do
        if [ -f "$chunk" ]; then
            chunk_name=$(basename "$chunk" .txt)
            # 提取块序号计算时间戳
            local chunk_num=$(echo "$chunk_name" | grep -o '[0-9]*$' | sed 's/^0*//')
            local start_min=$((chunk_num * 10))
            local end_min=$((start_min + 10))
            
            echo "" >> "$output_file"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$output_file"
            echo "⏱️ 时间段: ${start_min}:00 - ${end_min}:00" >> "$output_file"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$output_file"
            echo "" >> "$output_file"
            cat "$chunk" >> "$output_file"
            echo "" >> "$output_file"
            
            chunk_count=$((chunk_count + 1))
        fi
    done
    
    success "合并完成: $output_file ($chunk_count 个片段)"
    echo "$output_file"
}

# 分析视频内容
analyze_content() {
    local video="$1"
    local base_name=$(basename "$video" .mp4)
    
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "开始分析: $base_name"
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 步骤1: 提取并分块音频
    log "步骤 1/3: 音频提取与分块..."
    local chunk_files_str=$(extract_and_chunk "$video")
    read -ra chunk_files <<< "$chunk_files_str"
    
    # 步骤2: 转录所有块
    log "步骤 2/3: 音频转录..."
    local transcript_files=()
    for chunk_file in "${chunk_files[@]}"; do
        if [ -f "$chunk_file" ]; then
            local transcript=$(transcribe_chunk "$chunk_file")
            if [ -n "$transcript" ]; then
                transcript_files+=("$transcript")
            fi
        fi
    done
    
    # 步骤3: 合并转录
    log "步骤 3/3: 合并转录文本..."
    local full_transcript=$(merge_transcripts "$base_name")
    
    success "分析完成: $base_name"
    echo "$full_transcript"
}

# 处理优先级排序的视频列表
get_priority_videos() {
    # 按优先级排序：评价管理 > 推广通 > 后台数据 > 前端搭建 > 门店管理 > 排行榜 > 先导课
    cat << 'EOF'
/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】/5.评价与星级评分/评价：1.评分的底层逻辑.mp4
/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】/5.评价与星级评分/评价：2.AB账号规避差评.mp4
/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】/5.评价与星级评分/评价：3.99%留存的方法-双评法.mp4
/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】/5.评价与星级评分/评价：4.99%留存的方法-核评比.mp4
/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】/5.评价与星级评分/评价：5.星级评分总结.mp4
/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】/6.推广通/推广通：1.通投拉满与关键词出价.mp4
/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】/6.推广通/推广通：2.后台的基础设置.mp4
/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】/6.推广通/推广通：3.关键词垂类与泛垂类打法.mp4
/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】/6.推广通/推广通：4.微付费撬动自然流的方法.mp4
/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】/4.后台数据/后台数据：三大核心数据（1）.mp4
/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】/4.后台数据/后台数据：三大核心数据（2）.mp4
/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】/4.后台数据/后台数据：三大核心数据（3）.mp4
EOF
}

# 生成分析报告
generate_analysis_report() {
    local report_file="$REPORTS_DIR/course_analysis_report.md"
    
    log "生成综合分析报告..."
    
    cat > "$report_file" << EOF
# 美团运营课程深度分析报告

**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')  
**课程名称**: 巅峰流量·实体团购操盘手【正式版】  
**视频数量**: 21个  
**总大小**: 11.26GB  

---

## 📚 课程模块总览

### 模块1: 评价与星级评分 (5个视频)
- 评分的底层逻辑
- AB账号规避差评
- 99%留存的方法-双评法
- 99%留存的方法-核评比
- 星级评分总结

### 模块2: 推广通 (4个视频)
- 通投拉满与关键词出价
- 后台的基础设置
- 关键词垂类与泛垂类打法
- 微付费撬动自然流的方法

### 模块3: 后台数据 (3个视频)
- 三大核心数据（1）
- 三大核心数据（2）
- 三大核心数据（3）

### 模块4: 前端搭建 (4个视频)
- 0成本1天拿金牌
- 团单价格设定
- 热销指数的底层逻辑
- 视觉营销

### 模块5: 门店管理 (2个视频)
- 账号冷启动
- 奖罚机制

### 模块6: 排行榜 (2个视频)
- 低成本上热门榜
- 好评榜的考核逻辑

### 模块7: 先导课 (1个视频)
- 实体获客的道与法

---

## 📝 转录文件清单

EOF

    # 列出所有转录文件
    for transcript in "$TRANSCRIPT_DIR"/*_完整转录.txt; do
        if [ -f "$transcript" ]; then
            local name=$(basename "$transcript" _完整转录.txt)
            local size=$(wc -c < "$transcript" | awk '{print int($1/1024)}')
            echo "- **$name** (${size}KB)" >> "$report_file"
        fi
    done
    
    echo "" >> "$report_file"
    echo "---" >> "$report_file"
    echo "" >> "$report_file"
    echo "*报告由AI自动生成*" >> "$report_file"
    
    success "分析报告生成: $report_file"
}

# 处理单个视频
process_single() {
    local video="$1"
    if [ ! -f "$video" ]; then
        error "视频文件不存在: $video"
        return 1
    fi
    
    analyze_content "$video"
}

# 主函数
main() {
    case "${1:-priority}" in
        priority)
            log "开始优先处理核心模块视频..."
            log "优先级: 评价管理 > 推广通 > 后台数据"
            echo ""
            
            local count=0
            while IFS= read -r video; do
                if [ -n "$video" ] && [ -f "$video" ]; then
                    count=$((count + 1))
                    log "[$count] 处理: $(basename "$video")"
                    process_single "$video"
                    echo ""
                fi
            done < <(get_priority_videos)
            
            success "优先级视频处理完成!"
            ;;
        all)
            log "处理所有视频..."
            find "$VIDEO_DIR" -name "*.mp4" -print0 | while IFS= read -r -d '' video; do
                process_single "$video"
            done
            ;;
        single)
            if [ -z "$2" ]; then
                error "请指定视频文件路径"
                exit 1
            fi
            process_single "$2"
            ;;
        report)
            generate_analysis_report
            ;;
        help)
            echo "用法: $0 [priority|all|single <视频路径>|report]"
            echo ""
            echo "  priority  - 优先处理核心模块 (默认)"
            echo "  all       - 处理所有视频"
            echo "  single    - 处理单个视频"
            echo "  report    - 生成分析报告"
            ;;
        *)
            error "未知命令: $1"
            echo "用法: $0 [priority|all|single|report|help]"
            exit 1
            ;;
    esac
    
    # 生成报告
    generate_analysis_report
}

# 运行
main "$@"

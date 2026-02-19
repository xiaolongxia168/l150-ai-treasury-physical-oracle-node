#!/bin/bash
#
# 视频转录 + AI知识库投喂 一体化脚本
# 一键完成：视频转录 → 内容结构化 → AI知识库投喂
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 路径配置
WORKSPACE="/Users/xiaolongxia/.openclaw/workspace"
COURSE_DIR="$WORKSPACE/analysis/meituan-course"
ESCAPE_ROOM_DIR="$WORKSPACE/密室逃脱运营"

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🎬 视频转录 + 🤖 AI知识库投喂 一体化系统                     ║"
echo "║  美团运营课程 → 音频提取 → Whisper API → AI数字运营           ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 检查依赖
echo -e "${YELLOW}🔍 检查依赖...${NC}"

if ! command -v ffmpeg &> /dev/null; then
    echo -e "${RED}❌ 未找到 ffmpeg${NC}"
    echo "请安装: brew install ffmpeg"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 未找到 python3${NC}"
    exit 1
fi

# 检查API密钥
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  警告: 未设置 OPENAI_API_KEY 环境变量${NC}"
    echo "请设置: export OPENAI_API_KEY='your-api-key'"
    echo ""
    read -p "是否继续? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${GREEN}✅ 依赖检查通过${NC}"
echo ""

# 步骤1: 视频转录
echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  步骤 1/3: 视频转录${NC}"
echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
echo ""

cd "$COURSE_DIR"

# 显示统计
python3 transcribe_and_feed.py stats

echo ""
read -p "开始转录? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🚀 开始批量转录...${NC}"
    python3 transcribe_and_feed.py
else
    echo -e "${YELLOW}⏭️  跳过转录步骤${NC}"
fi

echo ""

# 步骤2: 知识库生成
echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  步骤 2/3: 生成AI知识库${NC}"
echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
echo ""

cd "$ESCAPE_ROOM_DIR"

# 确保scripts目录存在
mkdir -p scripts

# 复制知识库投喂脚本（如果不存在）
if [ ! -f "scripts/knowledge_feeder.py" ]; then
    cp "$WORKSPACE/analysis/meituan-course/knowledge_feeder.py" scripts/ 2>/dev/null || true
fi

echo -e "${YELLOW}🧠 生成知识库...${NC}"
python3 scripts/knowledge_feeder.py

echo ""

# 步骤3: 完成报告
echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  步骤 3/3: 完成报告${NC}"
echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${GREEN}✅ 全部完成！${NC}"
echo ""
echo "📂 输出文件:"
echo "  • 音频文件:    $COURSE_DIR/audio-extracted/"
echo "  • 转录文本:    $COURSE_DIR/transcripts-api/"
echo "  • 知识库JSON:  $ESCAPE_ROOM_DIR/知识库/knowledge_base_rag.json"
echo "  • 知识库MD:    $ESCAPE_ROOM_DIR/知识库/美团运营课程知识库.md"
echo "  • AI提示词:    $ESCAPE_ROOM_DIR/知识库/ai_system_prompt.txt"
echo ""
echo "🎯 AI数字运营系统现在可以使用这些知识回答运营问题了！"
echo ""

# 显示知识库统计
if [ -f "$ESCAPE_ROOM_DIR/知识库/knowledge_base_rag.json" ]; then
    echo -e "${BLUE}📊 知识库统计:${NC}"
    python3 -c "
import json
with open('$ESCAPE_ROOM_DIR/知识库/knowledge_base_rag.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f\"  总课程数: {data.get('total_courses', 0)}\")
    print(f\"  分类: {', '.join(data.get('categories', {}).keys())}\")
" 2>/dev/null || true
    echo ""
fi

echo -e "${GREEN}🎉 投喂完成！AI运营助手已准备就绪。${NC}"

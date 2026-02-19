#!/bin/bash

# 技能搜索和安装脚本
# 目标：安装视频制作、文案生成、融资自动化相关技能

echo "=== 搜索关键技能 ==="

# 1. 视频制作相关技能
echo "1. 搜索视频制作技能..."
# 这里可以添加从ClawHub搜索的逻辑

# 2. 文案生成技能
echo "2. 搜索文案生成技能..."
# 检查现有技能中是否有相关内容生成技能

# 3. 融资自动化技能
echo "3. 搜索融资自动化技能..."
# 检查business-model-canvas等现有技能

# 4. 检查已安装的相关技能
echo "=== 已安装的相关技能 ==="
cd /Users/xiaolongxia/.openclaw/workspace/skills
find . -name "SKILL.md" -exec grep -l -i "video\|content\|文案\|social\|automation\|融资\|investment" {} \; | while read skill; do
    skill_name=$(dirname "$skill" | xargs basename)
    echo "✅ $skill_name"
done

echo ""
echo "=== 需要安装的技能 ==="
echo "1. video-frames (视频帧提取)"
echo "2. obsidian (笔记自动化)"
echo "3. peekaboo (macOS UI自动化)"
echo "4. 专门的视频编辑自动化技能"
echo "5. 高级文案生成和优化技能"
echo "6. 融资CRM和投资人关系管理技能"

echo ""
echo "=== 安装建议 ==="
echo "1. 访问 https://clawhub.com 搜索以下关键词："
echo "   - video-editing-automation"
echo "   - content-generation"
echo "   - copywriting-ai"
echo "   - investment-automation"
echo "   - crm-automation"
echo "2. 使用GitHub搜索相关开源技能"
echo "3. 考虑自定义开发关键技能"
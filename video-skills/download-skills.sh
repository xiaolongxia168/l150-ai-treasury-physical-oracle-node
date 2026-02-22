#!/bin/bash

# 创建技能目录
mkdir -p skills

# 技能列表
skills=(
    "neur0map/clawvid"
    "DevvGwardo/grok-imagine-video"
    "zhanghaonan777/Seedance2-skill"
    "kghamilton89/veo-video-generator"
    "luv005/renderful-ai-skill"
    "zrewolwerowanykaloryfer/deapi-clawdbot-skill"
    "lijingpan/video-uploader-skill"
    "kantylee/video-audio-extractor"
    "ZeroPointRepo/youtube-skills"
    "happynocode/openclaw-skill-youtube"
    "KAMIENDER/douyin-video-fetch"
    "diskd-ai/assemblyai-cli"
    "sxu75374/videochat-withme"
    "SuperNovaRobot/grok-video-skill"
    "viralclaw/openclaw-skill"
)

echo "开始下载视频生成技能..."

for skill in "${skills[@]}"; do
    repo_name=$(basename "$skill")
    echo "正在下载: $repo_name"
    
    # 使用GitHub API下载ZIP文件
    curl -L -o "skills/${repo_name}.zip" "https://github.com/${skill}/archive/refs/heads/main.zip" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "✓ 已下载: $repo_name"
        
        # 解压ZIP文件
        unzip -q "skills/${repo_name}.zip" -d "skills/" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo "✓ 已解压: $repo_name"
            
            # 重命名目录
            if [ -d "skills/${repo_name}-main" ]; then
                mv "skills/${repo_name}-main" "skills/${repo_name}"
            fi
            
            # 删除ZIP文件
            rm "skills/${repo_name}.zip"
        else
            echo "✗ 解压失败: $repo_name"
        fi
    else
        echo "✗ 下载失败: $repo_name"
    fi
    
    echo ""
done

echo "下载完成！"
echo "总共下载了 $(ls -1 skills/ | wc -l) 个技能"
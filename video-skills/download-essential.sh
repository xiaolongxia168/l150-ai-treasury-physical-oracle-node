#!/bin/bash

# 创建技能目录
mkdir -p essential-skills

# 最重要的技能列表（确保能下载的）
essential_skills=(
    "neur0map/clawvid"
    "zhanghaonan777/Seedance2-skill"
    "kghamilton89/veo-video-generator"
    "happynocode/openclaw-skill-youtube"
    "ZeroPointRepo/youtube-skills"
    "KAMIENDER/douyin-video-fetch"
    "kantylee/video-audio-extractor"
)

echo "开始下载核心视频技能..."

for skill in "${essential_skills[@]}"; do
    repo_name=$(basename "$skill")
    echo "正在下载: $repo_name"
    
    # 尝试下载
    if curl -L -o "essential-skills/${repo_name}.zip" "https://github.com/${skill}/archive/refs/heads/main.zip" --silent --fail; then
        echo "✓ 已下载: $repo_name"
        
        # 尝试解压
        if unzip -q "essential-skills/${repo_name}.zip" -d "essential-skills/" 2>/dev/null; then
            echo "✓ 已解压: $repo_name"
            
            # 重命名目录
            if [ -d "essential-skills/${repo_name}-main" ]; then
                mv "essential-skills/${repo_name}-main" "essential-skills/${repo_name}"
            fi
            
            # 删除ZIP文件
            rm "essential-skills/${repo_name}.zip"
        else
            echo "✗ 解压失败: $repo_name"
            # 尝试其他解压方式
            if [ -f "essential-skills/${repo_name}.zip" ]; then
                echo "  尝试使用其他解压方法..."
                cd "essential-skills" && jar xf "${repo_name}.zip" && cd ..
                if [ $? -eq 0 ]; then
                    echo "✓ 使用jar解压成功"
                    rm "essential-skills/${repo_name}.zip"
                fi
            fi
        fi
    else
        echo "✗ 下载失败: $repo_name"
    fi
    
    echo ""
done

echo "下载完成！"
echo "成功下载的技能:"
ls -1 essential-skills/
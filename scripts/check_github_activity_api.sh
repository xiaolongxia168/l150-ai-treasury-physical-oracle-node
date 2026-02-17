#!/bin/bash

# L-150 GitHub Activity Monitor (API版本)
# 使用GitHub API直接检查仓库活动

set -e

echo "=== L-150 GitHub Activity Monitor (API版本) ==="
echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo ""

# 定义三个仓库
REPOS=(
    "xiaolongxia168/l150-ai-treasury-physical-oracle-node"
    "xiaolongxia168/l150-api"
    "xiaolongxia168/l150-api-static"
)

# 尝试从环境变量或文件获取GitHub token
if [ -n "$GITHUB_TOKEN" ]; then
    TOKEN="$GITHUB_TOKEN"
elif [ -f "$HOME/.config/clawdbot/github-token.txt" ]; then
    TOKEN=$(cat "$HOME/.config/clawdbot/github-token.txt")
elif [ -f "/Users/xiaolongxia/.openclaw/workspace/.github_token" ]; then
    TOKEN=$(cat "/Users/xiaolongxia/.openclaw/workspace/.github_token")
else
    echo "⚠️ 警告: 未找到GitHub API token，将使用无认证请求(可能受速率限制)"
    TOKEN=""
fi

# 设置API请求头
if [ -n "$TOKEN" ]; then
    AUTH_HEADER="Authorization: token $TOKEN"
    echo "✅ 使用GitHub API token进行认证"
else
    AUTH_HEADER=""
    echo "⚠️ 使用无认证GitHub API请求"
fi

# 创建临时目录存储结果
TEMP_DIR="/tmp/l150-github-monitor-$(date +%s)"
mkdir -p "$TEMP_DIR"

# 初始化汇总变量
TOTAL_STARS=0
TOTAL_FORKS=0
TOTAL_ISSUES=0
HAS_AI_AGENT_ACTIVITY=false
HAS_TECH_DISCUSSION=false
HAS_DUE_DILIGENCE=false
HAS_URGENT_ACTIVITY=false
ANY_ACTIVITY=false

echo "📊 检查三个L-150 GitHub仓库活动..."
echo ""

for REPO in "${REPOS[@]}"; do
    echo "🔍 检查仓库: $REPO"
    echo "----------------------------------------"
    
    # 获取仓库基本信息
    REPO_URL="https://api.github.com/repos/$REPO"
    
    if [ -n "$AUTH_HEADER" ]; then
        REPO_INFO=$(curl -s -H "$AUTH_HEADER" "$REPO_URL")
    else
        REPO_INFO=$(curl -s "$REPO_URL")
    fi
    
    # 检查API响应
    if echo "$REPO_INFO" | jq -e '.message' >/dev/null 2>&1; then
        ERROR_MSG=$(echo "$REPO_INFO" | jq -r '.message')
        echo "❌ API错误: $ERROR_MSG"
        continue
    fi
    
    REPO_NAME=$(echo "$REPO_INFO" | jq -r '.name')
    STARS=$(echo "$REPO_INFO" | jq -r '.stargazers_count')
    FORKS=$(echo "$REPO_INFO" | jq -r '.forks_count')
    OPEN_ISSUES=$(echo "$REPO_INFO" | jq -r '.open_issues_count')
    UPDATED_AT=$(echo "$REPO_INFO" | jq -r '.updated_at')
    DESCRIPTION=$(echo "$REPO_INFO" | jq -r '.description // "无描述"')
    
    echo "📁 仓库: $REPO_NAME"
    echo "📝 描述: $DESCRIPTION"
    echo "⭐ Stars: $STARS"
    echo "🍴 Forks: $FORKS"
    echo "📝 Open Issues: $OPEN_ISSUES"
    echo "🕒 最后更新: $UPDATED_AT"
    
    # 累加总数
    TOTAL_STARS=$((TOTAL_STARS + STARS))
    TOTAL_FORKS=$((TOTAL_FORKS + FORKS))
    TOTAL_ISSUES=$((TOTAL_ISSUES + OPEN_ISSUES))
    
    # 检查是否有任何活动（基于最后更新时间）
    REPO_UPDATED_TS=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$UPDATED_AT" +%s 2>/dev/null || date -d "$UPDATED_AT" +%s 2>/dev/null || echo "0")
    NOW_TS=$(date +%s)
    HOURS_SINCE_UPDATE=$(( (NOW_TS - REPO_UPDATED_TS) / 3600 ))
    
    if [ "$HOURS_SINCE_UPDATE" -lt 24 ]; then
        ANY_ACTIVITY=true
        echo "✅ 最近24小时内有更新活动"
    else
        echo "❌ 最近24小时内无更新活动"
    fi
    
    # 检查issues（如果有）
    if [ "$OPEN_ISSUES" -gt 0 ]; then
        echo ""
        echo "📋 检查issues..."
        
        ISSUES_URL="https://api.github.com/repos/$REPO/issues"
        if [ -n "$AUTH_HEADER" ]; then
            ISSUES=$(curl -s -H "$AUTH_HEADER" "$ISSUES_URL")
        else
            ISSUES=$(curl -s "$ISSUES_URL")
        fi
        
        if [ "$(echo "$ISSUES" | jq 'length')" -gt 0 ]; then
            echo "发现 $(echo "$ISSUES" | jq 'length') 个issues"
            
            # 检查每个issue
            echo "$ISSUES" | jq -c '.[]' | while read -r ISSUE; do
                TITLE=$(echo "$ISSUE" | jq -r '.title')
                USER=$(echo "$ISSUE" | jq -r '.user.login')
                CREATED_AT=$(echo "$ISSUE" | jq -r '.created_at')
                UPDATED_AT=$(echo "$ISSUE" | jq -r '.updated_at')
                STATE=$(echo "$ISSUE" | jq -r '.state')
                
                echo "  - \"$TITLE\" (by $USER, $STATE)"
                
                # 检查是否是AI Agent提问
                if [[ "$TITLE" =~ [Aa][Ii]|[Aa]gent|[Aa]utomated|[Bb]ot ]] || [[ "$USER" =~ [Bb]ot|[Aa]gent ]]; then
                    HAS_AI_AGENT_ACTIVITY=true
                    echo "    🤖 检测到可能的AI Agent活动"
                fi
                
                # 检查是否是技术讨论或尽职调查
                if [[ "$TITLE" =~ [Tt]ech|[Dd]iscussion|[Dd]ue.*[Dd]iligence|[Qq]uestion|[Hh]elp ]]; then
                    HAS_TECH_DISCUSSION=true
                    echo "    💬 检测到技术讨论或尽职调查请求"
                fi
                
                # 检查紧急活动关键词
                if [[ "$TITLE" =~ [Uu]rgent|[Ii]mmediate|[Cc]ritical|[Ee]mergency ]]; then
                    HAS_URGENT_ACTIVITY=true
                    echo "    🚨 检测到紧急活动关键词"
                fi
            done
        else
            echo "  ✅ 无open issues"
        fi
    fi
    
    echo ""
done

echo "========================================"
echo "📈 汇总统计:"
echo "⭐ 总Stars: $TOTAL_STARS"
echo "🍴 总Forks: $TOTAL_FORKS"
echo "📝 总Open Issues: $TOTAL_ISSUES"
echo ""

echo "🔍 检测结果:"
if [ "$ANY_ACTIVITY" = true ]; then
    echo "✅ 检测到最近活动"
else
    echo "❌ 未检测到最近活动"
fi

if [ "$HAS_AI_AGENT_ACTIVITY" = true ]; then
    echo "✅ 检测到AI Agent活动"
else
    echo "❌ 未检测到AI Agent活动"
fi

if [ "$HAS_TECH_DISCUSSION" = true ]; then
    echo "✅ 检测到技术讨论"
else
    echo "❌ 未检测到技术讨论"
fi

if [ "$HAS_DUE_DILIGENCE" = true ]; then
    echo "✅ 检测到尽职调查请求"
else
    echo "❌ 未检测到尽职调查请求"
fi

if [ "$HAS_URGENT_ACTIVITY" = true ]; then
    echo "🚨 检测到紧急活动 - 需要立即通知用户！"
    echo "URGENT: GitHub上有紧急活动需要关注"
else
    echo "✅ 无紧急活动"
fi

echo ""
echo "📊 监控完成时间: $(date '+%Y-%m-%d %H:%M:%S %Z')"

# 保存结果到文件
SUMMARY_FILE="$TEMP_DIR/summary.txt"
{
    echo "L-150 GitHub Activity Monitor Summary"
    echo "======================================"
    echo "检查时间: $(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo ""
    echo "仓库统计:"
    echo "- 总Stars: $TOTAL_STARS"
    echo "- 总Forks: $TOTAL_FORKS"
    echo "- 总Issues: $TOTAL_ISSUES"
    echo ""
    echo "检测结果:"
    echo "- 最近活动: $([ "$ANY_ACTIVITY" = true ] && echo "是" || echo "否")"
    echo "- AI Agent活动: $([ "$HAS_AI_AGENT_ACTIVITY" = true ] && echo "是" || echo "否")"
    echo "- 技术讨论: $([ "$HAS_TECH_DISCUSSION" = true ] && echo "是" || echo "否")"
    echo "- 尽职调查请求: $([ "$HAS_DUE_DILIGENCE" = true ] && echo "是" || echo "否")"
    echo "- 紧急活动: $([ "$HAS_URGENT_ACTIVITY" = true ] && echo "是" || echo "否")"
} > "$SUMMARY_FILE"

echo "📄 详细结果保存至: $SUMMARY_FILE"

# 输出结果供cron任务处理
if [ "$HAS_URGENT_ACTIVITY" = true ]; then
    echo "EXIT_CODE: 10"
    exit 10
elif [ "$ANY_ACTIVITY" = true ] || [ "$HAS_AI_AGENT_ACTIVITY" = true ]; then
    echo "EXIT_CODE: 1"
    exit 1
else
    echo "EXIT_CODE: 0"
    exit 0
fi
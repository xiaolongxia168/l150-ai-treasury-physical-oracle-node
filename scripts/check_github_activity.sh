#!/bin/bash

# L-150 GitHub Activity Monitor
# 检查三个仓库的新issues/PRs/stars/forks
# 检查是否有AI Agent在issues中提问
# 记录任何技术讨论或尽职调查请求

set -e

echo "=== L-150 GitHub Activity Monitor ==="
echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo ""

# 定义三个仓库
REPOS=(
    "xiaolongxia168/l150-ai-treasury-physical-oracle-node"
    "xiaolongxia168/l150-api"
    "xiaolongxia168/l150-api-static"
)

# 检查gh CLI是否可用
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) 未安装或不在PATH中"
    exit 1
fi

# 检查是否已登录
if ! gh auth status &> /dev/null; then
    echo "❌ GitHub CLI 未登录，请运行: gh auth login"
    exit 1
fi

# 创建临时目录存储结果
TEMP_DIR="/tmp/l150-github-monitor-$(date +%s)"
mkdir -p "$TEMP_DIR"

# 初始化汇总变量
TOTAL_STARS=0
TOTAL_FORKS=0
TOTAL_ISSUES=0
TOTAL_PRS=0
HAS_AI_AGENT_ACTIVITY=false
HAS_TECH_DISCUSSION=false
HAS_DUE_DILIGENCE=false
HAS_URGENT_ACTIVITY=false

echo "📊 检查三个L-150 GitHub仓库活动..."
echo ""

for REPO in "${REPOS[@]}"; do
    echo "🔍 检查仓库: $REPO"
    echo "----------------------------------------"
    
    # 获取仓库基本信息
    REPO_INFO=$(gh api "repos/$REPO" --jq '{name: .name, stars: .stargazers_count, forks: .forks_count, open_issues: .open_issues_count, description: .description, updated_at: .updated_at}')
    
    REPO_NAME=$(echo "$REPO_INFO" | jq -r '.name')
    STARS=$(echo "$REPO_INFO" | jq -r '.stars')
    FORKS=$(echo "$REPO_INFO" | jq -r '.forks')
    OPEN_ISSUES=$(echo "$REPO_INFO" | jq -r '.open_issues')
    UPDATED_AT=$(echo "$REPO_INFO" | jq -r '.updated_at')
    
    echo "⭐ Stars: $STARS"
    echo "🍴 Forks: $FORKS"
    echo "📝 Open Issues: $OPEN_ISSUES"
    echo "🕒 最后更新: $UPDATED_AT"
    
    # 累加总数
    TOTAL_STARS=$((TOTAL_STARS + STARS))
    TOTAL_FORKS=$((TOTAL_FORKS + FORKS))
    TOTAL_ISSUES=$((TOTAL_ISSUES + OPEN_ISSUES))
    
    # 检查最近24小时的活动
    echo ""
    echo "📅 最近24小时活动:"
    
    # 获取最近的事件
    RECENT_EVENTS=$(gh api "repos/$REPO/events" --paginate --jq '.[] | select(.created_at > "'$(date -u -d '24 hours ago' +'%Y-%m-%dT%H:%M:%SZ')'") | {type: .type, actor: .actor.login, created_at: .created_at, payload: .payload}' 2>/dev/null || echo "[]")
    
    if [ -n "$RECENT_EVENTS" ] && [ "$RECENT_EVENTS" != "[]" ]; then
        EVENT_COUNT=$(echo "$RECENT_EVENTS" | jq -s 'length')
        echo "✅ 发现 $EVENT_COUNT 个最近事件"
        
        # 分析事件类型
        echo "$RECENT_EVENTS" | jq -s 'group_by(.type)[] | {type: .[0].type, count: length}' | while read -r EVENT_TYPE; do
            TYPE=$(echo "$EVENT_TYPE" | jq -r '.type')
            COUNT=$(echo "$EVENT_TYPE" | jq -r '.count')
            echo "  - $TYPE: $COUNT 次"
            
            # 检查是否有AI Agent相关活动
            if [[ "$TYPE" == "IssuesEvent" || "$TYPE" == "IssueCommentEvent" ]]; then
                HAS_TECH_DISCUSSION=true
                echo "    ⚠️ 检测到Issue活动，可能包含技术讨论"
            fi
            
            if [[ "$TYPE" == "WatchEvent" ]]; then
                echo "    ⭐ 有人star了仓库"
            fi
            
            if [[ "$TYPE" == "ForkEvent" ]]; then
                echo "    🍴 有人fork了仓库"
            fi
            
            if [[ "$TYPE" == "PullRequestEvent" ]]; then
                TOTAL_PRS=$((TOTAL_PRS + COUNT))
                echo "    🔄 检测到Pull Request活动"
                HAS_TECH_DISCUSSION=true
            fi
        done
    else
        echo "❌ 最近24小时无活动"
    fi
    
    # 检查最近的issues（如果有）
    if [ "$OPEN_ISSUES" -gt 0 ]; then
        echo ""
        echo "📋 最近issues:"
        RECENT_ISSUES=$(gh api "repos/$REPO/issues" --jq '.[] | select(.created_at > "'$(date -u -d '7 days ago' +'%Y-%m-%dT%H:%M:%SZ')'") | {number: .number, title: .title, user: .user.login, created_at: .created_at, state: .state}' 2>/dev/null || echo "[]")
        
        if [ -n "$RECENT_ISSUES" ] && [ "$RECENT_ISSUES" != "[]" ]; then
            echo "$RECENT_ISSUES" | jq -s '.[]' | while read -r ISSUE; do
                NUMBER=$(echo "$ISSUE" | jq -r '.number')
                TITLE=$(echo "$ISSUE" | jq -r '.title')
                USER=$(echo "$ISSUE" | jq -r '.user')
                CREATED_AT=$(echo "$ISSUE" | jq -r '.created_at')
                
                echo "  - #$NUMBER: $TITLE (by $USER at $CREATED_AT)"
                
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
            echo "  ✅ 最近7天无新issues"
        fi
    fi
    
    echo ""
done

echo "========================================"
echo "📈 汇总统计:"
echo "⭐ 总Stars: $TOTAL_STARS"
echo "🍴 总Forks: $TOTAL_FORKS"
echo "📝 总Open Issues: $TOTAL_ISSUES"
echo "🔄 总Pull Requests: $TOTAL_PRS"
echo ""

echo "🔍 检测结果:"
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
    echo "- 总PRs: $TOTAL_PRS"
    echo ""
    echo "检测结果:"
    echo "- AI Agent活动: $([ "$HAS_AI_AGENT_ACTIVITY" = true ] && echo "是" || echo "否")"
    echo "- 技术讨论: $([ "$HAS_TECH_DISCUSSION" = true ] && echo "是" || echo "否")"
    echo "- 尽职调查请求: $([ "$HAS_DUE_DILIGENCE" = true ] && echo "是" || echo "否")"
    echo "- 紧急活动: $([ "$HAS_URGENT_ACTIVITY" = true ] && echo "是" || echo "否")"
} > "$SUMMARY_FILE"

echo "📄 详细结果保存至: $SUMMARY_FILE"

# 如果有紧急活动，设置退出码10（用于触发警报）
if [ "$HAS_URGENT_ACTIVITY" = true ]; then
    exit 10
fi

exit 0
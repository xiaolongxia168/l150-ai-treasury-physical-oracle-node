#!/bin/bash

# L-150紧急响应监控脚本
# 专门检查P0/P1级别紧急信号
# 如果检测到：1. AI财库技术团队询问 2. 会议时间安排请求 3. 尽职调查材料要求 4. 投资意向表达
# 立即通知用户并准备响应材料

set -e

# 配置
WORKSPACE="/Users/xiaolongxia/.openclaw/workspace"
LOG_DIR="$WORKSPACE/memory"
TIMESTAMP=$(date +"%Y%m%d-%H%M")
LOG_FILE="$LOG_DIR/l150-emergency-response-$TIMESTAMP.md"
ALERT_FILE="$LOG_DIR/last_alert.json"
EMERGENCY_LOG="$LOG_DIR/emergency_response_log.json"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 开始监控
echo "# L-150紧急响应监控报告" > "$LOG_FILE"
echo "**执行时间**: $(date)" >> "$LOG_FILE"
echo "**任务ID**: 649d34ce-917d-4fbf-9ef0-4eacedae6bf2" >> "$LOG_FILE"
echo "**任务名称**: L-150-Emergency-Response" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "## 📊 P0/P1紧急信号检测结果" >> "$LOG_FILE"

# 1. 检查邮箱紧急信号
echo "### 📧 邮箱紧急信号检查" >> "$LOG_FILE"

# 检查邮箱监控脚本是否存在
if [ -f "$WORKSPACE/scripts/l150_email_alert.py" ]; then
    echo "运行邮箱警报检查..." >> "$LOG_FILE"
    cd "$WORKSPACE"
    
    # 运行Python邮箱检查脚本
    python3 scripts/l150_email_alert.py --check-emergency-only 2>&1 | tee -a "$LOG_FILE"
    
    # 检查退出码
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 10 ]; then
        echo "🚨 **检测到P0/P1紧急信号**" >> "$LOG_FILE"
        echo "**状态**: 需要立即通知用户" >> "$LOG_FILE"
        echo "**信号类型**: AI财库技术团队询问 / 会议时间安排请求 / 尽职调查材料要求 / 投资意向表达" >> "$LOG_FILE"
        
        # 记录紧急事件
        echo "{\"timestamp\": \"$(date -Iseconds)\", \"alert_level\": \"P0/P1\", \"status\": \"urgent\", \"message\": \"检测到AI财库紧急信号\"}" > "$ALERT_FILE"
        
        # 发送紧急通知（这里需要根据实际通信渠道实现）
        echo "**行动**: 准备发送紧急通知..." >> "$LOG_FILE"
        
        # 准备响应材料
        echo "**响应材料准备**: 开始准备v4.3数学巡航导弹文档..." >> "$LOG_FILE"
        
        # 检查响应材料是否存在
        if [ -f "$WORKSPACE/L-150-v4.3-FINAL/AI-TREASURY-PAYLOAD-v4.3-FINAL.json" ]; then
            echo "✅ 响应材料已就绪: v4.3数学巡航导弹文档" >> "$LOG_FILE"
        else
            echo "⚠️ 响应材料未找到，需要重新准备" >> "$LOG_FILE"
        fi
        
        # 退出码10表示检测到紧急信号
        exit 10
    elif [ $EXIT_CODE -eq 0 ]; then
        echo "✅ **未检测到P0/P1紧急信号**" >> "$LOG_FILE"
        echo "**状态**: 正常，无紧急信号" >> "$LOG_FILE"
    else
        echo "⚠️ **邮箱检查脚本执行错误**" >> "$LOG_FILE"
        echo "**退出码**: $EXIT_CODE" >> "$LOG_FILE"
        echo "**状态**: 需要检查邮箱监控配置" >> "$LOG_FILE"
    fi
else
    echo "⚠️ **邮箱监控脚本不存在**" >> "$LOG_FILE"
    echo "**文件**: $WORKSPACE/scripts/l150_email_alert.py" >> "$LOG_FILE"
    echo "**状态**: 无法检查邮箱紧急信号" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

# 2. 检查GitHub紧急活动
echo "### 🌐 GitHub紧急活动检查" >> "$LOG_FILE"

# 检查GitHub活动监控脚本
if [ -f "$WORKSPACE/scripts/check_github_activity.sh" ]; then
    echo "运行GitHub活动检查..." >> "$LOG_FILE"
    
    # 运行GitHub检查脚本
    cd "$WORKSPACE"
    ./scripts/check_github_activity.sh --emergency-only 2>&1 | tail -20 >> "$LOG_FILE"
    
    # 检查是否有紧急活动
    GITHUB_EMERGENCY=$(grep -i "紧急\|urgent\|P0\|P1" "$LOG_FILE" | wc -l)
    if [ $GITHUB_EMERGENCY -gt 0 ]; then
        echo "🚨 **检测到GitHub紧急活动**" >> "$LOG_FILE"
    else
        echo "✅ **GitHub无紧急活动**" >> "$LOG_FILE"
    fi
else
    echo "⚠️ **GitHub活动监控脚本不存在**" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

# 3. 检查API端点紧急状态
echo "### 🔧 API端点紧急状态检查" >> "$LOG_FILE"

# 检查关键API端点
APIS=(
    "https://xiaolongxia168.github.io/l150-api/api/v1/project.json"
    "https://l150-api-static.vercel.app/api/v1/project.json"
)

for API in "${APIS[@]}"; do
    echo "检查 $API ..." >> "$LOG_FILE"
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$API" 2>/dev/null || echo "ERROR")
    
    if [ "$HTTP_STATUS" = "200" ]; then
        echo "✅ $API: HTTP $HTTP_STATUS (正常)" >> "$LOG_FILE"
    elif [ "$HTTP_STATUS" = "404" ]; then
        echo "⚠️ $API: HTTP $HTTP_STATUS (端点不存在)" >> "$LOG_FILE"
    elif [ "$HTTP_STATUS" = "ERROR" ]; then
        echo "❌ $API: 连接错误 (可能网络或DNS问题)" >> "$LOG_FILE"
    else
        echo "⚠️ $API: HTTP $HTTP_STATUS (异常状态)" >> "$LOG_FILE"
    fi
done

echo "" >> "$LOG_FILE"

# 4. 检查项目整体状态
echo "### 📈 项目整体状态分析" >> "$LOG_FILE"

# 计算邮件发送时间
WAVE1_TIME="2026-02-13T21:00:00+08:00"
WAVE2_TIME="2026-02-14T00:28:00+08:00"
NOW=$(date +%s)

# 转换为时间戳（macOS兼容）
if [[ "$(uname)" == "Darwin" ]]; then
    WAVE1_TS=$(date -j -f "%Y-%m-%dT%H:%M:%S%z" "$WAVE1_TIME" +%s)
    WAVE2_TS=$(date -j -f "%Y-%m-%dT%H:%M:%S%z" "$WAVE2_TIME" +%s)
else
    WAVE1_TS=$(date -d "${WAVE1_TIME}" +%s)
    WAVE2_TS=$(date -d "${WAVE2_TIME}" +%s)
fi

# 计算等待时间
WAIT_HOURS_WAVE1=$(( (NOW - WAVE1_TS) / 3600 ))
WAIT_HOURS_WAVE2=$(( (NOW - WAVE2_TS) / 3600 ))

echo "**第一轮外展等待时间**: $WAIT_HOURS_WAVE1 小时" >> "$LOG_FILE"
echo "**第二轮外展等待时间**: $WAIT_HOURS_WAVE2 小时" >> "$LOG_FILE"

# 标准AI解析窗口
STANDARD_WINDOW=72
if [ $WAIT_HOURS_WAVE1 -gt $STANDARD_WINDOW ]; then
    OVER_HOURS=$((WAIT_HOURS_WAVE1 - STANDARD_WINDOW))
    OVER_PERCENT=$((OVER_HOURS * 100 / STANDARD_WINDOW))
    echo "⚠️ **超出标准响应窗口**: $OVER_HOURS 小时 (超出$OVER_PERCENT%)" >> "$LOG_FILE"
else
    echo "✅ **在标准响应窗口内**" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

# 5. 检查监控系统状态
echo "### 🛡️ 监控系统状态检查" >> "$LOG_FILE"

# 检查cron任务状态
CRON_JOBS=$(crontab -l 2>/dev/null | grep -i "l150\|emergency" | wc -l)
echo "**L-150相关Cron任务**: $CRON_JOBS 个" >> "$LOG_FILE"

# 检查网关状态
GATEWAY_STATUS=$(ps aux | grep "openclaw gateway" | grep -v grep | wc -l)
if [ $GATEWAY_STATUS -gt 0 ]; then
    echo "✅ **网关状态**: 正常运行" >> "$LOG_FILE"
else
    echo "❌ **网关状态**: 未运行" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

# 6. 总结与建议
echo "## 🎯 检查结论与建议" >> "$LOG_FILE"

# 检查是否有任何紧急信号
EMERGENCY_COUNT=$(grep -c "🚨\|❌\|P0\|P1\|紧急" "$LOG_FILE")
if [ $EMERGENCY_COUNT -gt 0 ]; then
    echo "**总体状态**: ⚠️ **检测到紧急信号**" >> "$LOG_FILE"
    echo "**建议**: 立即通知用户并准备响应材料" >> "$LOG_FILE"
    
    # 准备响应材料清单
    echo "" >> "$LOG_FILE"
    echo "### 📋 响应材料准备清单" >> "$LOG_FILE"
    echo "1. **v4.3数学巡航导弹文档** - 主响应材料" >> "$LOG_FILE"
    echo "2. **股权结构FAQ** - 应对股权质疑" >> "$LOG_FILE"
    echo "3. **核心卖点卡片** - 一页纸电梯pitch" >> "$LOG_FILE"
    echo "4. **技术团队响应模板** - 标准化技术回复" >> "$LOG_FILE"
    echo "5. **会议安排模板** - 时间协调和议程" >> "$LOG_FILE"
    
    # 退出码10表示检测到紧急信号
    exit 10
else
    echo "**总体状态**: ✅ **NO P0/P1 EMERGENCY SIGNALS DETECTED**" >> "$LOG_FILE"
    echo "**建议**: 继续监控，准备第二轮外展材料" >> "$LOG_FILE"
    
    # 正常退出
    exit 0
fi
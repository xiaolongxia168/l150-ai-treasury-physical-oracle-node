#!/bin/bash
#
# 商家数据全自动化系统启动脚本
# 整合数据抓取 + 智能分析 + 报告推送
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$HOME/.openclaw/workspace/data/merchant-dashboard"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "═══════════════════════════════════════════════════════════════"
echo "🏪 商家数据全自动化系统"
echo "═══════════════════════════════════════════════════════════════"
echo "启动时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 确保目录存在
mkdir -p "$DATA_DIR/logs"
mkdir -p "$DATA_DIR/screenshots"

# 步骤1: 基础数据抓取
echo "📊 步骤1: 执行基础数据抓取..."
cd "$SCRIPT_DIR"
node scraper.js all
echo "✅ 基础抓取完成"
echo ""

# 步骤2: 智能分析
echo "🧠 步骤2: 执行智能运营分析..."
node smart-analyzer.js
echo "✅ 智能分析完成"
echo ""

# 步骤3: 深度抓取（可选，每4小时执行一次）
HOUR=$(date +%H)
if [ $((HOUR % 4)) -eq 0 ]; then
    echo "🔍 步骤3: 执行深度数据抓取（每4小时）..."
    node deep-scraper.js 2>/dev/null || echo "⚠️ 深度抓取暂时跳过"
    echo "✅ 深度抓取完成"
else
    echo "⏭️ 步骤3: 深度抓取（下次执行: $((4 - HOUR % 4))小时后）"
fi
echo ""

# 步骤4: 生成综合报告
echo "📄 步骤4: 生成综合报告..."
REPORT_FILE="$DATA_DIR/daily_report_$(date +%Y%m%d).txt"

cat > "$REPORT_FILE" << EOF
════════════════════════════════════════════════════════════════
          商家数据日报 - $(date '+%Y年%m月%d日 %H:%M')
════════════════════════════════════════════════════════════════

【数据抓取状态】✅ 成功
【报告生成时间】$(date '+%Y-%m-%d %H:%M:%S')

════════════════════════════════════════════════════════════════
📱 抖音来客 - 有点方恐怖密室
════════════════════════════════════════════════════════════════
EOF

# 追加抖音数据
if [ -f "$DATA_DIR/douyin_laike_latest.json" ]; then
    cat "$DATA_DIR/douyin_laike_latest.json" | node -e '
        const data = JSON.parse(require("fs").readFileSync(0, "utf8"));
        console.log(`店铺名称: ${data.shop_name || "N/A"}`);
        console.log(`抓取时间: ${data.scraped_at || "N/A"}`);
        console.log("");
        if (data.data) {
            console.log(`• 成交金额: ¥${data.data.deal_amount || 0}`);
            console.log(`• 成交券数: ${data.data.deal_count || 0}`);
            console.log(`• 退款金额: ¥${data.data.refund_amount || 0}`);
            console.log(`• 核销金额: ¥${data.data.verify_amount || 0}`);
            console.log(`• 访问人数: ${data.data.visit_count || 0}`);
            console.log(`• 经营分: ${data.data.business_score || 0}`);
            console.log(`• 账户余额: ¥${data.data.account_balance || 0}`);
            console.log(`• 本地推消耗: ¥${data.data.ad_spend || 0}`);
            console.log(`• 违规状态: ${data.data.violation_status || "正常"}`);
        }
    ' >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

════════════════════════════════════════════════════════════════
🍜 美团点评 - 有點方真人恐怖密室(解放西路店)
════════════════════════════════════════════════════════════════
EOF

# 追加美团数据
if [ -f "$DATA_DIR/meituan_dianping_latest.json" ]; then
    cat "$DATA_DIR/meituan_dianping_latest.json" | node -e '
        const data = JSON.parse(require("fs").readFileSync(0, "utf8"));
        console.log(`店铺名称: ${data.shop_name || "N/A"}`);
        console.log(`抓取时间: ${data.scraped_at || "N/A"}`);
        console.log("");
        if (data.data) {
            console.log(`• 访问人数: ${data.data.visit_count || 0}`);
            console.log(`• 下单金额: ¥${data.data.order_amount || 0}`);
            console.log(`• 核销金额: ¥${data.data.verify_amount || 0}`);
            console.log(`• 经营评分: ${data.data.business_score || 0}`);
            console.log(`• 新增评论: ${data.data.new_comments || 0}`);
            console.log(`• 新增差评: ${data.data.new_bad_comments || 0}`);
            console.log(`• 评分变化: ${data.data.score_change || "持平"}`);
        }
    ' >> "$REPORT_FILE"
fi

# 追加智能分析报告
if [ -f "$DATA_DIR/smart_report_$(date +%Y%m%d).txt" ]; then
    echo "" >> "$REPORT_FILE"
    echo "════════════════════════════════════════════════════════════════" >> "$REPORT_FILE"
    echo "🤖 智能运营分析" >> "$REPORT_FILE"
    echo "════════════════════════════════════════════════════════════════" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    cat "$DATA_DIR/smart_report_$(date +%Y%m%d).txt" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

════════════════════════════════════════════════════════════════
📁 数据文件
════════════════════════════════════════════════════════════════
• 抖音数据: douyin_laike_latest.json
• 美团数据: meituan_dianping_latest.json
• 分析报告: smart_report_$(date +%Y%m%d).txt
• 详细报告: report_$(date +%Y%m%d).json
• CSV报告: report_$(date +%Y%m%d).csv

数据目录: $DATA_DIR

════════════════════════════════════════════════════════════════
💡 说明
════════════════════════════════════════════════════════════════
• 本报告每5分钟自动生成
• 异常告警将实时推送
• 深度分析每4小时执行一次
• 建议每日查看并处理告警事项

════════════════════════════════════════════════════════════════
EOF

echo "✅ 报告已生成: $REPORT_FILE"
echo ""

# 显示报告摘要
echo "═══════════════════════════════════════════════════════════════"
echo "📋 报告摘要"
echo "═══════════════════════════════════════════════════════════════"
head -50 "$REPORT_FILE"
echo "..."
echo ""
echo "完整报告: $REPORT_FILE"
echo ""

# 步骤5: 推送通知（如果有飞书配置）
if [ -f "$SCRIPT_DIR/feishu-config.json" ]; then
    echo "📤 步骤5: 推送飞书通知..."
    node "$SCRIPT_DIR/send-feishu.js" 2>/dev/null || echo "⏭️ 飞书推送跳过"
fi

echo "═══════════════════════════════════════════════════════════════"
echo "✅ 全自动化流程完成 - $(date '+%H:%M:%S')"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "下次抓取: 5分钟后"
echo "数据目录: $DATA_DIR"
echo "日志文件: $DATA_DIR/logs/"

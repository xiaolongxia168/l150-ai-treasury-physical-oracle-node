#!/bin/bash
#
# 商家平台超级自动化运营系统 - 快速启动脚本
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "
╔══════════════════════════════════════════════════════════════════╗
║         🚀 商家平台超级自动化运营系统                             ║
║         一键启动全功能采集与监控                                  ║
╚══════════════════════════════════════════════════════════════════╝
"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查依赖
check_dependencies() {
    log_info "检查系统依赖..."
    
    # 检查 Node.js
    if ! command -v node &> /dev/null; then
        log_error "Node.js 未安装，请先安装 Node.js 18+"
        exit 1
    fi
    
    # 检查 curl
    if ! command -v curl &> /dev/null; then
        log_error "curl 未安装"
        exit 1
    fi
    
    log_success "依赖检查通过"
}

# 显示菜单
show_menu() {
    echo "
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 主菜单
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【数据采集】
  1) 运行完整采集 (抖音+美团)
  2) 仅采集抖音来客
  3) 仅采集美团开店宝
  4) 探索向导 (查看功能模块)

【实时监控】
  5) 查看最新数据
  6) 查看异常告警
  7) 生成数据报告

【系统管理】
  8) 查看采集日志
  9) 配置定时任务
  0) 退出

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"
}

# 运行完整采集
run_full_scrape() {
    log_info "启动完整采集..."
    node scraper-v2.js all
}

# 仅采集抖音
run_douyin_only() {
    log_info "启动抖音来客采集..."
    node scraper-v2.js douyin
}

# 仅采集美团
run_meituan_only() {
    log_info "启动美团开店宝采集..."
    node scraper-v2.js meituan
}

# 显示探索向导
show_explore_guide() {
    bash explore-guide.sh all
}

# 查看最新数据
view_latest_data() {
    DATA_DIR="$HOME/.openclaw/workspace/data/merchant-dashboard"
    
    echo "
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 最新采集数据
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"
    
    # 抖音数据
    if [ -f "$DATA_DIR/douyin_full_latest.json" ]; then
        echo "📱 抖音来客数据:"
        node -e "
            const data = require('$DATA_DIR/douyin_full_latest.json');
            const dash = data.modules?.dashboard?.data || {};
            console.log('  💰 成交金额: ¥' + (dash.deal_amount || 0));
            console.log('  🎫 成交券数: ' + (dash.deal_count || 0));
            console.log('  💳 账户余额: ¥' + (dash.account_balance || 0));
            console.log('  ⭐ 经营分: ' + (dash.business_score || 0));
            console.log('  ⚠️  违规: ' + (dash.violation_status || '正常'));
        "
    else
        log_warn "抖音数据文件不存在，请先运行采集"
    fi
    
    echo ""
    
    # 美团数据
    if [ -f "$DATA_DIR/meituan_full_latest.json" ]; then
        echo "🍜 美团点评数据:"
        node -e "
            const data = require('$DATA_DIR/meituan_full_latest.json');
            const dash = data.modules?.dashboard?.data || {};
            console.log('  👁️ 访问人数: ' + (dash.visit_count || 0));
            console.log('  ⭐ 经营评分: ' + (dash.business_score || 0));
            console.log('  💬 新增评论: ' + (dash.new_comments || 0));
            console.log('  👎 新增差评: ' + (dash.new_bad_comments || 0));
        "
    else
        log_warn "美团数据文件不存在，请先运行采集"
    fi
    
    echo ""
}

# 查看异常告警
view_alerts() {
    DATA_DIR="$HOME/.openclaw/workspace/data/merchant-dashboard"
    REPORT_FILE="$DATA_DIR/full_report_$(date +%Y-%m-%d).json"
    
    echo "
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 异常告警
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"
    
    if [ -f "$REPORT_FILE" ]; then
        node -e "
            const report = require('$REPORT_FILE');
            const alerts = report.summary?.alerts || [];
            if (alerts.length === 0) {
                console.log('✅ 暂无异常告警');
            } else {
                alerts.forEach(alert => {
                    const icon = alert.level === 'critical' ? '🔴' : '🟡';
                    console.log(icon + ' [' + alert.platform + '] ' + alert.message);
                });
            }
        "
    else
        log_warn "报告文件不存在，请先运行采集"
    fi
    
    echo ""
}

# 生成报告
generate_report() {
    log_info "生成数据报告..."
    
    DATA_DIR="$HOME/.openclaw/workspace/data/merchant-dashboard"
    REPORT_FILE="$DATA_DIR/full_report_$(date +%Y-%m-%d).json"
    
    if [ -f "$REPORT_FILE" ]; then
        echo "
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 数据报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"
        node -e "
            const report = require('$REPORT_FILE');
            console.log('报告生成时间:', report.generated_at);
            console.log('');
            console.log('抖音来客模块:');
            Object.keys(report.douyin?.modules || {}).forEach(key => {
                const mod = report.douyin.modules[key];
                const dataCount = Object.keys(mod.data || {}).length;
                console.log('  ✓', mod.name, '-', dataCount, '个数据字段');
            });
            console.log('');
            console.log('美团点评模块:');
            Object.keys(report.meituan?.modules || {}).forEach(key => {
                const mod = report.meituan.modules[key];
                const dataCount = Object.keys(mod.data || {}).length;
                console.log('  ✓', mod.name, '-', dataCount, '个数据字段');
            });
        "
        
        echo ""
        log_success "报告文件: $REPORT_FILE"
    else
        log_error "报告文件不存在"
    fi
    
    echo ""
}

# 查看日志
view_logs() {
    LOGS_DIR="$HOME/.openclaw/workspace/data/merchant-dashboard/logs"
    
    echo "
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 采集日志
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"
    
    if [ -d "$LOGS_DIR" ]; then
        echo "可用日志文件:"
        ls -lah "$LOGS_DIR"/*.log 2>/dev/null | tail -5 | awk '{print "  " $9 " (" $5 ")"}'
        echo ""
        
        LATEST_LOG=$(ls -t "$LOGS_DIR"/*.log 2>/dev/null | head -1)
        if [ -n "$LATEST_LOG" ]; then
            echo "最新日志内容 (最后20行):"
            echo "---"
            tail -20 "$LATEST_LOG"
            echo "---"
        fi
    else
        log_warn "日志目录不存在"
    fi
    
    echo ""
}

# 配置定时任务
setup_cron() {
    echo "
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ 配置定时任务
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

建议的定时任务配置:

# 每5分钟实时采集
*/5 * * * * cd $SCRIPT_DIR && node scraper-v2.js all >> /tmp/merchant-scraper-cron.log 2>&1

# 每小时生成趋势报告
0 * * * * cd $SCRIPT_DIR && node generate-hourly-report.js >> /tmp/merchant-report-cron.log 2>&1

# 每日9点生成完整日报
0 9 * * * cd $SCRIPT_DIR && node generate-daily-report.js >> /tmp/merchant-daily-cron.log 2>&1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"
    
    read -p "是否自动添加定时任务? (y/n): " confirm
    if [ "$confirm" = "y" ]; then
        CRON_CMD="*/5 * * * * cd $SCRIPT_DIR && node scraper-v2.js all >> /tmp/merchant-scraper-cron.log 2>&1"
        (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
        log_success "定时任务已添加"
    else
        log_info "已取消"
    fi
    
    echo ""
}

# 主循环
main() {
    check_dependencies
    
    while true; do
        show_menu
        read -p "请选择操作 [0-9]: " choice
        
        case $choice in
            1) run_full_scrape ;;
            2) run_douyin_only ;;
            3) run_meituan_only ;;
            4) show_explore_guide ;;
            5) view_latest_data ;;
            6) view_alerts ;;
            7) generate_report ;;
            8) view_logs ;;
            9) setup_cron ;;
            0) 
                echo "
感谢使用，再见! 👋
"
                exit 0 
                ;;
            *) 
                log_error "无效选项，请重新选择"
                ;;
        esac
        
        echo ""
        read -p "按下回车键继续..."
    done
}

# 运行
main "$@"

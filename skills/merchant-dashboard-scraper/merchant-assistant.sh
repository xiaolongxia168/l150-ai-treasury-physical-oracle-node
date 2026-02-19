#!/bin/bash
#
# 商家运营智能助手 - 统一入口
# Usage: ./merchant-assistant.sh [command]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$HOME/.openclaw/workspace/data/merchant-dashboard"
SKILL_DIR="$HOME/.openclaw/workspace/skills/merchant-dashboard-scraper"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 显示帮助
show_help() {
    cat << 'EOF'
╔════════════════════════════════════════════════════════════════╗
║           商家运营智能助手 - 命令行工具                          ║
╚════════════════════════════════════════════════════════════════╝

使用方式: ./merchant-assistant.sh <命令>

📊 数据抓取命令:
  quick         快速抓取基础数据 (每5分钟执行)
  deep          深度抓取全维度数据 (进入各功能模块)
  douyin        仅抓取抖音来客
  meituan       仅抓取美团点评

🤖 智能分析命令:
  analyze       运行智能运营分析
  report        生成完整运营报告
  dashboard     生成可视化仪表板

⚙️ 系统管理命令:
  install       安装依赖和初始化
  status        查看系统状态
  logs          查看实时日志
  cron-setup    配置自动化任务
  cron-list     查看定时任务列表
  cron-remove   移除所有定时任务

💡 示例:
  ./merchant-assistant.sh quick      # 快速抓取
  ./merchant-assistant.sh analyze    # 运行分析
  ./merchant-assistant.sh report     # 生成报告

EOF
}

# 安装依赖
install_deps() {
    log_info "安装依赖..."
    
    cd "$SKILL_DIR"
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        log_error "Node.js 未安装，请先安装 Node.js 18+"
        exit 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        log_warn "Node.js 版本较低，建议升级到 18+"
    fi
    
    # 安装npm依赖
    if [ ! -d "node_modules" ]; then
        log_info "安装 npm 依赖..."
        npm install playwright-core
    fi
    
    # 创建必要目录
    mkdir -p "$DATA_DIR"/{logs,screenshots,reports}
    
    # 设置权限
    chmod +x "$SKILL_DIR"/*.js
    chmod +x "$SKILL_DIR"/*.sh
    
    log_success "安装完成！"
}

# 快速抓取
quick_scrape() {
    log_info "开始快速数据抓取..."
    node "$SKILL_DIR/scraper.js" all
    log_success "快速抓取完成"
}

# 深度抓取
deep_scrape() {
    log_info "开始深度数据抓取 (进入各功能模块)..."
    log_warn "此操作可能需要 2-3 分钟，请耐心等待"
    node "$SKILL_DIR/deep-scraper.js" all
    log_success "深度抓取完成"
}

# 运行分析
run_analyze() {
    log_info "运行智能运营分析..."
    node "$SKILL_DIR/analyzer.js"
}

# 生成完整报告
generate_report() {
    log_info "生成完整运营报告..."
    
    # 1. 先抓取最新数据
    quick_scrape
    
    # 2. 运行分析
    run_analyze
    
    # 3. 显示最新报告
    LATEST_REPORT=$(ls -t "$DATA_DIR"/analysis_report_*.txt 2>/dev/null | head -1)
    if [ -n "$LATEST_REPORT" ]; then
        echo ""
        cat "$LATEST_REPORT"
    fi
    
    log_success "报告生成完成"
}

# 查看状态
show_status() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                   系统状态监控                                  ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    
    # 检查数据文件
    echo "📁 数据文件状态:"
    if [ -f "$DATA_DIR/douyin_laike_latest.json" ]; then
        DOUYIN_TIME=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$DATA_DIR/douyin_laike_latest.json" 2>/dev/null || stat -c "%y" "$DATA_DIR/douyin_laike_latest.json" 2>/dev/null | cut -d'.' -f1)
        echo "  ✅ 抖音数据: $DOUYIN_TIME"
    else
        echo "  ❌ 抖音数据: 未找到"
    fi
    
    if [ -f "$DATA_DIR/meituan_dianping_latest.json" ]; then
        MEITUAN_TIME=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$DATA_DIR/meituan_dianping_latest.json" 2>/dev/null || stat -c "%y" "$DATA_DIR/meituan_dianping_latest.json" 2>/dev/null | cut -d'.' -f1)
        echo "  ✅ 美团数据: $MEITUAN_TIME"
    else
        echo "  ❌ 美团数据: 未找到"
    fi
    
    # 检查最新报告
    echo ""
    echo "📊 最新分析报告:"
    LATEST_REPORT=$(ls -t "$DATA_DIR"/analysis_report_*.txt 2>/dev/null | head -1)
    if [ -n "$LATEST_REPORT" ]; then
        REPORT_TIME=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$LATEST_REPORT" 2>/dev/null || stat -c "%y" "$LATEST_REPORT" 2>/dev/null | cut -d'.' -f1)
        echo "  ✅ $REPORT_TIME"
    else
        echo "  ❌ 暂无分析报告"
    fi
    
    # 检查定时任务
    echo ""
    echo "⏰ 定时任务状态:"
    if command -v openclaw &> /dev/null; then
        openclaw cron list 2>/dev/null | grep -E "(商家|merchant)" || echo "  ℹ️ 暂无商家数据定时任务"
    else
        echo "  ⚠️ openclaw 命令不可用"
    fi
    
    echo ""
}

# 查看日志
show_logs() {
    LOG_FILE="$DATA_DIR/logs/scraper_$(date +%Y-%m-%d).log"
    if [ -f "$LOG_FILE" ]; then
        log_info "显示日志 (按 Ctrl+C 退出):"
        tail -f "$LOG_FILE"
    else
        log_warn "今日日志文件不存在: $LOG_FILE"
    fi
}

# 配置自动化任务
setup_cron() {
    log_info "配置自动化任务..."
    
    SKILL_DIR_ESCAPED=$(echo "$SKILL_DIR" | sed 's/\//\\\//g')
    
    # 1. 每5分钟快速抓取
    log_info "添加: 每5分钟快速抓取"
    openclaw cron add \
        --name "商家数据-快速抓取" \
        --schedule "*/5 * * * *" \
        --command "node ${SKILL_DIR}/scraper.js all" \
        2>/dev/null || log_warn "任务可能已存在"
    
    # 2. 每小时深度抓取
    log_info "添加: 每小时深度分析"
    openclaw cron add \
        --name "商家数据-深度分析" \
        --schedule "0 * * * *" \
        --command "node ${SKILL_DIR}/deep-scraper.js all && node ${SKILL_DIR}/analyzer.js" \
        2>/dev/null || log_warn "任务可能已存在"
    
    # 3. 每日9点完整报告
    log_info "添加: 每日9点完整报告"
    openclaw cron add \
        --name "商家数据-日报" \
        --schedule "0 9 * * *" \
        --command "bash ${SKILL_DIR}/merchant-assistant.sh report" \
        2>/dev/null || log_warn "任务可能已存在"
    
    log_success "自动化任务配置完成！"
    log_info "当前定时任务列表:"
    openclaw cron list 2>/dev/null | grep -E "(商家|merchant)" || echo "  暂无任务"
}

# 移除定时任务
remove_cron() {
    log_warn "移除所有商家数据定时任务..."
    
    openclaw cron list 2>/dev/null | grep -E "(商家|merchant)" | while read line; do
        JOB_ID=$(echo "$line" | awk '{print $1}')
        if [ -n "$JOB_ID" ]; then
            log_info "移除任务: $JOB_ID"
            openclaw cron remove "$JOB_ID" 2>/dev/null || true
        fi
    done
    
    log_success "定时任务已移除"
}

# 主命令处理
case "${1:-help}" in
    quick)
        quick_scrape
        ;;
    deep)
        deep_scrape
        ;;
    douyin)
        log_info "抓取抖音来客..."
        node "$SKILL_DIR/scraper.js" douyin
        ;;
    meituan)
        log_info "抓取美团点评..."
        node "$SKILL_DIR/scraper.js" meituan
        ;;
    analyze)
        run_analyze
        ;;
    report)
        generate_report
        ;;
    install)
        install_deps
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    cron-setup)
        setup_cron
        ;;
    cron-list)
        openclaw cron list 2>/dev/null | grep -E "(商家|merchant)" || echo "暂无商家数据任务"
        ;;
    cron-remove)
        remove_cron
        ;;
    help|--help|-h|*)
        show_help
        ;;
esac

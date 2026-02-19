#!/usr/bin/env node
/**
 * 智能运营分析引擎
 * 自动诊断店铺问题并生成优化建议
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(process.env.HOME, '.openclaw/workspace/data/merchant-dashboard');

/**
 * 运营分析师类
 */
class OperationsAnalyzer {
    constructor() {
        this.issues = [];
        this.suggestions = [];
        this.opportunities = [];
    }

    /**
     * 加载数据
     */
    loadData() {
        const douyinFile = path.join(DATA_DIR, 'douyin_laike_latest.json');
        const meituanFile = path.join(DATA_DIR, 'meituan_dianping_latest.json');
        
        const data = {
            douyin: fs.existsSync(douyinFile) ? JSON.parse(fs.readFileSync(douyinFile)) : null,
            meituan: fs.existsSync(meituanFile) ? JSON.parse(fs.readFileSync(meituanFile)) : null
        };
        
        return data;
    }

    /**
     * 执行完整分析
     */
    analyze(data) {
        console.log('\n🔍 开始智能运营分析...\n');
        
        if (data.douyin) {
            this.analyzeDouyin(data.douyin);
        }
        
        if (data.meituan) {
            this.analyzeMeituan(data.meituan);
        }
        
        this.generateCrossPlatformInsights(data);
        
        return {
            issues: this.issues,
            suggestions: this.suggestions,
            opportunities: this.opportunities,
            summary: this.generateSummary()
        };
    }

    /**
     * 分析抖音来客数据
     */
    analyzeDouyin(data) {
        const d = data.data || data;
        
        // 1. 违规状态检查
        if (d.violation_status && d.violation_status.includes('违规')) {
            this.issues.push({
                platform: '抖音来客',
                level: 'critical',
                title: '⚠️ 违规生效中',
                description: `店铺存在违规记录: ${d.violation_status}`,
                impact: '可能影响流量分配和曝光',
                action: '立即查看违规详情，按要求整改'
            });
        }
        
        // 2. 退款率分析
        if (d.deal_amount > 0 && d.refund_amount > 0) {
            const refundRate = (d.refund_amount / d.deal_amount * 100).toFixed(1);
            if (refundRate > 20) {
                this.issues.push({
                    platform: '抖音来客',
                    level: 'warning',
                    title: '📉 退款率偏高',
                    description: `今日退款率 ${refundRate}% (¥${d.refund_amount}/¥${d.deal_amount})`,
                    impact: '影响收入和店铺评分',
                    action: '分析退款原因，优化商品描述和服务流程'
                });
            }
        }
        
        // 3. 转化率分析
        if (d.visit_count > 0 && d.deal_count > 0) {
            const conversionRate = (d.deal_count / d.visit_count * 100).toFixed(2);
            if (conversionRate < 2) {
                this.issues.push({
                    platform: '抖音来客',
                    level: 'warning',
                    title: '📉 转化率偏低',
                    description: `访问-成交转化率 ${conversionRate}% (${d.deal_count}单/${d.visit_count}访问)`,
                    impact: '流量浪费，收入损失',
                    action: '优化商品详情页，增加促销活动和用户评价展示'
                });
            } else if (conversionRate > 8) {
                this.opportunities.push({
                    platform: '抖音来客',
                    title: '🚀 转化表现优秀',
                    description: `转化率 ${conversionRate}% 高于行业均值`,
                    suggestion: '加大推广投入，扩大流量获取'
                });
            }
        }
        
        // 4. 账户余额检查
        if (d.account_balance < 500) {
            this.issues.push({
                platform: '抖音来客',
                level: 'warning',
                title: '💰 账户余额偏低',
                description: `当前余额 ¥${d.account_balance}`,
                impact: '可能影响正常提现和运营',
                action: '关注结算周期，确保资金充足'
            });
        }
        
        // 5. 经营分分析
        if (d.business_score) {
            if (d.business_score < 120) {
                this.issues.push({
                    platform: '抖音来客',
                    level: 'warning',
                    title: '📊 经营分偏低',
                    description: `当前经营分 ${d.business_score}分`,
                    impact: '影响搜索排名和流量分配',
                    action: '提升服务质量，增加好评数量，提高核销率'
                });
            } else if (d.business_score > 150) {
                this.opportunities.push({
                    platform: '抖音来客',
                    title: '⭐ 经营分优秀',
                    description: `经营分 ${d.business_score}分，高于平均水平`,
                    suggestion: '保持现有运营水平，可申请更多平台资源'
                });
            }
        }
        
        // 6. 本地推分析
        if (d.ad_spend === 0) {
            this.suggestions.push({
                platform: '抖音来客',
                category: '推广建议',
                title: '💡 未投放本地推广告',
                description: '当前无广告投入，完全依赖自然流量',
                suggestion: '建议投放本地推广告，预算¥50-100/天，可提升50-100%曝光量',
                expected_impact: '预计日访问量从22人提升至40-60人'
            });
        }
        
        // 7. 咨询响应检查
        if (d.consultation_count > 0) {
            this.suggestions.push({
                platform: '抖音来客',
                category: '客服优化',
                title: '💬 有客户咨询待跟进',
                description: `${d.consultation_count}条客户咨询`,
                suggestion: '及时回复咨询，转化率可提升20-30%',
                expected_impact: '预计增加1-2单成交'
            });
        }
    }

    /**
     * 分析美团点评数据
     */
    analyzeMeituan(data) {
        const m = data.data || data;
        
        // 1. 评分危机检查
        if (m.business_score < 60) {
            this.issues.push({
                platform: '美团点评',
                level: 'critical',
                title: '🚨 评分严重偏低',
                description: `经营评分仅 ${m.business_score}分（及格线60分）`,
                impact: '严重影响搜索排名和顾客转化率',
                action: '紧急处理：1)回复所有差评 2)联系差评用户 3)改善服务问题'
            });
        } else if (m.business_score < 65) {
            this.issues.push({
                platform: '美团点评',
                level: 'warning',
                title: '⚠️ 评分偏低',
                description: `经营评分 ${m.business_score}分，低于商圈均值`,
                impact: '影响竞争力，顾客可能选择评分更高的竞品',
                action: '主动邀请满意顾客评价，提升评分'
            });
        }
        
        // 2. 转化率分析（访问→下单）
        if (m.visit_count > 0 && m.order_amount === 0) {
            this.issues.push({
                platform: '美团点评',
                level: 'warning',
                title: '📉 有访问无转化',
                description: `今日${m.visit_count}人访问，但无下单`,
                impact: '流量浪费，获客成本高',
                action: '检查商品价格和套餐设置，优化店铺装修'
            });
        }
        
        // 3. 通知积压检查
        if (m.notice_count > 50) {
            this.suggestions.push({
                platform: '美团点评',
                category: '日常运营',
                title: '📬 通知积压较多',
                description: `有${m.notice_count}条未读通知`,
                suggestion: '定期清理通知，关注平台活动和政策更新',
                expected_impact: '避免错过重要信息和活动机会'
            });
        }
        
        // 4. 差评监控
        if (m.new_bad_comments > 0) {
            this.issues.push({
                platform: '美团点评',
                level: 'warning',
                title: '👎 新增差评',
                description: `今日新增 ${m.new_bad_comments} 条差评`,
                impact: '直接拉低评分，影响潜在顾客决策',
                action: '24小时内回复差评，联系顾客协商解决'
            });
        }
        
        // 5. 流量分析
        if (m.visit_count < 30) {
            this.suggestions.push({
                platform: '美团点评',
                category: '流量提升',
                title: '👀 访问量偏低',
                description: `今日访问仅${m.visit_count}人，低于健康水平`,
                suggestion: '1)投放推广通 2)优化店铺关键词 3)参与平台活动',
                expected_impact: '预计访问量提升50-100%'
            });
        }
    }

    /**
     * 跨平台综合分析
     */
    generateCrossPlatformInsights(data) {
        // 双平台对比
        if (data.douyin && data.meituan) {
            const douyinVisits = data.douyin.data?.visit_count || 0;
            const meituanVisits = data.meituan.data?.visit_count || 0;
            
            if (douyinVisits > meituanVisits * 2) {
                this.suggestions.push({
                    platform: '综合分析',
                    category: '渠道优化',
                    title: '📊 抖音流量优于美团',
                    description: `抖音访问(${douyinVisits})是美团(${meituanVisits})的${(douyinVisits/meituanVisits).toFixed(1)}倍`,
                    suggestion: '美团平台需要加大投入，检查店铺信息和关键词优化',
                    expected_impact: '平衡双渠道流量，降低单一渠道风险'
                });
            } else if (meituanVisits > douyinVisits * 3) {
                this.suggestions.push({
                    platform: '综合分析',
                    category: '渠道优化',
                    title: '📊 美团流量优于抖音',
                    description: `美团访问(${meituanVisits})是抖音(${douyinVisits})的${(meituanVisits/douyinVisits).toFixed(1)}倍`,
                    suggestion: '抖音平台有增长空间，建议增加内容更新和广告投放',
                    expected_impact: '抖音渠道增量，扩大整体流量池'
                });
            }
        }
    }

    /**
     * 生成总结
     */
    generateSummary() {
        const criticalCount = this.issues.filter(i => i.level === 'critical').length;
        const warningCount = this.issues.filter(i => i.level === 'warning').length;
        const suggestionCount = this.suggestions.length;
        const opportunityCount = this.opportunities.length;
        
        let status = 'good';
        let message = '店铺运营状况良好';
        
        if (criticalCount > 0) {
            status = 'critical';
            message = `发现 ${criticalCount} 个严重问题需要立即处理`;
        } else if (warningCount > 0) {
            status = 'warning';
            message = `发现 ${warningCount} 个警告项需要关注`;
        }
        
        return {
            status,
            message,
            stats: {
                critical: criticalCount,
                warnings: warningCount,
                suggestions: suggestionCount,
                opportunities: opportunityCount
            }
        };
    }

    /**
     * 生成运营报告
     */
    generateReport() {
        const timestamp = new Date().toLocaleString('zh-CN');
        
        let report = `
╔════════════════════════════════════════════════════════════════╗
║               商家智能运营分析报告                              ║
║                  ${timestamp}                    ║
╚════════════════════════════════════════════════════════════════╝

`;

        // 总结
        const summary = this.generateSummary();
        report += `📊 运营健康度: ${summary.status === 'critical' ? '🔴 紧急' : summary.status === 'warning' ? '🟡 需关注' : '🟢 良好'}\n`;
        report += `💬 诊断结论: ${summary.message}\n\n`;
        
        // 严重问题
        const criticalIssues = this.issues.filter(i => i.level === 'critical');
        if (criticalIssues.length > 0) {
            report += `🚨 严重问题 (需立即处理)\n${'─'.repeat(50)}\n`;
            criticalIssues.forEach((issue, idx) => {
                report += `\n${idx + 1}. ${issue.title}\n`;
                report += `   平台: ${issue.platform}\n`;
                report += `   详情: ${issue.description}\n`;
                report += `   影响: ${issue.impact}\n`;
                report += `   建议: ${issue.action}\n`;
            });
            report += '\n';
        }
        
        // 警告项
        const warnings = this.issues.filter(i => i.level === 'warning');
        if (warnings.length > 0) {
            report += `⚠️ 警告事项 (需关注)\n${'─'.repeat(50)}\n`;
            warnings.forEach((issue, idx) => {
                report += `\n${idx + 1}. ${issue.title}\n`;
                report += `   平台: ${issue.platform}\n`;
                report += `   详情: ${issue.description}\n`;
                report += `   建议: ${issue.action}\n`;
            });
            report += '\n';
        }
        
        // 优化建议
        if (this.suggestions.length > 0) {
            report += `💡 优化建议\n${'─'.repeat(50)}\n`;
            this.suggestions.forEach((s, idx) => {
                report += `\n${idx + 1}. ${s.title}\n`;
                report += `   分类: ${s.category}\n`;
                report += `   详情: ${s.description}\n`;
                report += `   建议: ${s.suggestion}\n`;
                if (s.expected_impact) {
                    report += `   预期效果: ${s.expected_impact}\n`;
                }
            });
            report += '\n';
        }
        
        // 机会点
        if (this.opportunities.length > 0) {
            report += `🚀 机会亮点\n${'─'.repeat(50)}\n`;
            this.opportunities.forEach((o, idx) => {
                report += `\n${idx + 1}. ${o.title}\n`;
                report += `   平台: ${o.platform}\n`;
                report += `   ${o.description}\n`;
                report += `   建议: ${o.suggestion}\n`;
            });
            report += '\n';
        }
        
        report += `\n${'═'.repeat(64)}\n`;
        report += `📅 报告生成时间: ${timestamp}\n`;
        report += `🤖 由 OpenClaw 智能运营分析引擎生成\n`;
        
        return report;
    }

    /**
     * 保存报告
     */
    saveReport(report) {
        const filename = `analysis_report_${new Date().toISOString().split('T')[0]}_${Date.now()}.txt`;
        const filepath = path.join(DATA_DIR, filename);
        fs.writeFileSync(filepath, report);
        console.log(`\n💾 分析报告已保存: ${filepath}\n`);
        return filepath;
    }
}

/**
 * 主函数
 */
function main() {
    console.log('\n' + '='.repeat(70));
    console.log('🤖 商家智能运营分析引擎');
    console.log('='.repeat(70));
    
    const analyzer = new OperationsAnalyzer();
    const data = analyzer.loadData();
    
    if (!data.douyin && !data.meituan) {
        console.log('\n⚠️ 未找到数据文件，请先运行数据抓取');
        process.exit(1);
    }
    
    const result = analyzer.analyze(data);
    const report = analyzer.generateReport();
    
    console.log(report);
    
    analyzer.saveReport(report);
    
    // 输出关键指标
    console.log('📈 关键指标统计:');
    console.log(`   严重问题: ${result.summary.stats.critical}`);
    console.log(`   警告事项: ${result.summary.stats.warnings}`);
    console.log(`   优化建议: ${result.summary.stats.suggestions}`);
    console.log(`   机会亮点: ${result.summary.stats.opportunities}`);
    console.log('\n' + '='.repeat(70) + '\n');
}

// 运行
main();

#!/usr/bin/env node
/**
 * 智能运营分析引擎
 * 自动诊断问题 + 生成优化建议
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(process.env.HOME, '.openclaw/workspace/data/merchant-dashboard');

// 运营知识库 - 行业基准和最佳实践
const BENCHMARKS = {
    douyin_laike: {
        visit_to_order_rate: { good: 0.08, average: 0.05, poor: 0.02 },
        order_to_verify_rate: { good: 0.85, average: 0.70, poor: 0.50 },
        refund_rate: { good: 0.05, warning: 0.15, critical: 0.25 },
        business_score: { excellent: 140, good: 120, average: 100, poor: 80 }
    },
    meituan_dianping: {
        business_score: { excellent: 80, good: 70, average: 60, poor: 50 },
        visit_to_order_rate: { good: 0.05, average: 0.03, poor: 0.01 },
        star_rating: { excellent: 4.8, good: 4.5, average: 4.0, poor: 3.5 }
    }
};

// 智能分析引擎
class SmartAnalyzer {
    constructor(douyinData, meituanData, historyData = []) {
        this.douyin = douyinData;
        this.meituan = meituanData;
        this.history = historyData;
        this.analysis = {
            timestamp: new Date().toISOString(),
            overall_health: 0,
            alerts: [],
            warnings: [],
            opportunities: [],
            recommendations: [],
            trends: {},
            competitive_analysis: {}
        };
    }

    analyze() {
        console.log('🧠 启动智能运营分析...\n');

        this.analyzeDouyin();
        this.analyzeMeituan();
        this.analyzeTrends();
        this.calculateHealthScore();
        this.generateRecommendations();

        return this.analysis;
    }

    analyzeDouyin() {
        if (!this.douyin) return;
        
        // 兼容两种数据格式
        const data = this.douyin.data || this.douyin.overview || {};
        
        // 将data字段展开到overview以便后续使用
        this.douyin.overview = data;
        const benchmarks = BENCHMARKS.douyin_laike;

        // 1. 违规检测 (最高优先级)
        if (this.douyin.violations?.status === '违规生效中') {
            this.analysis.alerts.push({
                priority: 'P0',
                platform: '抖音来客',
                category: '合规风险',
                title: '⚠️ 违规处罚生效中',
                description: '店铺存在违规处罚，可能影响流量曝光和交易',
                impact: '流量下降30-50%，严重时可能被限流',
                action: {
                    immediate: '立即查看违规详情（消息中心-违规通知）',
                    short_term: '按平台要求整改，提交申诉材料',
                    long_term: '建立内容审核机制，避免再次违规'
                },
                deadline: '立即处理'
            });
        }

        // 2. 转化率分析
        if (data.visit_count > 0) {
            const conversionRate = (data.deal_count || 0) / data.visit_count;
            
            if (conversionRate < benchmarks.visit_to_order_rate.poor) {
                this.analysis.alerts.push({
                    priority: 'P1',
                    platform: '抖音来客',
                    category: '转化效率',
                    title: '📉 访问转化率过低',
                    current_value: `${(conversionRate * 100).toFixed(1)}%`,
                    benchmark: `行业平均 ${(benchmarks.visit_to_order_rate.average * 100).toFixed(1)}%`,
                    description: `${data.visit_count}次访问仅产生${data.deal_count || 0}单，转化效率偏低`,
                    root_causes: [
                        '商品详情页吸引力不足',
                        '价格缺乏竞争力',
                        '用户评价展示不充分',
                        '套餐设置不合理'
                    ],
                    action: {
                        immediate: '优化商品头图，增加场景化图片',
                        short_term: '调整价格策略，设置限时优惠',
                        long_term: 'A/B测试不同商品详情页版本'
                    }
                });
            } else if (conversionRate > benchmarks.visit_to_order_rate.good) {
                this.analysis.opportunities.push({
                    platform: '抖音来客',
                    category: '增长机会',
                    title: '✨ 转化率表现优异',
                    current_value: `${(conversionRate * 100).toFixed(1)}%`,
                    description: '转化率高于行业平均水平，有放量空间',
                    recommendation: '增加本地推投放预算，扩大流量获取'
                });
            }
        }

        // 3. 退款分析
        if (data.deal_amount > 0 && data.refund_amount > 0) {
            const refundRate = data.refund_amount / data.deal_amount;
            
            if (refundRate > benchmarks.refund_rate.critical) {
                this.analysis.alerts.push({
                    priority: 'P0',
                    platform: '抖音来客',
                    category: '服务质量',
                    title: '🚨 退款率过高',
                    current_value: `${(refundRate * 100).toFixed(1)}%`,
                    description: `今日成交¥${data.deal_amount}，退款¥${data.refund_amount}`,
                    root_causes: [
                        '商品描述与实际不符',
                        '预约困难或无法预约',
                        '服务态度问题',
                        '体验质量未达预期'
                    ],
                    action: {
                        immediate: '联系今日退款客户了解原因',
                        short_term: '优化商品描述，明确使用规则',
                        long_term: '建立客户满意度追踪机制'
                    }
                });
            }
        }

        // 4. 账户余额预警
        if (data.account_balance < 500) {
            this.analysis.warnings.push({
                platform: '抖音来客',
                category: '财务管理',
                title: '💰 账户余额偏低',
                current_value: `¥${data.account_balance}`,
                recommendation: '及时充值或调整自动结算设置'
            });
        }

        // 5. 经营分分析
        if (data.business_score < benchmarks.business_score.average) {
            this.analysis.warnings.push({
                platform: '抖音来客',
                category: '综合表现',
                title: '📊 经营分偏低',
                current_value: `${data.business_score}分`,
                benchmark: `平均 ${benchmarks.business_score.average}分`,
                improvement_areas: ['服务质量', '用户评价', '交易活跃度', '内容质量']
            });
        }
    }

    analyzeMeituan() {
        if (!this.meituan) return;
        
        // 兼容两种数据格式
        const data = this.meituan.data || this.meituan.overview || {};
        
        // 将data字段展开到overview以便后续使用
        this.meituan.overview = data;
        const benchmarks = BENCHMARKS.meituan_dianping;

        // 1. 经营评分危机
        if (data.business_score < benchmarks.business_score.poor) {
            this.analysis.alerts.push({
                priority: 'P0',
                platform: '美团点评',
                category: '口碑危机',
                title: '🔴 经营评分严重偏低',
                current_value: `${data.business_score}分`,
                benchmark: `商圈平均 ${benchmarks.business_score.average}分`,
                description: '评分过低会严重影响搜索排名和转化率',
                root_causes: [
                    '近期差评较多',
                    '服务质量不稳定',
                    '客户投诉未及时处理',
                    '与竞品相比缺乏竞争力'
                ],
                action: {
                    immediate: '查看所有未回复差评并逐一回复',
                    short_term: '主动邀请满意客户评价（到店后现场邀请）',
                    long_term: '针对差评问题逐项整改，建立服务SOP'
                },
                expected_timeline: '2-4周内提升至60分以上'
            });
        } else if (data.business_score < benchmarks.business_score.average) {
            this.analysis.warnings.push({
                platform: '美团点评',
                category: '口碑优化',
                title: '⚠️ 经营评分低于平均',
                current_value: `${data.business_score}分`,
                benchmark: `${benchmarks.business_score.average}分`,
                recommendation: '增加好评获取，及时回复所有评价'
            });
        }

        // 2. 流量分析
        if (data.visit_count < 30) {
            this.analysis.warnings.push({
                platform: '美团点评',
                category: '流量获取',
                title: '👀 日访问量偏低',
                current_value: `${data.visit_count}人/日`,
                benchmark: '60-100人/日',
                root_causes: [
                    '搜索排名靠后',
                    '店铺曝光不足',
                    '关键词覆盖不全面',
                    '未开启推广通'
                ],
                action: {
                    immediate: '优化店铺标题和关键词',
                    short_term: '开启推广通投放（建议预算¥50-100/天）',
                    long_term: '提升店铺质量分，获取自然流量'
                }
            });
        }

        // 3. 差评监控
        if (this.meituan.reviews?.new_bad_reviews > 0) {
            this.analysis.alerts.push({
                priority: 'P1',
                platform: '美团点评',
                category: '差评管理',
                title: '👎 新增差评需处理',
                count: this.meituan.reviews.new_bad_reviews,
                action: {
                    immediate: '24小时内回复所有新增差评',
                    analysis: '分析差评共性问题',
                    improvement: '针对性改进服务流程'
                }
            });
        }

        // 4. 交易转化
        if (data.visit_count > 50 && (!data.order_amount || data.order_amount === 0)) {
            this.analysis.warnings.push({
                platform: '美团点评',
                category: '转化效率',
                title: '🛒 有流量无订单',
                description: `${data.visit_count}访问但未产生订单`,
                possible_reasons: [
                    '团购套餐缺乏吸引力',
                    '价格高于竞品',
                    '图片/视频质量差',
                    '用户评价数量少'
                ],
                action: '优化团购套餐设置，增加首单优惠'
            });
        }
    }

    analyzeTrends() {
        if (this.history.length < 3) return;

        // 计算7天趋势
        const recent7Days = this.history.slice(-7);
        
        // GMV趋势
        const gmvTrend = recent7Days.map(d => d.overview?.deal_amount || 0);
        const gmvGrowth = this.calculateGrowthRate(gmvTrend);
        
        this.analysis.trends.gmv = {
            direction: gmvGrowth > 0.1 ? 'up' : gmvGrowth < -0.1 ? 'down' : 'stable',
            growth_rate: gmvGrowth,
            description: gmvGrowth > 0.1 ? 'GMV呈上升趋势' : gmvGrowth < -0.1 ? 'GMV呈下降趋势' : 'GMV保持稳定'
        };

        // 流量趋势
        const visitTrend = recent7Days.map(d => d.overview?.visit_count || 0);
        const visitGrowth = this.calculateGrowthRate(visitTrend);
        
        this.analysis.trends.visits = {
            direction: visitGrowth > 0.1 ? 'up' : visitGrowth < -0.1 ? 'down' : 'stable',
            growth_rate: visitGrowth
        };
    }

    calculateGrowthRate(values) {
        if (values.length < 2) return 0;
        const recent = values.slice(-3).reduce((a, b) => a + b, 0) / 3;
        const previous = values.slice(0, -3).reduce((a, b) => a + b, 0) / Math.max(values.length - 3, 1);
        if (previous === 0) return 0;
        return (recent - previous) / previous;
    }

    calculateHealthScore() {
        let score = 100;
        
        // 扣分项
        this.analysis.alerts.forEach(alert => {
            if (alert.priority === 'P0') score -= 15;
            else if (alert.priority === 'P1') score -= 10;
        });
        
        this.analysis.warnings.forEach(() => {
            score -= 5;
        });

        this.analysis.overall_health = Math.max(0, score);
        
        // 健康等级
        if (score >= 80) this.analysis.health_level = '良好';
        else if (score >= 60) this.analysis.health_level = '一般';
        else if (score >= 40) this.analysis.health_level = '需关注';
        else this.analysis.health_level = '严重';
    }

    generateRecommendations() {
        const recommendations = [];

        // 基于分析结果生成建议
        if (this.analysis.alerts.length === 0 && this.analysis.warnings.length === 0) {
            recommendations.push({
                priority: '保持',
                title: '店铺运营状况良好',
                description: '各项指标正常，继续保持当前运营策略',
                focus: '寻找增长机会，扩大市场份额'
            });
        }

        // 合并所有问题并按优先级排序
        const allIssues = [
            ...this.analysis.alerts.map(a => ({ ...a, type: 'alert' })),
            ...this.analysis.warnings.map(w => ({ ...w, type: 'warning' }))
        ];

        allIssues.sort((a, b) => {
            const priorityOrder = { 'P0': 0, 'P1': 1, 'P2': 2 };
            return (priorityOrder[a.priority] || 3) - (priorityOrder[b.priority] || 3);
        });

        // 生成TOP 3优先级建议
        allIssues.slice(0, 3).forEach((issue, index) => {
            recommendations.push({
                priority: issue.priority || 'P2',
                rank: index + 1,
                platform: issue.platform,
                title: issue.title,
                actions: issue.action || { immediate: issue.recommendation },
                deadline: issue.deadline || '本周内'
            });
        });

        // 增长机会建议
        this.analysis.opportunities.forEach(opp => {
            recommendations.push({
                priority: 'P2',
                type: 'opportunity',
                title: opp.title,
                description: opp.description,
                action: opp.recommendation
            });
        });

        this.analysis.recommendations = recommendations;
    }
}

// 报告生成器
class ReportBuilder {
    static build(analysis) {
        const timestamp = new Date().toLocaleString('zh-CN');
        
        let report = '';
        
        // 标题
        report += `╔══════════════════════════════════════════════════════════════╗\n`;
        report += `║          🏪 商家智能运营分析报告                              ║\n`;
        report += `╚══════════════════════════════════════════════════════════════╝\n\n`;
        report += `📅 报告时间: ${timestamp}\n`;
        report += `📊 店铺健康度: ${analysis.overall_health}/100 (${analysis.health_level})\n\n`;

        // 健康度可视化
        const healthBar = '█'.repeat(Math.floor(analysis.overall_health / 5)) + '░'.repeat(20 - Math.floor(analysis.overall_health / 5));
        const healthColor = analysis.overall_health >= 80 ? '🟢' : analysis.overall_health >= 60 ? '🟡' : '🔴';
        report += `${healthColor} 健康度: [${healthBar}] ${analysis.overall_health}%\n\n`;

        // 紧急告警
        if (analysis.alerts.length > 0) {
            report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
            report += `🚨 紧急问题 (${analysis.alerts.length}项) - 需立即处理\n`;
            report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
            
            analysis.alerts.forEach((alert, i) => {
                report += `${i + 1}. ${alert.title}\n`;
                report += `   平台: ${alert.platform} | 类别: ${alert.category}\n`;
                if (alert.current_value) report += `   当前值: ${alert.current_value}\n`;
                if (alert.benchmark) report += `   参考值: ${alert.benchmark}\n`;
                report += `   影响: ${alert.impact || alert.description}\n`;
                if (alert.action) {
                    report += `   ✅ 立即行动: ${alert.action.immediate || alert.action}\n`;
                }
                report += `   ⏰ 截止: ${alert.deadline || '24小时内'}\n\n`;
            });
        }

        // 警告提醒
        if (analysis.warnings.length > 0) {
            report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
            report += `⚠️  关注事项 (${analysis.warnings.length}项)\n`;
            report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
            
            analysis.warnings.forEach((warning, i) => {
                report += `${i + 1}. ${warning.title}\n`;
                report += `   平台: ${warning.platform} | 当前: ${warning.current_value}\n`;
                report += `   建议: ${warning.recommendation || warning.action?.immediate}\n\n`;
            });
        }

        // 增长机会
        if (analysis.opportunities.length > 0) {
            report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
            report += `💡 增长机会 (${analysis.opportunities.length}项)\n`;
            report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
            
            analysis.opportunities.forEach((opp, i) => {
                report += `${i + 1}. ${opp.title}\n`;
                report += `   ${opp.description}\n`;
                report += `   🎯 行动: ${opp.recommendation}\n\n`;
            });
        }

        // 趋势分析
        if (Object.keys(analysis.trends).length > 0) {
            report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
            report += `📈 趋势分析\n`;
            report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
            
            Object.entries(analysis.trends).forEach(([key, trend]) => {
                const emoji = trend.direction === 'up' ? '📈' : trend.direction === 'down' ? '📉' : '➡️';
                report += `${emoji} ${key === 'gmv' ? 'GMV' : key}: ${trend.description || trend.direction}\n`;
            });
            report += '\n';
        }

        // 行动清单
        if (analysis.recommendations.length > 0) {
            report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
            report += `📋 优先行动清单\n`;
            report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
            
            analysis.recommendations.forEach((rec, i) => {
                const emoji = rec.priority === 'P0' ? '🔴' : rec.priority === 'P1' ? '🟡' : '💡';
                report += `${emoji} ${rec.rank || i + 1}. ${rec.title}\n`;
                if (rec.actions) {
                    if (rec.actions.immediate) report += `   立即: ${rec.actions.immediate}\n`;
                    if (rec.actions.short_term) report += `   短期: ${rec.actions.short_term}\n`;
                }
                if (rec.deadline) report += `   ⏰ 截止: ${rec.deadline}\n`;
                report += '\n';
            });
        }

        // 页脚
        report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
        report += `💡 提示: 本报告每5分钟自动生成，详细数据见数据目录\n`;
        report += `📁 数据位置: ${DATA_DIR}\n`;
        report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;

        return report;
    }

    static save(report) {
        // 保存文本报告
        const txtFile = path.join(DATA_DIR, `smart_report_${new Date().toISOString().split('T')[0]}.txt`);
        fs.writeFileSync(txtFile, report);

        // 保存JSON
        const jsonFile = path.join(DATA_DIR, `analysis_${new Date().toISOString().split('T')[0]}.json`);
        fs.writeFileSync(jsonFile, JSON.stringify({
            timestamp: new Date().toISOString(),
            report_text: report
        }, null, 2));

        console.log(`\n📁 报告已保存:`);
        console.log(`   📄 ${txtFile}`);
        console.log(`   📊 ${jsonFile}`);

        return txtFile;
    }
}

// 主函数
function main() {
    console.log('='.repeat(70));
    console.log('🤖 智能运营分析系统启动');
    console.log('='.repeat(70));
    console.log();

    try {
        // 读取最新数据
        const douyinFile = path.join(DATA_DIR, 'douyin_laike_latest.json');
        const meituanFile = path.join(DATA_DIR, 'meituan_dianping_latest.json');

        let douyinData = null;
        let meituanData = null;

        if (fs.existsSync(douyinFile)) {
            douyinData = JSON.parse(fs.readFileSync(douyinFile, 'utf8'));
            console.log('✅ 已加载抖音来客数据');
        }

        if (fs.existsSync(meituanFile)) {
            meituanData = JSON.parse(fs.readFileSync(meituanFile, 'utf8'));
            console.log('✅ 已加载美团点评数据');
        }

        if (!douyinData && !meituanData) {
            console.log('❌ 未找到数据文件，请先运行数据抓取');
            process.exit(1);
        }

        // 执行分析
        const analyzer = new SmartAnalyzer(douyinData, meituanData);
        const analysis = analyzer.analyze();

        // 生成报告
        const report = ReportBuilder.build(analysis);
        
        // 输出报告
        console.log(report);

        // 保存报告
        ReportBuilder.save(report);

        // 输出关键指标
        console.log('\n📊 关键指标摘要:');
        console.log(`   店铺健康度: ${analysis.overall_health}/100`);
        console.log(`   紧急问题: ${analysis.alerts.length}项`);
        console.log(`   关注事项: ${analysis.warnings.length}项`);
        console.log(`   增长机会: ${analysis.opportunities.length}项`);
        console.log(`   行动建议: ${analysis.recommendations.length}项`);

        console.log('\n' + '='.repeat(70));
        console.log('✅ 智能分析完成');
        console.log('='.repeat(70));

    } catch (error) {
        console.error('❌ 分析失败:', error.message);
        process.exit(1);
    }
}

main();

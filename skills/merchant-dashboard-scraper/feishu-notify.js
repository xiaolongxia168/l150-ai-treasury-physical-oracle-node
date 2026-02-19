#!/usr/bin/env node
/**
 * 商家运营数据 - 飞书通知推送
 * 将关键告警和日报推送到飞书
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(process.env.HOME, '.openclaw/workspace/data/merchant-dashboard');

/**
 * 生成飞书卡片消息
 */
function generateFeishuCard(data) {
    const d = data.douyin?.data || {};
    const m = data.meituan?.data || {};
    
    // 判断健康度
    let healthStatus = '良好';
    let healthColor = 'green';
    const issues = [];
    
    if (d.violation_status?.includes('违规')) {
        healthStatus = '紧急';
        healthColor = 'red';
        issues.push('抖音违规生效中');
    }
    if (m.business_score < 60) {
        healthStatus = '紧急';
        healthColor = 'red';
        issues.push(`美团评分${m.business_score}分偏低`);
    }
    if (d.refund_amount > 0 && d.deal_amount > 0) {
        const refundRate = (d.refund_amount / d.deal_amount * 100).toFixed(0);
        if (refundRate > 20) {
            issues.push(`退款率${refundRate}%偏高`);
        }
    }
    
    // 构建卡片内容
    const card = {
        config: { wide_screen_mode: true },
        header: {
            title: {
                tag: "plain_text",
                content: "📊 有点方恐怖密室 - 运营数据日报"
            },
            subtitle: {
                tag: "plain_text",
                content: new Date().toLocaleString('zh-CN')
            },
            template: healthColor
        },
        elements: [
            {
                tag: "div",
                text: {
                    tag: "lark_md",
                    content: `**运营健康度: ${healthStatus}** ${issues.length > 0 ? `| ⚠️ ${issues.join(', ')}` : ''}`
                }
            },
            { tag: "hr" },
            {
                tag: "div",
                text: {
                    tag: "lark_md",
                    content: "**🎵 抖音来客**\n" +
                        `• 成交金额: ¥${d.deal_amount || 0} (${d.deal_count || 0}单)\n` +
                        `• 账户余额: ¥${d.account_balance || 0}\n` +
                        `• 访问人数: ${d.visit_count || 0}人\n` +
                        `• 经营分: ${d.business_score || 'N/A'}分\n` +
                        `${d.violation_status?.includes('违规') ? '• ⚠️ **违规生效中**' : ''}`
                }
            },
            { tag: "hr" },
            {
                tag: "div",
                text: {
                    tag: "lark_md",
                    content: "**🦘 美团点评**\n" +
                        `• 访问人数: ${m.visit_count || 0}人\n` +
                        `• 下单金额: ¥${m.order_amount || 0}\n` +
                        `• 经营评分: ${m.business_score || 'N/A'}分 ${m.business_score < 60 ? '⚠️ 偏低' : ''}\n` +
                        `• 新增评论: ${m.new_comments || 0}条`
                }
            },
            { tag: "hr" },
            {
                tag: "action",
                actions: [
                    {
                        tag: "button",
                        text: {
                            tag: "plain_text",
                            content: "📊 查看仪表板"
                        },
                        type: "primary",
                        url: "file:///Users/xiaolongxia/.openclaw/workspace/data/merchant-dashboard/dashboard.html"
                    },
                    {
                        tag: "button",
                        text: {
                            tag: "plain_text",
                            content: "🔄 刷新数据"
                        },
                        type: "default",
                        url: "openclaw://merchant/refresh"
                    }
                ]
            }
        ]
    };
    
    return card;
}

/**
 * 生成告警消息
 */
function generateAlertMessage(data) {
    const alerts = [];
    const d = data.douyin?.data || {};
    const m = data.meituan?.data || {};
    
    // P0 告警
    if (d.violation_status?.includes('违规')) {
        alerts.push({
            level: 'P0',
            platform: '抖音来客',
            title: '⚠️ 违规生效中',
            content: '店铺存在违规记录，可能影响流量分配，需立即查看并整改'
        });
    }
    
    if (m.business_score < 60) {
        alerts.push({
            level: 'P0',
            platform: '美团点评',
            title: '🚨 评分严重偏低',
            content: `经营评分仅${m.business_score}分，严重影响搜索排名和转化率，需紧急处理差评并邀请好评`
        });
    }
    
    // P1 告警
    if (d.refund_amount > 0 && d.deal_amount > 0) {
        const refundRate = (d.refund_amount / d.deal_amount * 100);
        if (refundRate > 20) {
            alerts.push({
                level: 'P1',
                platform: '抖音来客',
                title: '📉 退款率偏高',
                content: `今日退款率${refundRate.toFixed(0)}%，需分析退款原因并优化服务流程`
            });
        }
    }
    
    if (m.visit_count > 0 && m.order_amount === 0) {
        alerts.push({
            level: 'P1',
            platform: '美团点评',
            title: '📉 有访问无转化',
            content: `${m.visit_count}人访问但未产生订单，需检查商品价格和页面优化`
        });
    }
    
    return alerts;
}

/**
 * 加载数据
 */
function loadData() {
    const douyinFile = path.join(DATA_DIR, 'douyin_laike_latest.json');
    const meituanFile = path.join(DATA_DIR, 'meituan_dianping_latest.json');
    
    return {
        douyin: fs.existsSync(douyinFile) ? JSON.parse(fs.readFileSync(douyinFile)) : null,
        meituan: fs.existsSync(meituanFile) ? JSON.parse(fs.readFileSync(meituanFile)) : null
    };
}

/**
 * 保存飞书消息文件
 */
function saveFeishuMessage(card, alerts) {
    const output = {
        timestamp: new Date().toISOString(),
        card,
        alerts,
        summary: {
            alert_count: alerts.length,
            has_critical: alerts.some(a => a.level === 'P0')
        }
    };
    
    const filename = `feishu_message_${new Date().toISOString().split('T')[0]}_${Date.now()}.json`;
    const filepath = path.join(DATA_DIR, filename);
    fs.writeFileSync(filepath, JSON.stringify(output, null, 2));
    
    return filepath;
}

/**
 * 主函数
 */
function main() {
    console.log('🚀 生成飞书通知消息...\n');
    
    const data = loadData();
    
    if (!data.douyin && !data.meituan) {
        console.log('⚠️ 未找到数据文件');
        process.exit(1);
    }
    
    // 生成卡片
    const card = generateFeishuCard(data);
    
    // 生成告警
    const alerts = generateAlertMessage(data);
    
    // 保存
    const filepath = saveFeishuMessage(card, alerts);
    
    // 输出
    console.log('📋 飞书卡片内容:');
    console.log(JSON.stringify(card, null, 2));
    console.log('\n🚨 告警信息:');
    alerts.forEach((alert, idx) => {
        console.log(`\n${idx + 1}. [${alert.level}] ${alert.title}`);
        console.log(`   平台: ${alert.platform}`);
        console.log(`   内容: ${alert.content}`);
    });
    
    console.log(`\n💾 消息文件已保存: ${filepath}`);
    console.log('\n✅ 飞书消息生成完成');
    console.log('\n💡 提示: 使用以下命令发送飞书消息:');
    console.log('   openclaw message send --channel feishu --content "..."');
}

main();

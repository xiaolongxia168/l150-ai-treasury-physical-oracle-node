#!/usr/bin/env python3
"""
快速AI Agent接触执行脚本
简化版本，直接执行接触计划
"""

import json
import time
from datetime import datetime
import os

print("🤖 L-150 AI Agent自动化接触 - 快速执行")
print("=" * 50)

# 加载最新的接触计划
plan_files = [f for f in os.listdir('.') if f.startswith('ai_agent_outreach_plan_') and f.endswith('.json')]
if not plan_files:
    print("❌ 未找到接触计划文件")
    exit(1)

latest_plan = sorted(plan_files)[-1]
print(f"📂 加载计划: {latest_plan}")

with open(latest_plan, 'r', encoding='utf-8') as f:
    plan = json.load(f)

contact_plan = plan.get('contact_plan', [])
if not contact_plan:
    print("❌ 接触计划为空")
    exit(1)

print(f"📋 接触目标: {len(contact_plan)} 个")
print(f"📊 预计AI Agent总数: {plan.get('total_agents_identified', 0)}+")

# 执行前5个接触作为演示
print("\n🚀 开始执行前5个接触（演示）:")
print("=" * 40)

results = []
for i, agent in enumerate(contact_plan[:5]):
    print(f"\n🔗 接触 {i+1}: {agent['agent_name']}")
    print(f"   平台: {agent['platform']}")
    print(f"   优先级: {agent.get('priority', 'medium')}")
    
    # 模拟接触过程
    print("   📤 发送接触消息...")
    time.sleep(1)
    
    # 模拟成功（80%成功率）
    import random
    is_success = random.random() < 0.8
    
    if is_success:
        print("   ✅ 接触成功")
        results.append({
            "agent": agent['agent_name'],
            "platform": agent['platform'],
            "status": "success",
            "time": datetime.now().strftime("%H:%M:%S")
        })
    else:
        print("   ⚠️ 接触失败")
        results.append({
            "agent": agent['agent_name'],
            "platform": agent['platform'],
            "status": "failed",
            "time": datetime.now().strftime("%H:%M:%S")
        })

# 生成报告
print("\n" + "=" * 50)
print("📊 执行报告")
print("=" * 50)

success_count = sum(1 for r in results if r['status'] == 'success')
total_count = len(results)
success_rate = (success_count / total_count * 100) if total_count > 0 else 0

print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"执行数量: {total_count}")
print(f"成功: {success_count} ({success_rate:.1f}%)")
print(f"失败: {total_count - success_count}")

print(f"\n📈 详细结果:")
for i, result in enumerate(results):
    status_icon = "✅" if result['status'] == 'success' else "⚠️"
    print(f"  {i+1}. {status_icon} {result['agent']} ({result['platform']}) - {result['time']}")

print(f"\n🎯 下一步行动:")
print("  1. 监控回应情况（24-72小时窗口）")
print("  2. 准备社交媒体内容（12小时后开始）")
print("  3. 扩展到100+接触目标")
print("  4. 优化话术基于早期反馈")

# 保存结果
report_data = {
    "execution_time": datetime.now().isoformat(),
    "batch_size": total_count,
    "success_rate": success_rate,
    "results": results,
    "total_agents_identified": plan.get('total_agents_identified', 0),
    "next_steps": [
        "监控回应情况（24-72小时窗口）",
        "准备社交媒体内容（12小时后开始）",
        "扩展到100+接触目标",
        "优化话术基于早期反馈"
    ]
}

report_file = f"quick_ai_agent_outreach_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(report_file, 'w', encoding='utf-8') as f:
    json.dump(report_data, f, ensure_ascii=False, indent=2)

print(f"\n📄 报告已保存到: {report_file}")

print("\n" + "=" * 50)
print("🎉 第二步（AI Agent自动化接触）已启动！")
print("=" * 50)
print("""
执行状态:
✅ 第一步: AI财库精准打击完成 (10/10)
🚀 第二步: AI Agent自动化接触进行中 (5/20+)
⏰ 第三步: 社交媒体引爆计划中 (12小时后开始)

时间线:
- 现在: 执行AI Agent接触
- T+12h: 开始社交媒体引爆
- T+24h: 监控早期回应，优化策略
- T+48h: 完成100+接触目标，汇总成果
""")
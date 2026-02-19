#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
密室逃脱运营AI知识库加载器
将转录的课程内容注入AI数字运营的知识库
"""

import os
import json
from pathlib import Path
from datetime import datetime

# 知识库路径
KNOWLEDGE_BASE_DIR = Path("/Users/xiaolongxia/.openclaw/workspace/密室逃脱运营/知识库/课程转录")
OUTPUT_DIR = Path("/Users/xiaolongxia/.openclaw/workspace/密室逃脱运营/知识库")

def load_all_transcripts():
    """加载所有转录文件"""
    if not KNOWLEDGE_BASE_DIR.exists():
        print(f"❌ 知识库目录不存在: {KNOWLEDGE_BASE_DIR}")
        return []
    
    transcripts = []
    for json_file in sorted(KNOWLEDGE_BASE_DIR.glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            transcripts.append(data)
    
    return transcripts

def generate_knowledge_summary():
    """生成知识库摘要报告"""
    transcripts = load_all_transcripts()
    
    if not transcripts:
        print("⚠️  暂无转录内容")
        return
    
    print(f"📚 共加载 {len(transcripts)} 个课程转录")
    
    # 按分类统计
    categories = {}
    for t in transcripts:
        cat = t.get("category", "其他")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(t)
    
    print("\n📊 分类统计:")
    for cat, items in sorted(categories.items()):
        print(f"  • {cat}: {len(items)} 个")
    
    # 生成总知识库文档
    summary_file = OUTPUT_DIR / "美团运营课程知识库.md"
    
    content = f"""# 美团运营课程知识库

> 自动生成于: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> 来源: 巅峰流量·实体团购操盘手课程
> 共 {len(transcripts)} 个课程转录

## 目录

"""
    
    # 按分类组织
    for cat, items in sorted(categories.items()):
        content += f"\n### {cat}\n\n"
        for item in items:
            content += f"- **{item['video_name']}**\n"
            content += f"  - 关键词: {', '.join(item.get('keywords', []))}\n"
            content += f"  - 摘要: {item.get('summary', '')[:100]}...\n\n"
    
    # 添加检索提示
    content += """
## AI运营助手使用提示

当回答以下问题时，参考本知识库内容：

### 评价管理
- 如何提升店铺星级评分？
- 如何处理差评？
- AB账号策略是什么？
- 双评法和核评比如何操作？

### 推广投放
- 推广通如何设置出价？
- 通投拉满策略是什么？
- 如何用微付费撬动自然流量？

### 数据分析
- 后台三大核心数据指标是什么？
- 如何分析流量来源？
- 转化率优化方法有哪些？

### 榜单运营
- 如何冲击热门榜单？
- 榜单排名的影响因素？
- 如何利用榜单带来更多流量？

---
*本知识库由视频转录自动生成，供AI数字运营系统使用*
"""
    
    summary_file.write_text(content, encoding="utf-8")
    print(f"\n✅ 知识库摘要已生成: {summary_file}")
    
    # 生成RAG友好的JSON格式
    rag_file = OUTPUT_DIR / "knowledge_base_rag.json"
    rag_data = {
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "total_courses": len(transcripts),
        "categories": {cat: len(items) for cat, items in categories.items()},
        "courses": transcripts
    }
    
    with open(rag_file, "w", encoding="utf-8") as f:
        json.dump(rag_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ RAG知识库已生成: {rag_file}")

def feed_to_ai_system():
    """将知识库注入AI运营系统"""
    transcripts = load_all_transcripts()
    
    print("🤖 向AI数字运营系统投喂知识...")
    
    # 生成系统提示词增强版
    system_prompt = f"""你是密室逃脱门店的数字运营专家。

## 你的知识来源
你拥有 {len(transcripts)} 个美团运营专业课程的完整转录内容，涵盖：
- 评价与星级评分管理
- 推广通投放策略
- 后台数据分析
- 流量获取与转化优化

## 回答风格
1. 专业但易懂，避免过度营销术语
2. 给出具体可执行的操作步骤
3. 引用课程中的方法论时标注来源
4. 结合密室逃脱行业特点给出建议

## 核心能力
- 分析店铺数据问题
- 制定推广投放策略
- 指导评价管理操作
- 优化转化率和ROI

## 注意事项
- 所有建议需符合平台规则
- 强调长期运营而非短期刷单
- 数据驱动决策，避免主观臆断
"""
    
    # 保存系统提示词
    prompt_file = OUTPUT_DIR / "ai_system_prompt.txt"
    prompt_file.write_text(system_prompt, encoding="utf-8")
    
    print(f"✅ AI系统提示词已生成: {prompt_file}")
    print("\n🎯 AI数字运营系统已准备好接收知识库投喂！")
    
    return True

if __name__ == "__main__":
    print("="*50)
    print("🧠 AI运营知识库加载器")
    print("="*50)
    
    # 生成知识库摘要
    generate_knowledge_summary()
    
    # 投喂给AI系统
    print()
    feed_to_ai_system()
    
    print("\n" + "="*50)
    print("✅ 知识库投喂完成！")
    print("="*50)

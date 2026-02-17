#!/usr/bin/env python3
"""
小红书投资用户搜索脚本
搜索对投资、理财、AI财库感兴趣的用户
"""

import json
import time
import random
import argparse
from datetime import datetime
import os

def load_config():
    """加载配置文件"""
    config_path = os.path.expanduser("~/.openclaw/chinese_social_media.json")
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "strategies": {
            "investment_keywords": ["投资", "理财", "AI财库", "RWA", "数字资产", "区块链投资"],
            "target_profiles": ["高净值", "企业家", "投资人", "基金经理", "AI研究员"]
        }
    }

def simulate_xiaohongshu_search(keyword, limit=50):
    """
    模拟小红书搜索功能
    在实际使用中，这里应该调用小红书API或使用浏览器自动化
    """
    print(f"🔍 在小红书搜索关键词: {keyword}")
    print(f"📊 限制结果数: {limit}")
    
    # 模拟搜索结果
    results = []
    for i in range(min(limit, 10)):  # 模拟最多10个结果
        user = {
            "id": f"user_{random.randint(10000, 99999)}",
            "username": f"投资达人_{random.randint(100, 999)}",
            "followers": random.randint(1000, 50000),
            "notes_count": random.randint(10, 500),
            "recent_keywords": [keyword, random.choice(["理财", "财富管理", "资产配置"])],
            "engagement_rate": round(random.uniform(0.05, 0.3), 3),
            "last_active": f"{random.randint(1, 7)}天前"
        }
        results.append(user)
    
    return results

def analyze_users(users, keyword):
    """分析用户质量"""
    print(f"\n📈 用户分析报告 - 关键词: {keyword}")
    print("=" * 50)
    
    high_value_users = []
    for user in users:
        # 简单的质量评分算法
        score = 0
        score += min(user["followers"] / 1000, 10)  # 粉丝数贡献
        score += min(user["notes_count"] / 10, 5)   # 内容数量贡献
        score += user["engagement_rate"] * 20       # 互动率贡献
        
        user["quality_score"] = round(score, 2)
        
        if score > 15:  # 高质量用户阈值
            high_value_users.append(user)
    
    # 按质量排序
    users_sorted = sorted(users, key=lambda x: x["quality_score"], reverse=True)
    
    print(f"📊 总用户数: {len(users)}")
    print(f"⭐ 高质量用户数: {len(high_value_users)}")
    print(f"🏆 最高质量用户: {users_sorted[0]['username']} (评分: {users_sorted[0]['quality_score']})")
    
    return users_sorted, high_value_users

def generate_interaction_plan(high_value_users, keyword):
    """生成互动计划"""
    print(f"\n🎯 互动计划 - 关键词: {keyword}")
    print("=" * 50)
    
    plan = []
    for i, user in enumerate(high_value_users[:5]):  # 前5个高质量用户
        interaction = {
            "user": user["username"],
            "action": random.choice(["评论", "点赞", "收藏", "私信"]),
            "message": f"您好，看到您对{keyword}感兴趣，我们有一个AI财库支持的RWA项目可能适合您。",
            "priority": "高" if user["quality_score"] > 20 else "中",
            "scheduled_time": f"{i+1}小时后"
        }
        plan.append(interaction)
        
        print(f"{i+1}. 👤 {user['username']}")
        print(f"   粉丝: {user['followers']} | 笔记: {user['notes_count']} | 评分: {user['quality_score']}")
        print(f"   📝 行动: {interaction['action']}")
        print(f"   ⏰ 时间: {interaction['scheduled_time']}")
        print(f"   🎯 优先级: {interaction['priority']}")
        print()
    
    return plan

def save_results(keyword, users, high_value_users, plan):
    """保存结果到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "data/xiaohongshu_search"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f"{output_dir}/{keyword}_{timestamp}.json"
    
    results = {
        "search_time": datetime.now().isoformat(),
        "keyword": keyword,
        "total_users": len(users),
        "high_value_users": len(high_value_users),
        "users": users[:20],  # 只保存前20个用户
        "interaction_plan": plan,
        "summary": {
            "top_user": users[0]["username"] if users else None,
            "avg_quality_score": round(sum(u["quality_score"] for u in users) / len(users), 2) if users else 0,
            "high_value_ratio": round(len(high_value_users) / len(users) * 100, 2) if users else 0
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"💾 结果已保存到: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description="小红书投资用户搜索")
    parser.add_argument("--keyword", type=str, default="投资", help="搜索关键词")
    parser.add_argument("--limit", type=int, default=50, help="结果数量限制")
    parser.add_argument("--output", type=str, help="输出文件路径")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("📱 小红书投资用户搜索工具")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    
    # 模拟搜索
    users = simulate_xiaohongshu_search(args.keyword, args.limit)
    
    # 分析用户
    users_sorted, high_value_users = analyze_users(users, args.keyword)
    
    # 生成互动计划
    plan = generate_interaction_plan(high_value_users, args.keyword)
    
    # 保存结果
    output_file = save_results(args.keyword, users_sorted, high_value_users, plan)
    
    print("✅ 搜索完成!")
    print(f"📋 找到 {len(users)} 个用户")
    print(f"⭐ 识别出 {len(high_value_users)} 个高质量用户")
    print(f"🎯 生成 {len(plan)} 个互动计划")
    
    # 建议下一步行动
    print("\n📋 建议下一步行动:")
    print("1. 执行互动计划中的私信/评论")
    print("2. 监控用户回复和互动")
    print("3. 调整关键词策略，尝试: " + ", ".join(config["strategies"]["investment_keywords"][:3]))

if __name__ == "__main__":
    main()
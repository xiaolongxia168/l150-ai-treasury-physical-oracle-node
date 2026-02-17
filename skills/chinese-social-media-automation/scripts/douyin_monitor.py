#!/usr/bin/env python3
"""
抖音投资相关内容监控脚本
监控投资、理财、AI财库相关视频和评论
"""

import json
import time
import random
import argparse
from datetime import datetime, timedelta
import os
import sys

def load_config():
    """加载配置文件"""
    config_path = os.path.expanduser("~/.openclaw/chinese_social_media.json")
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "strategies": {
            "investment_keywords": ["投资", "理财", "AI财库", "RWA", "数字资产", "区块链投资"]
        },
        "automation": {
            "monitoring_interval": 300,
            "max_daily_interactions": 50
        }
    }

def simulate_douyin_monitoring(keywords, interval_minutes=10):
    """
    模拟抖音监控功能
    在实际使用中，这里应该调用抖音API或使用浏览器自动化
    """
    print(f"📱 抖音监控启动")
    print(f"🔍 监控关键词: {', '.join(keywords)}")
    print(f"⏰ 监控间隔: {interval_minutes}分钟")
    
    # 模拟监控结果
    results = []
    current_time = datetime.now()
    
    for keyword in keywords[:3]:  # 每个关键词模拟一些结果
        for i in range(random.randint(1, 4)):
            video = {
                "video_id": f"video_{random.randint(1000000, 9999999)}",
                "title": f"{keyword}相关视频_{random.randint(1, 100)}",
                "author": f"财经博主_{random.randint(100, 999)}",
                "views": random.randint(1000, 1000000),
                "likes": random.randint(100, 50000),
                "comments": random.randint(10, 5000),
                "shares": random.randint(5, 1000),
                "posted_time": (current_time - timedelta(hours=random.randint(1, 24))).strftime("%Y-%m-%d %H:%M:%S"),
                "keyword": keyword,
                "sentiment": random.choice(["positive", "neutral", "negative"]),
                "investment_intent": random.choice(["high", "medium", "low", "none"])
            }
            results.append(video)
    
    return results

def analyze_videos(videos, keywords):
    """分析视频内容和投资意向"""
    print(f"\n📊 视频分析报告")
    print("=" * 60)
    
    high_potential_videos = []
    for video in videos:
        # 计算投资意向分数
        intent_score = 0
        
        # 基于互动数据
        intent_score += min(video["comments"] / 100, 10)
        intent_score += min(video["likes"] / 1000, 5)
        intent_score += min(video["shares"] / 100, 5)
        
        # 基于关键词
        if video["keyword"] in ["投资", "理财", "AI财库"]:
            intent_score += 5
        
        # 基于情感
        if video["sentiment"] == "positive":
            intent_score += 3
        
        video["intent_score"] = round(intent_score, 2)
        
        if intent_score > 10:  # 高潜力视频阈值
            high_potential_videos.append(video)
    
    # 按投资意向排序
    videos_sorted = sorted(videos, key=lambda x: x["intent_score"], reverse=True)
    
    print(f"📺 监控到视频数: {len(videos)}")
    print(f"🎯 高潜力视频数: {len(high_potential_videos)}")
    
    if videos_sorted:
        top_video = videos_sorted[0]
        print(f"🏆 最高潜力视频: {top_video['title']}")
        print(f"   作者: {top_video['author']} | 播放: {top_video['views']:,}")
        print(f"   意向分数: {top_video['intent_score']} | 关键词: {top_video['keyword']}")
    
    return videos_sorted, high_potential_videos

def extract_comments(video, max_comments=20):
    """提取视频评论（模拟）"""
    print(f"\n💬 分析视频评论: {video['title'][:30]}...")
    
    comments = []
    investment_comments = []
    
    # 模拟评论
    comment_templates = [
        "这个投资机会不错",
        "怎么参与这个项目？",
        "收益率怎么样？",
        "有风险吗？",
        "需要多少资金？",
        "AI财库是什么？",
        "RWA项目靠谱吗？",
        "在哪里可以了解更多？",
        "有联系方式吗？",
        "这个项目有白皮书吗？"
    ]
    
    for i in range(min(video["comments"], max_comments)):
        comment = {
            "comment_id": f"comment_{random.randint(10000, 99999)}",
            "user": f"用户_{random.randint(1000, 9999)}",
            "content": random.choice(comment_templates),
            "likes": random.randint(0, 100),
            "time": (datetime.now() - timedelta(minutes=random.randint(1, 120))).strftime("%H:%M"),
            "has_investment_intent": random.random() > 0.7  # 30%有投资意向
        }
        comments.append(comment)
        
        if comment["has_investment_intent"]:
            investment_comments.append(comment)
    
    print(f"   📝 总评论数: {len(comments)}")
    print(f"   🎯 投资意向评论: {len(investment_comments)}")
    
    return comments, investment_comments

def generate_engagement_strategy(videos, investment_comments):
    """生成互动策略"""
    print(f"\n🎯 互动策略生成")
    print("=" * 60)
    
    strategy = {
        "videos_to_engage": [],
        "comments_to_reply": [],
        "users_to_contact": [],
        "scheduled_actions": []
    }
    
    # 视频互动策略
    for video in videos[:3]:  # 前3个高潜力视频
        action = {
            "type": "video_engagement",
            "video_id": video["video_id"],
            "title": video["title"],
            "actions": [
                {"action": "like", "priority": "high"},
                {"action": "comment", "priority": "high", 
                 "template": "这个{keyword}内容很有价值，我们有一个AI财库支持的RWA项目可能适合您。"},
                {"action": "share", "priority": "medium"}
            ],
            "scheduled_time": "立即执行"
        }
        strategy["videos_to_engage"].append(action)
    
    # 评论回复策略
    for comment in investment_comments[:5]:  # 前5个有投资意向的评论
        reply = {
            "type": "comment_reply",
            "comment_id": comment["comment_id"],
            "user": comment["user"],
            "original_comment": comment["content"],
            "reply_template": "您好，{user}！看到您对投资感兴趣，我们有一个AI财库支持的RWA项目，年化收益18-25%，可以私信了解更多。",
            "priority": "high",
            "scheduled_time": "10分钟内"
        }
        strategy["comments_to_reply"].append(reply)
        
        # 添加到私信列表
        dm = {
            "type": "direct_message",
            "user": comment["user"],
            "reason": "评论显示投资意向",
            "message": "您好，看到您在视频下的评论，对投资很感兴趣。我们有一个托管账户控制的RWA项目，资方完全控制现金流，有兴趣了解一下吗？",
            "priority": "medium",
            "scheduled_time": "1小时后"
        }
        strategy["users_to_contact"].append(dm)
    
    # 打印策略摘要
    print(f"📺 视频互动计划: {len(strategy['videos_to_engage'])}个")
    print(f"💬 评论回复计划: {len(strategy['comments_to_reply'])}个")
    print(f"📩 私信联系计划: {len(strategy['users_to_contact'])}个")
    
    return strategy

def save_monitoring_results(keywords, videos, strategy):
    """保存监控结果"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "data/douyin_monitor"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f"{output_dir}/monitor_{timestamp}.json"
    
    results = {
        "monitor_time": datetime.now().isoformat(),
        "keywords": keywords,
        "videos_found": len(videos),
        "high_potential_videos": len([v for v in videos if v["intent_score"] > 10]),
        "videos": videos[:10],  # 只保存前10个视频
        "engagement_strategy": strategy,
        "summary": {
            "total_potential_leads": len(strategy["users_to_contact"]),
            "avg_intent_score": round(sum(v["intent_score"] for v in videos) / len(videos), 2) if videos else 0,
            "next_check_time": (datetime.now() + timedelta(minutes=10)).strftime("%H:%M")
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 监控结果已保存到: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description="抖音投资内容监控")
    parser.add_argument("--keywords", type=str, default="投资,理财,AI财库", help="监控关键词，用逗号分隔")
    parser.add_argument("--interval", type=int, default=10, help="监控间隔（分钟）")
    parser.add_argument("--output", type=str, help="输出文件路径")
    
    args = parser.parse_args()
    
    keywords = [k.strip() for k in args.keywords.split(",")]
    
    print("=" * 60)
    print("📱 抖音投资内容监控工具")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    
    # 合并配置中的关键词
    all_keywords = list(set(keywords + config["strategies"]["investment_keywords"]))
    print(f"🔍 使用关键词: {', '.join(all_keywords[:5])}...")
    
    # 模拟监控
    videos = simulate_douyin_monitoring(all_keywords, args.interval)
    
    # 分析视频
    videos_sorted, high_potential_videos = analyze_videos(videos, all_keywords)
    
    # 提取评论（模拟第一个高潜力视频）
    if high_potential_videos:
        comments, investment_comments = extract_comments(high_potential_videos[0])
    else:
        comments, investment_comments = [], []
    
    # 生成互动策略
    strategy = generate_engagement_strategy(high_potential_videos, investment_comments)
    
    # 保存结果
    output_file = save_monitoring_results(all_keywords, videos_sorted, strategy)
    
    print("\n✅ 监控完成!")
    print(f"📋 发现 {len(videos)} 个相关视频")
    print(f"🎯 识别 {len(high_potential_videos)} 个高潜力视频")
    print(f"💬 提取 {len(investment_comments)} 个投资意向评论")
    
    # 建议
    print("\n📋 建议行动:")
    print("1. 立即执行视频互动计划")
    print("2. 回复有投资意向的评论")
    print("3. 安排私信联系潜在用户")
    print("4. 设置定时监控任务")

if __name__ == "__main__":
    main()
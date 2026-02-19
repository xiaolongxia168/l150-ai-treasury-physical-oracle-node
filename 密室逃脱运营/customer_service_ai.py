#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
密室逃脱 - 智能客服AI
功能：7×24自动回复 + 多平台接入 + 知识库管理
"""

import json
import re
from datetime import datetime
from pathlib import Path

class EscapeRoomCustomerServiceAI:
    def __init__(self, workspace_path="/Users/xiaolongxia/.openclaw/workspace/密室逃脱运营"):
        self.workspace = Path(workspace_path)
        self.kb_dir = self.workspace / "客服" / "知识库"
        self.chat_dir = self.workspace / "客服" / "对话记录"
        self.log_dir = self.workspace / "日志"
        
        for dir_path in [self.kb_dir, self.chat_dir, self.log_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.knowledge_base = self._load_knowledge_base()
        self.log(f"智能客服AI初始化完成")
    
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = self.log_dir / f"cs_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"[CS AI] {message}")
    
    def _load_knowledge_base(self):
        """加载知识库"""
        kb_file = self.kb_dir / "knowledge_base.json"
        
        if kb_file.exists():
            with open(kb_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # 创建默认知识库
        default_kb = {
            "version": "1.0",
            "last_update": datetime.now().isoformat(),
            "categories": {
                "pricing": {
                    "keywords": ["价格", "多少钱", "费用", "团购", "优惠", "便宜", "贵"],
                    "responses": [
                        "您好！我们目前有多个主题可选，价格从{price_range}不等。现在预订还有{discount}优惠哦！",
                        "我们的团购套餐非常划算！平日票{weekday_price}元，周末{weekend_price}元。点击下方链接立即预订 👇"
                    ],
                    "data": {
                        "price_range": "88-168元",
                        "discount": "8折",
                        "weekday_price": "88",
                        "weekend_price": "128"
                    }
                },
                "themes": {
                    "keywords": ["主题", "有什么", "推荐", "恐怖", "悬疑", "解谜", "剧情"],
                    "responses": [
                        "我们有5大热门主题：\n🎭 {theme_1}\n🎭 {theme_2}\n🎭 {theme_3}\n🎭 {theme_4}\n🎭 {theme_5}\n\n每个主题时长60-90分钟，您偏好哪种风格？",
                        "强烈推荐我们的招牌主题《{top_theme}》！{theme_desc} 适合{player_count}人体验~"
                    ],
                    "data": {
                        "theme_1": "午夜凶铃（恐怖）",
                        "theme_2": "福尔摩斯（推理）",
                        "theme_3": "古墓丽影（冒险）",
                        "theme_4": "时间裂缝（科幻）",
                        "theme_5": "民国往事（剧情）",
                        "top_theme": "午夜凶铃",
                        "theme_desc": "沉浸式恐怖体验，真人NPC互动",
                        "player_count": "4-8"
                    }
                },
                "booking": {
                    "keywords": ["预订", "预约", "订场", "时间", "场次", "空位"],
                    "responses": [
                        "预订很简单！请告诉我：\n1️⃣ 选择主题\n2️⃣ 选择日期和时间\n3️⃣ 确认人数\n\n我来为您查询空位~",
                        "今天的场次还有：{today_slots}\n明天：{tomorrow_slots}\n您想订哪个时段？"
                    ],
                    "data": {
                        "today_slots": "14:00, 16:00, 19:00, 21:00",
                        "tomorrow_slots": "10:00, 14:00, 16:00, 19:00, 21:00"
                    }
                },
                "location": {
                    "keywords": ["地址", "在哪", "位置", "怎么去", "停车", "地铁", "公交"],
                    "responses": [
                        "📍 我们的地址是：{address}\n\n🚇 地铁：{metro}\n🚌 公交：{bus}\n🅿️ 停车：{parking}",
                        "我们在{location_name}，{landmark}旁边，很显眼的位置~"
                    ],
                    "data": {
                        "address": "待填写",
                        "metro": "待填写",
                        "bus": "待填写",
                        "parking": "待填写",
                        "location_name": "待填写",
                        "landmark": "待填写"
                    }
                },
                "refund": {
                    "keywords": ["退款", "取消", "改期", "退钱", "能退吗"],
                    "responses": [
                        "关于退款政策：\n✅ 提前24小时取消：全额退款\n✅ 提前12小时：退款80%\n❌ 当天取消：不可退款\n\n如需改期，请提前联系~",
                        "特殊情况（如疫情、极端天气）可以申请特殊处理，我们会尽力协助！"
                    ],
                    "data": {}
                },
                "requirements": {
                    "keywords": ["年龄", "限制", "几个人", "人数", "小孩", "儿童", "孕妇"],
                    "responses": [
                        "参与要求：\n👥 人数：{min_players}-{max_players}人/场\n🎂 年龄：{age_limit}\n⚠️ 注意事项：{notes}",
                        "恐怖主题建议16岁以上，解谜主题10岁以上都可以玩~"
                    ],
                    "data": {
                        "min_players": "2",
                        "max_players": "8",
                        "age_limit": "10岁以上（恐怖主题16+）",
                        "notes": "心脏病、高血压患者及孕妇不建议参与"
                    }
                },
                "hours": {
                    "keywords": ["营业时间", "几点", "关门", "开门", "营业到"],
                    "responses": [
                        "⏰ 营业时间：\n周一至周五：{weekday_hours}\n周末及节假日：{weekend_hours}\n\n最晚入场时间：{last_entry}",
                        "建议提前30分钟到店，可以挑选角色和熟悉规则~"
                    ],
                    "data": {
                        "weekday_hours": "13:00-22:00",
                        "weekend_hours": "10:00-23:00",
                        "last_entry": "21:00"
                    }
                }
            },
            "default_responses": [
                "您好！欢迎咨询我们的密室逃脱~ 请问有什么可以帮您的？",
                "收到您的问题！让我为您解答...",
                "这个咨询有点复杂，我为您转接人工客服，请稍等~"
            ],
            "escort_keywords": ["投诉", "差评", "经理", "老板", "人工", "客服", "退钱", "举报"]
        }
        
        with open(kb_file, "w", encoding="utf-8") as f:
            json.dump(default_kb, f, ensure_ascii=False, indent=2)
        
        self.log(f"创建默认知识库: {kb_file}")
        return default_kb
    
    def detect_intent(self, message):
        """意图识别"""
        message = message.lower()
        
        for category, data in self.knowledge_base["categories"].items():
            for keyword in data["keywords"]:
                if keyword in message:
                    return category
        
        return "default"
    
    def detect_emotion(self, message):
        """情绪检测"""
        negative_words = ["差", "垃圾", "坑", "骗", "气", "失望", "不爽", "差评", "投诉"]
        positive_words = ["好", "棒", "赞", "喜欢", "满意", "不错", "推荐", "好玩"]
        urgent_words = ["急", "马上", "立刻", "现在", "快"]
        
        emotion_score = 0
        
        for word in negative_words:
            if word in message:
                emotion_score -= 1
        
        for word in positive_words:
            if word in message:
                emotion_score += 1
        
        urgency = any(word in message for word in urgent_words)
        
        if emotion_score < 0:
            return "negative", urgency
        elif emotion_score > 0:
            return "positive", urgency
        else:
            return "neutral", urgency
    
    def generate_response(self, message, platform="unknown"):
        """生成回复"""
        timestamp = datetime.now().isoformat()
        
        # 检测意图
        intent = self.detect_intent(message)
        emotion, urgency = self.detect_emotion(message)
        
        # 检查是否需要转人工
        for keyword in self.knowledge_base.get("escort_keywords", []):
            if keyword in message:
                response = "[SYSTEM] 触发人工转接 - 关键词匹配"
                self._log_conversation(timestamp, platform, message, response, intent, emotion, True)
                return response
        
        # 负面情绪且紧急
        if emotion == "negative" and urgency:
            response = self.knowledge_base["default_responses"][2]
            self._log_conversation(timestamp, platform, message, response, intent, emotion, True)
            return response
        
        # 根据意图生成回复
        if intent in self.knowledge_base["categories"]:
            category_data = self.knowledge_base["categories"][intent]
            import random
            template = random.choice(category_data["responses"])
            response = template.format(**category_data.get("data", {}))
        else:
            response = self.knowledge_base["default_responses"][0]
        
        # 情绪安抚
        if emotion == "negative":
            response = "非常抱歉给您带来不好的体验！" + response
        
        self._log_conversation(timestamp, platform, message, response, intent, emotion, False)
        return response
    
    def _log_conversation(self, timestamp, platform, user_msg, ai_response, intent, emotion, escalated):
        """记录对话"""
        log_entry = {
            "timestamp": timestamp,
            "platform": platform,
            "user_message": user_msg,
            "ai_response": ai_response,
            "intent": intent,
            "emotion": emotion,
            "escalated": escalated
        }
        
        log_file = self.chat_dir / f"conversations_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    def simulate_conversation(self, test_messages=None):
        """模拟对话测试"""
        if not test_messages:
            test_messages = [
                ("douyin", "多少钱一个人？"),
                ("meituan", "有什么主题推荐？"),
                ("xiaohongshu", "地址在哪里？"),
                ("wechat", "可以退款吗？"),
                ("douyin", "太差了！我要投诉！")
            ]
        
        self.log("=" * 50)
        self.log("开始模拟对话测试")
        self.log("=" * 50)
        
        for platform, msg in test_messages:
            response = self.generate_response(msg, platform)
            print(f"\n[{platform}] 用户: {msg}")
            print(f"[AI] 回复: {response}")
        
        self.log("=" * 50)
        self.log("模拟测试完成")
        self.log("=" * 50)
    
    def update_knowledge_base(self, category, data):
        """更新知识库"""
        if category in self.knowledge_base["categories"]:
            self.knowledge_base["categories"][category]["data"].update(data)
            self.knowledge_base["last_update"] = datetime.now().isoformat()
            
            kb_file = self.kb_dir / "knowledge_base.json"
            with open(kb_file, "w", encoding="utf-8") as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
            
            self.log(f"更新知识库[{category}]: {data}")
            return True
        return False
    
    def get_stats(self):
        """获取客服统计"""
        today = datetime.now().strftime('%Y%m%d')
        log_file = self.chat_dir / f"conversations_{today}.jsonl"
        
        stats = {
            "total_conversations": 0,
            "by_platform": {},
            "by_intent": {},
            "escalation_rate": 0,
            "emotion_distribution": {"positive": 0, "neutral": 0, "negative": 0}
        }
        
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    entry = json.loads(line.strip())
                    stats["total_conversations"] += 1
                    stats["by_platform"][entry["platform"]] = stats["by_platform"].get(entry["platform"], 0) + 1
                    stats["by_intent"][entry["intent"]] = stats["by_intent"].get(entry["intent"], 0) + 1
                    stats["emotion_distribution"][entry["emotion"]] += 1
                    if entry["escalated"]:
                        stats["escalation_rate"] += 1
            
            if stats["total_conversations"] > 0:
                stats["escalation_rate"] = stats["escalation_rate"] / stats["total_conversations"]
        
        return stats


if __name__ == "__main__":
    cs_ai = EscapeRoomCustomerServiceAI()
    
    print("\n" + "=" * 60)
    print("🤖 智能客服AI测试启动")
    print("=" * 60)
    
    # 运行模拟对话
    cs_ai.simulate_conversation()
    
    # 输出统计
    stats = cs_ai.get_stats()
    print(f"\n📊 今日对话统计:")
    print(f"   总对话数: {stats['total_conversations']}")
    print(f"   转人工率: {stats['escalation_rate']:.1%}")
    print(f"   情绪分布: {stats['emotion_distribution']}")
    
    print("\n✅ 智能客服AI测试完成!")

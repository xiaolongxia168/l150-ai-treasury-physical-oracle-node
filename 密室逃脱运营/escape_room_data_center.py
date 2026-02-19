#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
密室逃脱超级运营团队 - 数据抓取核心模块
支持：抖音来客、美团开店宝、竞品监控
"""

import json
import csv
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

# 数据目录配置
BASE_DIR = Path("/Users/xiaolongxia/.openclaw/workspace/密室逃脱运营")
DATA_DIR = BASE_DIR / "数据"
ANALYSIS_DIR = BASE_DIR / "分析"
CONTENT_DIR = BASE_DIR / "内容"
REPORT_DIR = BASE_DIR / "报告"

# 确保目录存在
for dir_path in [DATA_DIR, ANALYSIS_DIR, CONTENT_DIR, REPORT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

class DataManager:
    """数据管理器 - 统一处理所有数据存储"""
    
    def __init__(self):
        self.douyin_file = DATA_DIR / "douyin_data.json"
        self.meituan_file = DATA_DIR / "meituan_data.json"
        self.competitor_file = DATA_DIR / "competitor_data.json"
        
    def save_douyin_data(self, data):
        """保存抖音来客数据"""
        timestamp = datetime.now().isoformat()
        record = {
            "timestamp": timestamp,
            "data": data
        }
        
        existing = self._load_json(self.douyin_file)
        if not isinstance(existing, list):
            existing = []
        existing.append(record)
        
        self._save_json(self.douyin_file, existing)
        print(f"✅ 抖音数据已保存: {timestamp}")
        return True
    
    def save_meituan_data(self, data):
        """保存美团开店宝数据"""
        timestamp = datetime.now().isoformat()
        record = {
            "timestamp": timestamp,
            "data": data
        }
        
        existing = self._load_json(self.meituan_file)
        if not isinstance(existing, list):
            existing = []
        existing.append(record)
        
        self._save_json(self.meituan_file, existing)
        print(f"✅ 美团数据已保存: {timestamp}")
        return True
    
    def save_competitor_data(self, competitor_name, data):
        """保存竞品数据"""
        timestamp = datetime.now().isoformat()
        
        competitor_dir = DATA_DIR / "竞品"
        competitor_dir.mkdir(exist_ok=True)
        
        file_path = competitor_dir / f"{competitor_name}.json"
        
        existing = self._load_json(file_path)
        if not isinstance(existing, list):
            existing = []
        
        record = {
            "timestamp": timestamp,
            "data": data
        }
        existing.append(record)
        
        self._save_json(file_path, existing)
        print(f"✅ 竞品数据已保存: {competitor_name} @ {timestamp}")
        return True
    
    def get_latest_douyin(self):
        """获取最新抖音数据"""
        data = self._load_json(self.douyin_file)
        if isinstance(data, list) and len(data) > 0:
            return data[-1]
        return None
    
    def get_latest_meituan(self):
        """获取最新美团数据"""
        data = self._load_json(self.meituan_file)
        if isinstance(data, list) and len(data) > 0:
            return data[-1]
        return None
    
    def get_all_competitors(self):
        """获取所有竞品最新数据"""
        competitor_dir = DATA_DIR / "竞品"
        if not competitor_dir.exists():
            return {}
        
        result = {}
        for file_path in competitor_dir.glob("*.json"):
            data = self._load_json(file_path)
            if isinstance(data, list) and len(data) > 0:
                result[file_path.stem] = data[-1]
        return result
    
    def _load_json(self, file_path):
        """加载JSON文件"""
        if not file_path.exists():
            return []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_json(self, file_path, data):
        """保存JSON文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class AnalysisEngine:
    """分析引擎 - 数据分析与洞察生成"""
    
    def __init__(self):
        self.data_manager = DataManager()
        
    def generate_daily_report(self):
        """生成每日运营报告"""
        douyin = self.data_manager.get_latest_douyin()
        meituan = self.data_manager.get_latest_meituan()
        competitors = self.data_manager.get_all_competitors()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "douyin_summary": self._analyze_douyin(douyin),
            "meituan_summary": self._analyze_meituan(meituan),
            "competitor_summary": self._analyze_competitors(competitors),
            "recommendations": self._generate_recommendations(douyin, meituan, competitors)
        }
        
        # 保存报告
        report_file = REPORT_DIR / f"daily_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 每日报告已生成: {report_file}")
        return report
    
    def _analyze_douyin(self, data):
        """分析抖音数据"""
        if not data:
            return {"status": "无数据", "insights": []}
        
        insights = []
        # 这里可以根据实际数据结构添加分析逻辑
        
        return {
            "status": "正常",
            "last_update": data.get("timestamp"),
            "insights": insights
        }
    
    def _analyze_meituan(self, data):
        """分析美团数据"""
        if not data:
            return {"status": "无数据", "insights": []}
        
        insights = []
        
        return {
            "status": "正常",
            "last_update": data.get("timestamp"),
            "insights": insights
        }
    
    def _analyze_competitors(self, competitors):
        """分析竞品数据"""
        if not competitors:
            return {"status": "无数据", "competitor_count": 0}
        
        return {
            "status": "正常",
            "competitor_count": len(competitors),
            "competitors": list(competitors.keys())
        }
    
    def _generate_recommendations(self, douyin, meituan, competitors):
        """生成运营建议"""
        recommendations = []
        
        if not douyin:
            recommendations.append("⚠️ 抖音数据缺失，请检查数据抓取")
        if not meituan:
            recommendations.append("⚠️ 美团数据缺失，请检查数据抓取")
        if not competitors:
            recommendations.append("⚠️ 竞品数据缺失，请配置竞品监控")
        
        return recommendations


class ContentGenerator:
    """内容生成器 - 爆款内容创作"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """加载内容模板"""
        templates_file = CONTENT_DIR / "爆款灵感库.md"
        
        # 默认模板
        default_templates = {
            "hook_templates": [
                "99%的人都逃不出去的密室，你敢挑战吗？",
                "这个密室的结局让我彻底破防了...",
                "沉浸式密室体验，代入感直接拉满！",
                "解密这个机关花了我们整整1小时",
                "恐怖密室实录，胆小慎入！"
            ],
            "script_structure": [
                "黄金3秒钩子",
                "悬念剧情片段",
                "玩家真实反应",
                "主题亮点展示",
                "优惠信息",
                "行动号召"
            ],
            "cta_templates": [
                "点击左下角团购，立省{discount}元！",
                "周末场次紧张，赶紧预约！",
                "带上你的胆大的朋友来挑战！",
                "评论区告诉我你敢不敢来！"
            ]
        }
        
        return default_templates
    
    def generate_video_script(self, theme="恐怖", discount=20):
        """生成视频脚本"""
        import random
        
        hook = random.choice(self.templates["hook_templates"])
        cta = random.choice(self.templates["cta_templates"]).format(discount=discount)
        
        script = {
            "title": f"【{theme}主题】{hook}",
            "hook": hook,
            "structure": self.templates["script_structure"],
            "cta": cta,
            "hashtags": ["#密室逃脱", f"#{theme}密室", "#沉浸式体验", "#周末去哪儿", "#团建好去处"],
            "suggested_bgm": "悬疑/紧张/节奏感强的音乐",
            "duration": "15-30秒",
            "optimal_post_time": "18:00-20:00"
        }
        
        # 保存脚本
        script_file = CONTENT_DIR / f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(script_file, 'w', encoding='utf-8') as f:
            json.dump(script, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 视频脚本已生成: {script_file}")
        return script
    
    def generate_weekly_content_plan(self):
        """生成一周内容计划"""
        plan = {
            "week_of": datetime.now().isoformat(),
            "content_schedule": [
                {"day": "周一", "type": "主题预告", "focus": "新品推广"},
                {"day": "周二", "type": "玩家实况", "focus": "真实体验"},
                {"day": "周三", "type": "攻略教学", "focus": "价值输出"},
                {"day": "周四", "type": "玩家实况", "focus": "真实体验"},
                {"day": "周五", "type": "优惠活动", "focus": "周末引流"},
                {"day": "周六", "type": "玩家实况", "focus": "周末热度"},
                {"day": "周日", "type": "幕后花絮", "focus": "粉丝互动"}
            ]
        }
        
        plan_file = CONTENT_DIR / f"weekly_plan_{datetime.now().strftime('%Y%m%d')}.json"
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 周内容计划已生成: {plan_file}")
        return plan


# 命令行入口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("""
密室逃脱超级运营团队 - 数据中心

用法:
  python3 escape_room_data_center.py <command> [options]

命令:
  report          生成每日运营报告
  script          生成视频脚本
  weekly          生成周内容计划
  status          查看数据状态
  import_douyin   导入抖音数据 (CSV文件路径)
  import_meituan  导入美团数据 (CSV文件路径)
        """)
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "report":
        engine = AnalysisEngine()
        engine.generate_daily_report()
    
    elif command == "script":
        generator = ContentGenerator()
        script = generator.generate_video_script()
        print("\n" + "="*50)
        print("生成的脚本:")
        print("="*50)
        print(json.dumps(script, ensure_ascii=False, indent=2))
    
    elif command == "weekly":
        generator = ContentGenerator()
        generator.generate_weekly_content_plan()
    
    elif command == "status":
        dm = DataManager()
        print("\n" + "="*50)
        print("数据状态概览")
        print("="*50)
        
        douyin = dm.get_latest_douyin()
        meituan = dm.get_latest_meituan()
        competitors = dm.get_all_competitors()
        
        print(f"\n抖音数据: {'✅ 最新 @ ' + douyin['timestamp'] if douyin else '❌ 无数据'}")
        print(f"美团数据: {'✅ 最新 @ ' + meituan['timestamp'] if meituan else '❌ 无数据'}")
        print(f"竞品监控: {'✅ ' + str(len(competitors)) + '个竞品' if competitors else '❌ 无数据'}")
        if competitors:
            for name in competitors.keys():
                print(f"  - {name}")
    
    else:
        print(f"未知命令: {command}")

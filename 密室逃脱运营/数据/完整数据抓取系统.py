#!/usr/bin/env python3
"""
密室逃脱运营数据抓取系统
自动抓取抖音来客 + 美团开店宝数据
"""

import json
import csv
import time
from datetime import datetime, timedelta
from pathlib import Path
import re

class DataScraper:
    def __init__(self):
        self.data_dir = Path.home() / ".openclaw/workspace/密室逃脱运营/数据"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def scrape_douyin_data(self):
        """
        抖音来客数据抓取
        需要手动登录后运行，或提供Cookie
        """
        print("🎵 开始抓取抖音来客数据...")
        
        # 数据抓取配置
        douyin_config = {
            "login_url": "https://e.douyin.com/",
            "data_pages": [
                "/data/shop",
                "/data/video", 
                "/data/live",
                "/data/fans"
            ],
            "extract_fields": {
                "video_data": [
                    "publish_time", "title", "play_count", "like_count",
                    "comment_count", "share_count", "completion_rate",
                    "product_click", "order_count", "gmv"
                ],
                "fan_data": [
                    "date", "total_fans", "new_fans", "fan_profile", "active_time"
                ],
                "live_data": [
                    "date", "duration", "viewers", "interaction_rate", "conversion"
                ],
                "conversion_data": [
                    "date", "gmv", "orders", "verification_rate", "avg_price"
                ]
            }
        }
        
        # 保存配置
        config_file = self.data_dir / "douyin_scraper_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(douyin_config, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 抖音抓取配置已保存: {config_file}")
        return douyin_config
    
    def scrape_meituan_data(self):
        """
        美团开店宝数据抓取
        """
        print("🍜 开始抓取美团开店宝数据...")
        
        meituan_config = {
            "login_url": "https://e.waimai.meituan.com/",
            "data_pages": [
                "/data/flow",
                "/data/trade",
                "/data/evaluate",
                "/data/compete"
            ],
            "extract_fields": {
                "flow_data": [
                    "date", "exposure", "visit", "click_rate", "conversion"
                ],
                "trade_data": [
                    "date", "orders", "revenue", "avg_price", "refund_rate"
                ],
                "evaluate_data": [
                    "date", "rating", "positive", "negative", "keywords"
                ],
                "compete_data": [
                    "date", "rank", "flow_source", "competitor_activity"
                ]
            }
        }
        
        config_file = self.data_dir / "meituan_scraper_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(meituan_config, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 美团抓取配置已保存: {config_file}")
        return meituan_config
    
    def create_scraper_script(self):
        """
        创建Playwright自动化抓取脚本
        """
        scraper_code = '''#!/usr/bin/env python3
"""
Playwright自动化数据抓取脚本
运行前请确保已安装: pip install playwright
并安装浏览器: playwright install
"""

import asyncio
import json
import csv
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

class AutoScraper:
    def __init__(self):
        self.data_dir = Path.home() / ".openclaw/workspace/密室逃脱运营/数据"
        self.results = {}
        
    async def scrape_douyin(self, page):
        """抓取抖音来客数据"""
        print("🎵 抓取抖音数据...")
        
        # 等待页面加载
        await page.wait_for_load_state('networkidle')
        
        # 抓取视频数据
        video_data = []
        try:
            # 点击数据菜单
            await page.click('text=数据')
            await page.wait_for_timeout(2000)
            
            # 点击视频分析
            await page.click('text=视频分析')
            await page.wait_for_timeout(3000)
            
            # 提取视频列表数据
            videos = await page.query_selector_all('.video-item')  # 需要根据实际页面调整选择器
            
            for video in videos[:20]:  # 抓取前20条
                try:
                    title = await video.query_selector_eval('.video-title', 'el => el.textContent')
                    plays = await video.query_selector_eval('.play-count', 'el => el.textContent')
                    likes = await video.query_selector_eval('.like-count', 'el => el.textContent')
                    
                    video_data.append({
                        'title': title,
                        'plays': plays,
                        'likes': likes,
                        'scraped_at': datetime.now().isoformat()
                    })
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ 抖音数据抓取部分失败: {e}")
            
        self.results['douyin_videos'] = video_data
        return video_data
    
    async def scrape_meituan(self, page):
        """抓取美团开店宝数据"""
        print("🍜 抓取美团数据...")
        
        await page.wait_for_load_state('networkidle')
        
        meituan_data = []
        try:
            # 点击经营分析
            await page.click('text=经营分析')
            await page.wait_for_timeout(2000)
            
            # 抓取交易数据
            # 这里需要根据实际页面结构调整
            
        except Exception as e:
            print(f"⚠️ 美团数据抓取部分失败: {e}")
            
        self.results['meituan'] = meituan_data
        return meituan_data
    
    def save_results(self):
        """保存抓取结果"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存为JSON
        json_file = self.data_dir / f"scraped_data_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
            
        # 保存为CSV（如果有视频数据）
        if 'douyin_videos' in self.results:
            csv_file = self.data_dir / f"douyin_videos_{timestamp}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if self.results['douyin_videos']:
                    writer = csv.DictWriter(f, fieldnames=self.results['douyin_videos'][0].keys())
                    writer.writeheader()
                    writer.writerows(self.results['douyin_videos'])
                    
        print(f"✅ 数据已保存到: {self.data_dir}")
        return json_file

async def main():
    scraper = AutoScraper()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # 可见模式便于调试
        
        # 抓取抖音
        print("\\n🌐 打开抖音来客...")
        page = await browser.new_page()
        await page.goto('https://e.douyin.com/')
        print("⏳ 请在浏览器中完成登录，然后按回车继续...")
        input()
        
        await scraper.scrape_douyin(page)
        
        # 抓取美团
        print("\\n🌐 打开美团开店宝...")
        page2 = await browser.new_page()
        await page2.goto('https://e.waimai.meituan.com/')
        print("⏳ 请在浏览器中完成登录，然后按回车继续...")
        input()
        
        await scraper.scrape_meituan(page2)
        
        # 保存结果
        scraper.save_results()
        
        await browser.close()
        print("\\n✅ 数据抓取完成！")

if __name__ == '__main__':
    asyncio.run(main())
'''
        
        script_file = self.data_dir / "auto_scraper.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(scraper_code)
            
        print(f"✅ 自动化抓取脚本已创建: {script_file}")
        return script_file
    
    def create_data_processor(self):
        """
        创建数据处理和分析模块
        """
        processor_code = '''#!/usr/bin/env python3
"""
运营数据分析引擎
自动分析抓取的数据并生成运营建议
"""

import json
import pandas as pd
from datetime import datetime
from pathlib import Path

class DataAnalyzer:
    def __init__(self):
        self.data_dir = Path.home() / ".openclaw/workspace/密室逃脱运营/数据"
        self.analysis_dir = Path.home() / ".openclaw/workspace/密室逃脱运营/分析"
        self.analysis_dir.mkdir(exist_ok=True)
        
    def load_data(self, data_file):
        """加载抓取的数据"""
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def analyze_douyin(self, data):
        """分析抖音数据"""
        print("📊 分析抖音数据...")
        
        analysis = {
            'platform': '抖音来客',
            'analysis_time': datetime.now().isoformat(),
            'metrics': {}
        }
        
        if 'douyin_videos' in data:
            videos = data['douyin_videos']
            df = pd.DataFrame(videos)
            
            # 计算关键指标
            analysis['metrics'] = {
                'total_videos': len(videos),
                'avg_plays': df['plays'].mean() if 'plays' in df else 0,
                'avg_likes': df['likes'].mean() if 'likes' in df else 0,
                'engagement_rate': (df['likes'].sum() / df['plays'].sum() * 100) if 'plays' in df and 'likes' in df else 0
            }
            
            # 找出表现最好的视频
            if 'plays' in df:
                top_video = df.loc[df['plays'].idxmax()]
                analysis['top_performer'] = {
                    'title': top_video.get('title', ''),
                    'plays': top_video.get('plays', 0),
                    'likes': top_video.get('likes', 0)
                }
        
        return analysis
    
    def generate_insights(self, douyin_analysis, meituan_analysis):
        """生成运营洞察和建议"""
        print("💡 生成运营洞察...")
        
        insights = {
            'generated_at': datetime.now().isoformat(),
            'summary': {},
            'recommendations': [],
            'action_items': []
        }
        
        # 基于数据的建议
        if douyin_analysis.get('metrics', {}).get('engagement_rate', 0) < 5:
            insights['recommendations'].append({
                'priority': 'high',
                'area': '内容优化',
                'suggestion': '互动率偏低，建议增加互动引导话术',
                'action': '在视频结尾添加"评论告诉我你最想玩哪个主题"'
            })
        
        # 添加更多基于数据的建议...
        
        return insights
    
    def save_report(self, analysis, insights):
        """保存分析报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.analysis_dir / f"运营分析报告_{timestamp}.json"
        
        report = {
            'analysis': analysis,
            'insights': insights
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 分析报告已保存: {report_file}")
        return report_file

if __name__ == '__main__':
    analyzer = DataAnalyzer()
    # 这里可以添加实际的分析流程
    print("数据分析引擎已准备就绪！")
'''
        
        processor_file = self.data_dir / "data_analyzer.py"
        with open(processor_file, 'w', encoding='utf-8') as f:
            f.write(processor_code)
            
        print(f"✅ 数据分析引擎已创建: {processor_file}")
        return processor_file
    
    def create_content_generator(self):
        """
        创建爆款内容生成器
        """
        generator_code = '''#!/usr/bin/env python3
"""
爆款内容生成器
基于数据分析和跨行业灵感生成视频文案
"""

import json
import random
from datetime import datetime
from pathlib import Path

class ContentGenerator:
    def __init__(self):
        self.content_dir = Path.home() / ".openclaw/workspace/密室逃脱运营/内容"
        self.content_dir.mkdir(exist_ok=True)
        
        # 爆款标题模板
        self.title_templates = [
            "⚠️ 胆小慎入！这家密室让我{emotion}",
            "🔥 全网最火的密室主题，{achievement}！",
            "😱 99%的人都逃不出去的密室，{challenge}",
            "💡 密室逃脱必知的{number}个技巧",
            "🏆 我们仅用{time}就逃出来了！",
            "💰 人均{price}元，体验{feature}！",
            "🎭 玩完这个密室，我{reaction}...",
            "👻 和{relation}玩恐怖密室，结果...",
            "🤯 {subject}被碾压的一天",
            "🆚 {comparison}玩密室的区别"
        ]
        
        # 情绪词库
        self.emotions = ["吓哭了", "尖叫不止", "夜不能寐", "回味无穷", "欲罢不能"]
        self.achievements = ["终于打卡了", "排了3周队", "二刷都不够", "要带所有人来"]
        self.challenges = ["你敢挑战吗", "你能破纪录吗", "你能保持冷静吗"]
        
    def generate_video_script(self, theme="恐怖", difficulty="中等", players="4-6人"):
        """生成视频脚本"""
        
        # 生成标题
        title = self._generate_title(theme)
        
        # 脚本结构
        script = {
            'title': title,
            'theme': theme,
            'difficulty': difficulty,
            'players': players,
            'duration': '60-90秒',
            'structure': {
                'hook': self._generate_hook(theme),
                'setup': self._generate_setup(theme),
                'climax': self._generate_climax(theme),
                'cta': self._generate_cta()
            },
            'hashtags': self._generate_hashtags(theme),
            'bgm_suggestions': self._generate_bgm(theme),
            'generated_at': datetime.now().isoformat()
        }
        
        return script
    
    def _generate_title(self, theme):
        """生成爆款标题"""
        template = random.choice(self.title_templates)
        
        replacements = {
            'emotion': random.choice(self.emotions),
            'achievement': random.choice(self.achievements),
            'challenge': random.choice(self.challenges),
            'number': random.choice(['3', '5', '7']),
            'time': random.choice(['30分钟', '45分钟', '1小时']),
            'price': random.choice(['68', '88', '99', '128']),
            'feature': random.choice(['电影级场景', '沉浸式体验', '烧脑解谜']),
            'reaction': random.choice(['哭了', '笑了', '惊呆了']),
            'relation': random.choice(['暗恋对象', '闺蜜', '兄弟', '对象']),
            'subject': random.choice(['智商', '胆量', '体力']),
            'comparison': random.choice(['新手vs高手', '男生vs女生', '社牛vs社恐'])
        }
        
        title = template
        for key, value in replacements.items():
            title = title.replace('{' + key + '}', value)
            
        return title
    
    def _generate_hook(self, theme):
        """生成黄金3秒钩子"""
        hooks = {
            '恐怖': [
                "这个密室，让我整整一周不敢关灯睡觉...",
                "胆小勿入！这个主题的NPC会追着你在全馆跑...",
                "我敢打赌，你绝对撑不过前10分钟！"
            ],
            '悬疑': [
                "这个密室的剧情，比电影还精彩！",
                "我们解到最后才发现，真相竟然是...",
                "99%的人猜不到结局的密室主题！"
            ],
            '解谜': [
                "智商140以下别来挑战这个密室！",
                "这个密室的谜题，我们团队讨论了整整一周...",
                "号称最难密室，我们能否破纪录？"
            ]
        }
        
        return random.choice(hooks.get(theme, hooks['恐怖']))
    
    def _generate_setup(self, theme):
        """生成场景铺垫"""
        return "场景描述和氛围营造..."
    
    def _generate_climax(self, theme):
        """生成高潮部分"""
        return "最精彩的游戏片段和玩家反应..."
    
    def _generate_cta(self):
        """生成行动号召"""
        ctas = [
            "点击左下角团购，限时优惠中！",
            "评论区告诉我你最想挑战哪个主题！",
            "关注+点赞，下期带你解锁隐藏结局！",
            "快带上你的冤种朋友来挑战！"
        ]
        return random.choice(ctas)
    
    def _generate_hashtags(self, theme):
        """生成标签"""
        base_tags = ["#密室逃脱", "#密室", "#周末去哪儿", "#长沙密室"]
        theme_tags = {
            '恐怖': ["#恐怖密室", "#胆小慎入", "#刺激体验"],
            '悬疑': ["#悬疑推理", "#烧脑", "#剧本杀"],
            '解谜': ["#解谜游戏", "#智商挑战", "#推理"]
        }
        return base_tags + theme_tags.get(theme, [])
    
    def _generate_bgm(self, theme):
        """生成BGM建议"""
        bgms = {
            '恐怖': ["悬疑紧张BGM", "恐怖氛围音乐", "《小白船》变奏版"],
            '悬疑': ["推理侦探BGM", "紧张节奏音乐", "《名侦探柯南》BGM"],
            '解谜': ["轻快智力BGM", "挑战节奏音乐", "游戏闯关BGM"]
        }
        return bgms.get(theme, ["热门BGM"])
    
    def batch_generate(self, count=5):
        """批量生成内容"""
        contents = []
        themes = ['恐怖', '悬疑', '解谜']
        
        for i in range(count):
            theme = random.choice(themes)
            script = self.generate_video_script(theme)
            contents.append(script)
            
        # 保存生成的内容
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = self.content_dir / f"生成的脚本_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(contents, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 已生成{count}个视频脚本: {output_file}")
        return contents

if __name__ == '__main__':
    generator = ContentGenerator()
    generator.batch_generate(5)
'''
        
        generator_file = self.data_dir / "content_generator.py"
        with open(generator_file, 'w', encoding='utf-8') as f:
            f.write(generator_code)
            
        print(f"✅ 爆款内容生成器已创建: {generator_file}")
        return generator_file


def main():
    """主函数"""
    print("=" * 60)
    print("🚀 密室逃脱运营数据抓取系统")
    print("=" * 60)
    
    scraper = DataScraper()
    
    # 创建所有必要的组件
    print("\\n📦 正在创建数据抓取系统...")
    
    # 1. 创建平台配置
    douyin_config = scraper.scrape_douyin_data()
    meituan_config = scraper.scrape_meituan_data()
    
    # 2. 创建自动化抓取脚本
    scraper_script = scraper.create_scraper_script()
    
    # 3. 创建数据分析引擎
    analyzer_script = scraper.create_data_processor()
    
    # 4. 创建内容生成器
    generator_script = scraper.create_content_generator()
    
    print("\\n" + "=" * 60)
    print("✅ 系统部署完成！")
    print("=" * 60)
    print("\\n📋 使用步骤：")
    print("1. 安装依赖: pip install playwright pandas")
    print("2. 安装浏览器: playwright install")
    print("3. 运行抓取: python3", scraper_script.name)
    print("4. 分析数据: python3", analyzer_script.name)
    print("5. 生成内容: python3", generator_script.name)
    print("\\n📁 所有文件保存在:", scraper.data_dir)
    print("=" * 60)


if __name__ == '__main__':
    main()

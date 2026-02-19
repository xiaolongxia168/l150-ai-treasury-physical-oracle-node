#!/usr/bin/env python3
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

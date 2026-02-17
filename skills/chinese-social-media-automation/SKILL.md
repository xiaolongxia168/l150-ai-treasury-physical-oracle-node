---
name: chinese-social-media-automation
description: 中国社交媒体自动化技能 - 抖音、小红书、微博等平台的自动化发布、评论监控和精准目标投资粉截流
metadata:
 {
   "openclaw": {
     "emoji": "🇨🇳",
     "requires": {
       "bins": ["python3"],
       "env": ["CHINESE_SOCIAL_MEDIA_CONFIG"]
     },
     "primaryEnv": "CHINESE_SOCIAL_MEDIA_CONFIG"
   }
 }
---

# 中国社交媒体自动化技能

专门针对中国社交媒体平台（抖音、小红书、微博等）的自动化工具，支持精准目标投资粉截流、内容发布、评论监控和自动化互动。

## 功能特性

### 1. 平台支持
- **小红书 (Xiaohongshu)**: 内容发布、评论监控、精准用户搜索
- **抖音 (Douyin/TikTok)**: 短视频分析、评论互动、趋势监控
- **微博 (Weibo)**: 话题监控、大V互动、热点追踪
- **B站 (Bilibili)**: 二次元投资社区、UP主合作

### 2. 精准目标投资粉截流
- **关键词监控**: 监控"投资"、"理财"、"AI财库"、"RWA"等关键词
- **用户画像分析**: 识别高净值投资意向用户
- **自动化互动**: 智能评论回复、私信沟通
- **转化漏斗**: 从社交媒体到投资意向的完整转化路径

### 3. 自动化发布
- **内容生成**: AI生成符合平台调性的内容
- **定时发布**: 根据用户活跃时间自动发布
- **多账号管理**: 支持矩阵账号运营
- **数据优化**: 基于发布效果自动优化策略

### 4. 监控与分析
- **竞品监控**: 监控竞争对手的社交媒体活动
- **情感分析**: 分析用户评论的情感倾向
- **效果追踪**: 追踪转化率和ROI
- **预警系统**: 发现负面评论或危机信号

## 快速安装

```bash
# 克隆技能到工作空间
cd /Users/xiaolongxia/.openclaw/workspace/skills
git clone https://github.com/your-repo/chinese-social-media-automation.git

# 运行安装脚本
cd chinese-social-media-automation
chmod +x install.sh
./install.sh

# 编辑配置文件
vim ~/.openclaw/chinese_social_media.json
```

## 安装依赖

```bash
# 安装Python依赖
pip3 install schedule requests beautifulsoup4 selenium playwright
playwright install chromium

# 配置环境变量（可选）
export CHINESE_SOCIAL_MEDIA_CONFIG='{"xiaohongshu": {"username": "", "password": ""}, "douyin": {"username": "", "password": ""}}'
```

## 使用示例

### 1. 小红书自动化
```bash
# 搜索投资相关用户
python3 {baseDir}/scripts/xiaohongshu_search.py --keyword "投资理财" --limit 50

# 发布内容
python3 {baseDir}/scripts/xiaohongshu_post.py --title "L-150 RWA投资机会" --content "..." --images "img1.jpg,img2.jpg"

# 监控评论
python3 {baseDir}/scripts/xiaohongshu_monitor.py --interval 300
```

### 2. 抖音投资粉截流
```bash
# 监控投资相关视频
python3 {baseDir}/scripts/douyin_monitor.py --keywords "投资,理财,AI财库" --interval 600

# 自动评论互动
python3 {baseDir}/scripts/douyin_comment.py --video_id "123456" --comment "这个投资机会不错，可以私信了解更多RWA项目"

# 私信转化
python3 {baseDir}/scripts/douyin_dm.py --user_id "789012" --message "您好，看到您对投资感兴趣，我们有一个AI财库支持的RWA项目..."
```

### 3. 微博热点追踪
```bash
# 监控投资话题
python3 {baseDir}/scripts/weibo_monitor.py --topics "AI投资,RWA,数字资产" --interval 900

# 与大V互动
python3 {baseDir}/scripts/weibo_engagement.py --kols "投资大V1,财经博主2" --strategy "comment_and_share"
```

## 配置文件

创建 `~/.openclaw/chinese_social_media.json`:

```json
{
  "platforms": {
    "xiaohongshu": {
      "enabled": true,
      "username": "your_username",
      "password": "your_password",
      "cookies": "optional_cookies"
    },
    "douyin": {
      "enabled": true,
      "username": "your_username",
      "password": "your_password"
    },
    "weibo": {
      "enabled": true,
      "access_token": "your_access_token"
    }
  },
  "strategies": {
    "investment_keywords": ["投资", "理财", "AI财库", "RWA", "数字资产", "区块链投资"],
    "target_profiles": ["高净值", "企业家", "投资人", "基金经理", "AI研究员"],
    "response_templates": {
      "initial_contact": "您好，看到您对{keyword}感兴趣，我们有一个{project}项目可能适合您...",
      "follow_up": "感谢您的关注，这是更多详细信息...",
      "conversion": "如果您有兴趣深入了解，我们可以安排一个简短的会议..."
    }
  },
  "automation": {
    "posting_schedule": ["09:00", "12:00", "18:00", "21:00"],
    "monitoring_interval": 300,
    "max_daily_interactions": 50,
    "safety_delay": [5, 15]
  }
}
```

## 安全注意事项

1. **遵守平台规则**: 避免过度自动化导致账号被封
2. **隐私保护**: 不收集用户敏感信息
3. **内容合规**: 确保发布内容符合中国法律法规
4. **频率控制**: 合理控制互动频率，避免被识别为机器人

## 高级功能

### 1. AI内容生成
- 基于投资主题自动生成小红书笔记
- 生成抖音短视频脚本
- 创建微博话题讨论

### 2. 智能对话系统
- 自动回复用户评论和私信
- 识别投资意向并分级处理
- 引导用户进入转化漏斗

### 3. 数据分析仪表板
- 实时监控各平台表现
- 转化率分析和优化建议
- ROI计算和投资回报预测

## 故障排除

1. **登录失败**: 检查账号密码，可能需要验证码
2. **API限制**: 降低请求频率，使用代理IP
3. **内容审核**: 调整内容策略，避免敏感词
4. **性能问题**: 优化脚本，增加延迟和重试机制

## 更新日志

- v1.0.0: 初始版本，支持小红书、抖音、微博基础功能
- v1.1.0: 增加AI内容生成和智能对话
- v1.2.0: 添加数据分析仪表板和高级监控

## 贡献指南

欢迎提交PR改进功能或添加新平台支持。请确保代码质量和测试覆盖率。

## 许可证

MIT License
#!/bin/bash

# 中国社交媒体自动化技能安装脚本

echo "🇨🇳 中国社交媒体自动化技能安装"
echo "=" * 50

# 检查Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要Python3，请先安装: brew install python"
    exit 1
fi

echo "✅ Python3 已安装: $(python3 --version)"

# 安装Python依赖
echo "📦 安装Python依赖..."
pip3 install schedule requests beautifulsoup4 selenium playwright

if [ $? -eq 0 ]; then
    echo "✅ Python依赖安装成功"
else
    echo "⚠️  Python依赖安装可能有问题，请手动检查"
fi

# 安装Playwright浏览器
echo "🌐 安装Playwright浏览器..."
python3 -m playwright install chromium

if [ $? -eq 0 ]; then
    echo "✅ Playwright浏览器安装成功"
else
    echo "⚠️  Playwright安装可能有问题，请手动检查"
fi

# 创建数据目录
echo "📁 创建数据目录..."
mkdir -p data/xiaohongshu_search
mkdir -p data/douyin_monitor
mkdir -p data/weibo_trending
mkdir -p data/automation
mkdir -p logs

echo "✅ 数据目录创建完成"

# 创建配置文件
echo "⚙️  创建配置文件..."
CONFIG_FILE="$HOME/.openclaw/chinese_social_media.json"
if [ ! -f "$CONFIG_FILE" ]; then
    cp config_template.json "$CONFIG_FILE"
    echo "✅ 配置文件已创建: $CONFIG_FILE"
    echo "   请编辑此文件并填写您的平台账号信息"
else
    echo "⚠️  配置文件已存在: $CONFIG_FILE"
    echo "   如果需要更新，请手动备份后替换"
fi

# 设置脚本权限
echo "🔧 设置脚本权限..."
chmod +x scripts/*.py

echo "✅ 脚本权限设置完成"

# 创建OpenClaw技能链接
echo "🔗 创建OpenClaw技能链接..."
SKILLS_DIR="$HOME/.openclaw/workspace/skills"
if [ -d "$SKILLS_DIR" ]; then
    ln -sf "$(pwd)" "$SKILLS_DIR/chinese-social-media-automation" 2>/dev/null
    echo "✅ 技能链接创建完成"
else
    echo "⚠️  OpenClaw技能目录不存在: $SKILLS_DIR"
    echo "   请确保OpenClaw正确安装"
fi

# 创建Cron任务示例
echo "⏰ 创建Cron任务示例..."
CRON_EXAMPLE="cron_example.txt"
cat > "$CRON_EXAMPLE" << 'EOF'
# 中国社交媒体自动化Cron任务示例

# 每6小时运行小红书搜索
0 */6 * * * cd /path/to/chinese-social-media-automation && python3 scripts/xiaohongshu_search.py --keyword "投资" --limit 30 >> logs/xiaohongshu.log 2>&1

# 每30分钟运行抖音监控
*/30 * * * * cd /path/to/chinese-social-media-automation && python3 scripts/douyin_monitor.py --keywords "投资,理财,AI财库" --interval 30 >> logs/douyin.log 2>&1

# 每天9点和18点发布内容
0 9,18 * * * cd /path/to/chinese-social-media-automation && python3 scripts/automation_scheduler.py --test >> logs/posting.log 2>&1

# 每天23:30生成报告
30 23 * * * cd /path/to/chinese-social-media-automation && python3 scripts/automation_scheduler.py --test >> logs/report.log 2>&1
EOF

echo "✅ Cron示例已创建: $CRON_EXAMPLE"

# 测试运行
echo "🧪 测试运行..."
python3 scripts/automation_scheduler.py --test > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ 测试运行成功"
else
    echo "⚠️  测试运行可能有问题，请检查错误信息"
fi

echo ""
echo "🎉 安装完成!"
echo "=" * 50
echo ""
echo "📋 下一步操作:"
echo "1. 编辑配置文件: $CONFIG_FILE"
echo "   填写您的社交媒体账号信息"
echo ""
echo "2. 设置Cron任务:"
echo "   查看示例: cat $CRON_EXAMPLE"
echo "   添加到crontab: crontab -e"
echo ""
echo "3. 手动测试:"
echo "   cd $(pwd)"
echo "   python3 scripts/xiaohongshu_search.py --keyword \"投资\" --limit 10"
echo "   python3 scripts/douyin_monitor.py --keywords \"投资,理财\" --interval 10"
echo ""
echo "4. 启动自动化调度器:"
echo "   python3 scripts/automation_scheduler.py"
echo ""
echo "📚 文档:"
echo "   查看SKILL.md文件获取完整使用指南"
echo ""
echo "🆘 故障排除:"
echo "   1. 检查Python依赖: pip3 list | grep -E 'schedule|requests|beautifulsoup4|selenium|playwright'"
echo "   2. 检查Playwright: python3 -m playwright --version"
echo "   3. 检查配置文件: cat $CONFIG_FILE | head -20"
echo ""
echo "💡 提示:"
echo "   在实际使用前，请确保:"
echo "   - 遵守各平台的使用条款"
echo "   - 合理控制自动化频率"
echo "   - 准备应对验证码等安全措施"
echo "   - 定期备份数据"
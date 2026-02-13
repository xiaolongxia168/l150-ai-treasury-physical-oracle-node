#!/bin/bash
# L-150 邮件监控cron任务设置脚本

echo "🔧 设置L-150邮件监控cron任务"
echo "=" * 50

# 检查Python脚本
echo "1. 检查Python脚本..."
if [ -f "l150_email_monitor_simple.py" ]; then
    echo "   ✅ l150_email_monitor_simple.py 存在"
else
    echo "   ❌ l150_email_monitor_simple.py 不存在"
    exit 1
fi

# 测试Python脚本
echo "2. 测试Python脚本..."
python3 l150_email_monitor_simple.py
TEST_RESULT=$?

if [ $TEST_RESULT -eq 0 ]; then
    echo "   ✅ Python脚本测试成功"
else
    echo "   ⚠️ Python脚本测试失败，但继续设置cron"
fi

# 创建cron任务
echo "3. 创建cron任务配置..."
CRON_JOB="*/30 * * * * cd /Users/xiaolongxia/.openclaw/workspace && /usr/bin/python3 l150_email_monitor_simple.py >> /Users/xiaolongxia/.openclaw/workspace/memory/email-monitor/cron.log 2>&1"

echo "Cron任务配置:"
echo "$CRON_JOB"
echo ""

# 提供添加cron的指令
echo "4. 添加cron任务的方法:"
echo ""
echo "方法A - 使用crontab命令:"
echo "   crontab -e"
echo "   然后添加这一行:"
echo "   $CRON_JOB"
echo ""
echo "方法B - 使用OpenClaw cron工具:"
echo "   运行以下命令创建OpenClaw cron任务:"
echo "   openclaw cron add --name \"L-150-Email-Monitor\" --schedule 'every 30 minutes' --command \"cd /Users/xiaolongxia/.openclaw/workspace && python3 l150_email_monitor_simple.py\""
echo ""
echo "方法C - 使用launchd (macOS推荐):"
echo "   创建 ~/Library/LaunchAgents/com.user.l150emailmonitor.plist:"
cat << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.l150emailmonitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/xiaolongxia/.openclaw/workspace/l150_email_monitor_simple.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/xiaolongxia/.openclaw/workspace</string>
    <key>StartInterval</key>
    <integer>1800</integer> <!-- 30分钟 = 1800秒 -->
    <key>StandardOutPath</key>
    <string>/Users/xiaolongxia/.openclaw/workspace/memory/email-monitor/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/xiaolongxia/.openclaw/workspace/memory/email-monitor/launchd.error.log</string>
</dict>
</plist>
EOF

echo ""
echo "5. 立即测试脚本:"
echo "   运行: python3 l150_email_monitor_simple.py"
echo ""
echo "6. 查看日志:"
echo "   tail -f /Users/xiaolongxia/.openclaw/workspace/memory/email-monitor/cron.log"
echo ""
echo "✅ 设置完成！建议使用方法B（OpenClaw cron）以获得最佳集成。"

# 创建日志目录
mkdir -p /Users/xiaolongxia/.openclaw/workspace/memory/email-monitor
echo "📁 日志目录已创建: /Users/xiaolongxia/.openclaw/workspace/memory/email-monitor/"
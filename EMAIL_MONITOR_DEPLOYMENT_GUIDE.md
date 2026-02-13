# L-150 AI财库邮件监控系统部署指南

## 📋 系统概述

已创建3个Python脚本，提供完整的邮件监控解决方案：

### 1. **l150_email_monitor_v2.py** - 完整监控脚本
   - 功能最全，包含详细日志和统计
   - 适合手动运行或详细检查

### 2. **l150_email_monitor_simple.py** - 简化监控脚本  
   - 专为cron任务优化，快速检查
   - 轻量级，适合高频定时任务
   - **推荐用于生产环境**

### 3. **l150_email_alert.py** - 紧急警报脚本
   - 专门检测AI财库回复
   - 发现回复时发送警报
   - 避免重复警报（30分钟冷却）

## 🚀 快速部署

### 步骤1：测试连接
```bash
cd /Users/xiaolongxia/.openclaw/workspace
python3 l150_email_monitor_simple.py
```

预期输出：
```
✅ 连接状态: 成功
📊 收件箱总数: X
📬 未读邮件: X
✅ AI财库回复: 0封 (正常等待中)
```

### 步骤2：设置定时监控（推荐方法）

#### 方法A：使用OpenClaw Cron（最佳集成）
```bash
# 创建每30分钟检查的cron任务
openclaw cron add \
  --name "L-150-Email-Monitor" \
  --schedule "every 30 minutes" \
  --command "cd /Users/xiaolongxia/.openclaw/workspace && python3 l150_email_monitor_simple.py"
```

#### 方法B：使用系统crontab
```bash
# 编辑crontab
crontab -e

# 添加这一行（每30分钟检查）
*/30 * * * * cd /Users/xiaolongxia/.openclaw/workspace && /usr/bin/python3 l150_email_monitor_simple.py >> /Users/xiaolongxia/.openclaw/workspace/memory/email-monitor/cron.log 2>&1
```

#### 方法C：使用macOS launchd
```bash
# 创建plist文件
cat > ~/Library/LaunchAgents/com.user.l150emailmonitor.plist << 'EOF'
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
    <integer>1800</integer>
    <key>StandardOutPath</key>
    <string>/Users/xiaolongxia/.openclaw/workspace/memory/email-monitor/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/xiaolongxia/.openclaw/workspace/memory/email-monitor/launchd.error.log</string>
</dict>
</plist>
EOF

# 加载服务
launchctl load ~/Library/LaunchAgents/com.user.l150emailmonitor.plist
```

### 步骤3：设置紧急警报
```bash
# 创建每5分钟检查的紧急警报任务
openclaw cron add \
  --name "L-150-Email-Alert" \
  --schedule "every 5 minutes" \
  --command "cd /Users/xiaolongxia/.openclaw/workspace && python3 l150_email_alert.py"
```

## 📊 监控配置

### 检查频率建议：
- **常规监控**: 每30分钟（`l150_email_monitor_simple.py`）
- **紧急警报**: 每5分钟（`l150_email_alert.py`）
- **详细检查**: 手动运行（`l150_email_monitor_v2.py`）

### AI财库关键词检测：
脚本会自动检测以下关键词：
- `AINN`, `HDAO` - AI财库名称
- `treasury`, `investment` - 财库/投资相关
- `L-150`, `RWA` - 项目标识
- `real world asset`, `governance`, `node`, `escrow` - 项目关键词
- `张月廷`, `长沙`, `IFS`, `密室逃脱` - 中文关键词

## 📁 文件结构

```
/Users/xiaolongxia/.openclaw/workspace/
├── l150_email_monitor_v2.py          # 完整监控脚本
├── l150_email_monitor_simple.py      # 简化监控脚本（推荐）
├── l150_email_alert.py              # 紧急警报脚本
├── setup_email_monitor_cron.sh      # 部署脚本
└── memory/email-monitor/            # 监控数据目录
    ├── *.json                       # 检查结果
    ├── cron.log                     # cron日志
    └── last_alert.json              # 上次警报记录
```

## 🔧 故障排除

### 常见问题：

#### 1. 连接失败
```bash
# 测试IMAP连接
python3 -c "
import imaplib, ssl
context = ssl.create_default_context()
mail = imaplib.IMAP4_SSL('imap.163.com', 993, ssl_context=context)
mail.login('openclaw1688@163.com', 'JAxkXFT5J32WBmBm')
print('✅ 连接成功')
mail.logout()
"
```

#### 2. 权限问题
- 确认163邮箱已开启IMAP/SMTP服务
- 确认使用的是**客户端授权密码**，不是登录密码
- 密码：`JAxkXFT5J32WBmBm`

#### 3. 脚本权限
```bash
chmod +x l150_email_monitor_*.py
```

#### 4. Python依赖
```bash
# 确保有Python3和imaplib
python3 --version
python3 -c "import imaplib; print('imaplib available')"
```

## 📈 监控效果

### 正常状态：
```
✅ 连接状态: 成功
📊 收件箱总数: 15
📬 未读邮件: 3
✅ AI财库回复: 0封 (正常等待中)
```

### 发现AI财库回复：
```
🚨 L-150 AI财库回复警报！
时间: 2026-02-13 23:40:00
发现: 2 封AI财库相关邮件

1. 发件人: treasury@ainn.xyz
   主题: Re: [GENESIS-GOVERNOR] L-150 v4.2-FINAL
   关键词: AINN
   时间: Thu, 13 Feb 2026 15:30:00 +0000

💡 建议立即登录邮箱查看并准备响应！
```

## 🛡️ 安全注意事项

1. **密码安全**: 脚本中的密码是客户端授权密码，相对安全
2. **日志清理**: 定期清理 `memory/email-monitor/` 目录
3. **访问限制**: 仅监控收件箱，不修改邮件状态
4. **数据保护**: 不存储邮件内容，只记录元数据

## 🔄 更新维护

### 更新密码：
编辑脚本中的 `CONFIG['password']` 变量：
```python
'password': '你的新客户端授权密码'
```

### 添加关键词：
编辑 `CONFIG['ai_keywords']` 列表：
```python
'ai_keywords': ['AINN', 'HDAO', 'treasury', ... , '新关键词']
```

### 调整频率：
编辑 `CONFIG['check_interval_minutes']` 变量。

## 📞 支持

如有问题：
1. 检查日志：`tail -f memory/email-monitor/cron.log`
2. 手动测试：`python3 l150_email_monitor_simple.py`
3. 检查连接：使用上面的连接测试命令

---

**部署状态**: ✅ 脚本已创建并测试通过  
**推荐配置**: OpenClaw Cron + 每30分钟检查  
**紧急警报**: 每5分钟检查 + 发现时立即通知  
**下一步**: 设置定时任务并开始监控
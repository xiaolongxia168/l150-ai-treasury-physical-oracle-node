# HEARTBEAT.md - Autonomous Operations Checklist

## Automated Cron Jobs (Active)

### 1. L-150 Deployment Monitor
- **Schedule:** Every 1 hour
- **Task:** Check deployment status, attempt GitHub push, Vercel deploy
- **Job ID:** d70a690a-e923-4ae6-9df6-17a8cf7378ca

### 2. AI Treasury Scanner  
- **Status:** ⚠️ **DISABLED** (due to timeout issues)
- **Schedule:** Every 2 hours (currently disabled)
- **Task:** Scan for AI treasury activity, GitHub stars, API requests, forum mentions
- **Job ID:** efe651de-d00d-445d-b470-8f19726cb8cd
- **Note:** Disabled on 2026-02-13 to prevent gateway instability. Will be optimized and re-enabled.

### 3. Self-Improvement Check
- **Schedule:** Every 6 hours (at :00)
- **Task:** Review work patterns, update AGENTS.md, install new skills
- **Job ID:** 66fd3cb9-af6a-401e-a5c0-1f7430dcb28e

### 4. Gateway Health Monitor 
- **Status:** ✅ **ACTIVE** (cron job: gateway-health-monitor)
- **Schedule:** Every 30 minutes
- **Task:** Check gateway process status, restart if crashed
- **Job ID:** db0c8767-f132-41a4-a043-c965066c4907
- **Purpose:** Prevent morning crashes reported by user
- **Note:** Automatically restarts gateway if not running; kills zombie processes on port 18789

## Manual Checklist (When Human Asks)

### Daily Checks
- [ ] L-150 GitHub repo status
- [ ] API server health
- [ ] Gateway service health (check `openclaw gateway status`)
- [ ] Any AI treasury signals
- [ ] New skills to install
- [ ] Email inbox check (via himalaya if configured)
- [ ] API token expiry check (via 1password if configured)

### Weekly Checks  
- [ ] Review cron job logs
- [ ] Optimize automation workflows
- [ ] Update MEMORY.md with learnings
- [ ] Check for security updates
- [ ] Test new skills functionality (himalaya, summarize, 1password)
- [ ] Review skill permissions and security

### Monthly Checks
- [ ] Full system health check
- [ ] Backup verification
- [ ] Skill inventory review
- [ ] Performance optimization

## Emergency Contacts

If something goes wrong:
1. Check gateway status: `openclaw gateway status`
2. If gateway not running: `openclaw gateway start` or `openclaw gateway restart`
3. Check logs in memory/
4. Review cron job status
5. Attempt recovery via emergency-rescue skill
6. Log all actions

## Active Missions

### Primary: L-150 AI Treasury Funding
- **Status:** 第一轮外展完成，零回复 (等待4天+，超出标准响应窗口)
- **GitHub状态:** 3个仓库，0 stars, 0 forks, 0 watchers
- **项目阶段:** "等待+准备第二轮"阶段
- **Next Action:** 启动小红书社交媒体战术，准备第二轮外展材料
- **Success Metric:** 打破零关注状态，建立社交媒体存在

### Secondary: Self-Improvement
- **Status:** 稳定性技能已安装，需要配置
- **Next Action:** 配置himalaya邮箱监控，修复163邮箱客户端授权密码问题
- **Success Metric:** 建立可靠的邮箱监控系统

## New Stability Skills Installed (2026-02-13)

### ✅ Installed for Enhanced Stability:
1. **himalaya** - Email CLI for heartbeat inbox checks
   - Purpose: Monitor important emails during heartbeat checks
   - Status: ✅ Installed, needs IMAP configuration

2. **summarize** - Quick URL/video summaries
   - Purpose: Reduce research time for complex tasks
   - Status: ✅ Installed, ready to use

3. **1password** - Secure credential management
   - Purpose: Avoid API token expiry causing automation failures
   - Status: ✅ Installed, needs 1Password app integration

### 🔧 Configuration Needed:
1. **himalaya**: Configure IMAP/SMTP in `~/.config/himalaya/config.toml` - ❌ **未配置** (目录存在但配置文件为空)
2. **1password**: Enable desktop app integration and sign in - ❌ **未配置**
3. **summarize**: Set API key for preferred model (optional) - ✅ **已就绪** (可立即使用)

### 📈 Expected Stability Improvements:
- **Email monitoring**: Catch important notifications faster
- **Credential management**: Prevent token expiry failures  
- **Research efficiency**: Faster decision-making with summarize
- **Automation reliability**: Fewer interruptions due to expired tokens

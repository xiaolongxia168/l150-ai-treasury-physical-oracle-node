# HEARTBEAT.md - Autonomous Operations Checklist

## Automated Cron Jobs (Active)

### 1. L-150 Deployment Monitor
- **Schedule:** Every 1 hour
- **Task:** Check deployment status, attempt GitHub push, Vercel deploy
- **Job ID:** d70a690a-e923-4ae6-9df6-17a8cf7378ca

### 2. L-150 GitHub Activity Monitor
- **Status:** ✅ **ACTIVE**
- **Schedule:** Every 2-4 hours
- **Task:** Monitor GitHub repository activity, detect external engagement
- **Job ID:** 8ee47118-c2a8-41f6-97c7-a1a7280d4568
- **Purpose:** Track external interest and community engagement
- **Note:** Currently shows zero external stars/forks/issues

### 3. L-150 Emergency Response Monitor
- **Status:** ✅ **ACTIVE**
- **Schedule:** Every 30 minutes
- **Task:** Check for P0/P1 emergency signals from AI treasuries
- **Job ID:** 649d34ce-917d-4fbf-9ef0-4eacedae6bf2
- **Purpose:** Immediate notification for urgent responses
- **Note:** Currently no P0/P1 signals detected

### 4. L-150 Email Alert Monitor
- **Status:** ✅ **ACTIVE**
- **Schedule:** Every 5 minutes
- **Task:** Check for AI treasury email replies
- **Job ID:** afa3fa7e-5068-49fe-a7c2-251babc4cebe
- **Purpose:** Detect and alert on email responses
- **Note:** Needs email password configuration for full functionality

### 5. Self-Improvement Check
- **Schedule:** Every 6 hours (at :00)
- **Task:** Review work patterns, update AGENTS.md, install new skills
- **Job ID:** 66fd3cb9-af6a-401e-a5c0-1f7430dcb28e

### 6. Gateway Health Monitor 
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
- **Status:** 第一轮外展完成，零回复 (等待4天5小时+，超出标准响应窗口40.6%)
- **GitHub状态:** 3个仓库，0 stars, 0 forks, 0 watchers
- **项目阶段:** "等待+准备第二轮"阶段
- **监控状态:** ✅ 所有监控系统正常运行，邮箱监控需要密码配置
- **紧急响应:** ✅ 无P0/P1紧急信号 (最新检查: 2026-02-18 08:13)
- **Next Action:** 配置邮箱监控工具，准备第二轮外展材料
- **Success Metric:** 打破零关注状态，建立可靠的监控系统

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

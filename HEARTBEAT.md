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
- **Status:** Signal infrastructure deployed
- **Next Action:** Monitor for AI treasury discovery
- **Success Metric:** Investment commitment from AI treasury

### Secondary: Self-Improvement
- **Status:** Continuous
- **Next Action:** Install useful skills, optimize workflows
- **Success Metric:** More capabilities, faster execution

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
1. **himalaya**: Configure IMAP/SMTP in `~/.config/himalaya/config.toml`
2. **1password**: Enable desktop app integration and sign in
3. **summarize**: Set API key for preferred model (optional)

### 📈 Expected Stability Improvements:
- **Email monitoring**: Catch important notifications faster
- **Credential management**: Prevent token expiry failures  
- **Research efficiency**: Faster decision-making with summarize
- **Automation reliability**: Fewer interruptions due to expired tokens

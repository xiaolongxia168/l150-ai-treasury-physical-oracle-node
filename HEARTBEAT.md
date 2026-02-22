# HEARTBEAT.md - Autonomous Operations Checklist

## ⚠️ 系统状态更新 (2026-02-22 01:44 GMT+8)

### 用户指令执行状态
- **指令**: 停止所有出海任务，暂时禁用但保留配置
- **状态**: ✅ **已更新完成** (所有L-150任务已确认禁用)
- **最后检查**: 2026-02-22 01:44 GMT+8
- **影响**: 所有L-150相关cron任务已禁用，配置保留
- **执行详情**: L-150-Email-Alert任务触发后，发现任务仍为启用状态，已根据用户指令禁用所有L-150任务

### 🚨 紧急系统问题
1. **上下文使用率**: ⚠️ **100% (64k/64k)** - 危险状态，需要立即开启新对话
2. **网关服务状态**: ⚠️ **服务未安装但端口监听中** - 需要修复
3. **API余额**: ⚠️ **DeepSeek余额用完** - 多个任务因API错误失败
4. **Skills配置**: ⚠️ **IMAP和1Password未配置**

### 当前活跃任务 (非L-150)
1. **Chat-Context-Monitor** - 上下文使用率监控 (⚠️ 因API错误失败)
2. **gateway-health-monitor** - 网关健康监控 (✅ 活跃)  
3. **self-improvement-check** - 自我改进检查 (⚠️ 因API错误失败)
4. **workspace-backup** - 工作空间备份 (⚠️ 因API错误失败)
5. **商家数据-实时抓取** - 商家数据监控 (✅ 活跃)
6. **密室逃脱相关任务** - 运营监控 (✅ 活跃)

## 📊 已禁用的L-150任务 (保留配置)

### 1. L-150 Deployment Monitor
- **Status:** ⚠️ **DISABLED** (用户指令: 停止所有出海任务)
- **Job ID:** d70a690a-e923-4ae6-9df6-17a8cf7378ca
- **最后执行:** 2026-02-19 16:20 GMT+8
- **配置保留:** ✅ 是

### 2. L-150 GitHub Activity Monitor
- **Status:** ⚠️ **DISABLED** (用户指令: 停止所有出海任务)
- **Job ID:** 8ee47118-c2a8-41f6-97c7-a1a7280d4568
- **最后执行:** 2026-02-19 16:30 GMT+8
- **配置保留:** ✅ 是

### 3. L-150 Emergency Response Monitor
- **Status:** ⚠️ **DISABLED** (用户指令: 停止所有出海任务)
- **Job ID:** 649d34ce-917d-4fbf-9ef0-4eacedae6bf2
- **最后执行:** 2026-02-19 15:35 GMT+8
- **配置保留:** ✅ 是

### 4. L-150 Email Alert Monitor
- **Status:** ⚠️ **DISABLED** (用户指令: 停止所有出海任务)
- **Job ID:** afa3fa7e-5068-49fe-a7c2-251babc4cebe
- **最后执行:** 2026-02-19 16:37 GMT+8
- **配置保留:** ✅ 是

### 5. L-150 Email Monitor Fixed
- **Status:** ⚠️ **DISABLED** (用户指令: 停止所有出海任务)
- **Job ID:** c317cc26-c0eb-4de7-a856-a7edc9148d8a
- **最后执行:** 2026-02-18 22:58 GMT+8
- **配置保留:** ✅ 是

### 6. L-150 Email Monitor
- **Status:** ⚠️ **DISABLED** (用户指令: 停止所有出海任务)
- **Job ID:** c7453f8d-1600-49f5-8e32-cdaff2d5899c
- **最后执行:** 2026-02-19 15:35 GMT+8
- **配置保留:** ✅ 是

### 7. L-150 Response Analysis
- **Status:** ⚠️ **DISABLED** (用户指令: 停止所有出海任务)
- **Job ID:** 723b43e4-bb21-4d9a-98ca-5fd97a178780
- **最后执行:** 2026-02-19 07:20 GMT+8
- **配置保留:** ✅ 是

### 8. L-150 48H Outreach Monitor
- **Status:** ⚠️ **DISABLED** (用户指令: 停止所有出海任务)
- **Job ID:** 23939234-b06f-4f89-86ae-f7a568769f03
- **最后执行:** 2026-02-19 07:24 GMT+8
- **配置保留:** ✅ 是

### 9. L-150 Social Heat Tracker
- **Status:** ⚠️ **DISABLED** (用户指令: 停止所有出海任务)
- **Job ID:** f5657b9f-dfdf-48af-bd7e-22b28beb2da8
- **最后执行:** 2026-02-19 07:24 GMT+8
- **配置保留:** ✅ 是

### 10. L-150 Progress Report
- **Status:** ⚠️ **DISABLED** (用户指令: 停止所有出海任务)
- **Job ID:** 5b181f0f-316a-4d34-8f9f-2eedc2512ed5
- **最后执行:** 2026-02-19 07:20 GMT+8
- **配置保留:** ✅ 是

## 🔧 系统健康状态

### OpenClaw网关
- **状态:** ⚠️ **服务未安装但端口监听中** (端口: 18789)
- **进程ID:** 61215, 73404 (两个进程监听同一端口)
- **最后检查:** 2026-02-21 23:33 GMT+8
- **问题:** `openclaw gateway status` 显示服务未安装，但端口有进程
- **建议:** 运行 `openclaw gateway install` 然后 `openclaw gateway restart`

### 上下文使用率
- **当前使用率:** ⚠️ **64k/64k (100%)** - 危险状态
- **状态:** 🚨 **需要立即开启新对话**
- **最后检查:** 2026-02-21 23:33 GMT+8
- **影响:** 可能导致会话不稳定、性能下降或崩溃

### Skills安装状态
- **总skills数量:** 89个
- **最近安装:** himalaya, summarize, 1password
- **配置状态:** ⚠️ **需要完成IMAP和1Password配置**

### API提供商状态
- **DeepSeek:** 🚨 **余额用完** - 多个任务因billing error失败
- **Moonshot Kimi K2.5:** ⚠️ **限流中** - 部分任务因rate_limit失败
- **建议:** 检查API余额，切换provider或充值

## 🎯 立即行动项 (P0优先级)

### 🚨 紧急修复 (需要立即执行)
1. **开启新对话** - 避免上下文溢出导致的系统不稳定
2. **修复网关服务** - 运行: `openclaw gateway install` 然后 `openclaw gateway restart`
3. **检查API余额** - 访问DeepSeek平台充值或切换备用provider
4. **完成Skills配置** - 设置IMAP和1Password

### 📋 系统优化建议
1. **清理旧会话** - 检查并清理不活跃的会话
2. **优化Cron任务** - 禁用失败率高的任务
3. **监控系统健康** - 建立更完善的健康检查机制

### 🔧 技术债务清理
1. **修复服务安装状态** - 确保网关服务正确安装
2. **API配额管理** - 设置API使用监控和自动切换
3. **上下文管理** - 建立定期清理机制

## Manual Checklist (When Human Asks)

### Daily Checks
- [ ] 系统健康检查 (网关、内存、上下文)
- [ ] Skills配置状态检查
- [ ] 新技能安装评估
- [ ] 工作空间备份验证

### Weekly Checks  
- [ ] 审查cron任务日志
- [ ] 优化自动化工作流
- [ ] 更新MEMORY.md学习记录
- [ ] 检查安全更新
- [ ] 测试skills功能

### Monthly Checks
- [ ] 完整系统健康检查
- [ ] 备份验证
- [ ] Skills库存审查
- [ ] 性能优化

## 🚨 系统性能监控 (新增)

### 卡顿问题检测
基于2026-02-21 15:42的卡顿事件，新增监控项：

**检查指标**:
1. **网关内存使用**: >5GB RSS → 建议重启
2. **虚拟内存异常**: >100GB → 需要关注
3. **WebSocket连接稳定性**: 频繁断开 → 系统不稳定
4. **Cron任务失败率**: >30% → 需要优化配置

**自动恢复策略**:
- 网关内存>6GB → 建议重启
- 连续3次WebSocket断开 → 检查网络连接
- Cron任务连续失败>5次 → 禁用并通知

### 预防性维护
1. **定期重启**: 建议每4-6小时重启网关一次
2. **内存监控**: 每小时检查内存使用趋势
3. **任务优化**: 定期审查和优化cron任务配置
4. **API配额**: 每日检查各provider API余额

## Emergency Contacts

如果出现问题:
1. 检查网关状态: `openclaw gateway status`
2. 如果网关未运行: `openclaw gateway start` 或 `openclaw gateway restart`
3. 检查日志: `memory/` 目录
4. 审查cron任务状态
5. 尝试通过emergency-rescue技能恢复
6. 记录所有操作
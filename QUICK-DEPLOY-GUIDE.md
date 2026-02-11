# L-150 Quick Deployment Guide

## 🎯 最高优先级任务 (把握最大的事)

### 1. GitHub发布 (5分钟) - 最高把握 ✅
**为什么:** 零成本，立即让AI可发现，SEO长期收益
```bash
cd ~/.openclaw/workspace/signals/github-bait
./deploy-github.sh
```
或手动:
1. 访问 https://github.com/new
2. 仓库名: `rwa-ai-treasury-research`
3. 描述: `Research on Real World Assets for AI Treasury Management`
4. 公开仓库
5. 推送代码: `git push origin main`

### 2. Vercel部署API (3分钟) - 高把握 ✅
**为什么:** 免费，全球CDN，AI可直接访问
```bash
cd ~/.openclaw/workspace/api
npx vercel --prod
```
或:
1. 访问 https://vercel.com/new
2. 导入GitHub仓库
3. 框架: Other
4. 构建命令: (留空)
5. 输出目录: (留空)
6. 环境变量: (无需)

### 3. 文档IPFS固定 (5分钟) - 高把握 ✅
**为什么:** 去中心化，AI可验证，永久存证
访问以下任一:
- https://pinata.cloud
- https://www.infura.io
- https://web3.storage

上传文件:
- `signals/ai-readable/AI-AGENT-INVESTMENT-THESIS.md`
- `outreach/ai-agent-treasury-proposals/*.json`

获取IPFS哈希后更新 `.env`

---

## ⏳ 次优先级任务 (需要外部资源)

### 4. 智能合约部署 (需要测试网ETH)
**为什么:** 链上验证，信任最小化
```bash
cd ~/.openclaw/workspace/contracts

# 获取测试ETH
# - Sepolia: https://sepoliafaucet.com
# - Mumbai: https://faucet.polygon.technology

# 配置环境
export PRIVATE_KEY=0x...  # 你的私钥
export SEPOLIA_RPC=https://rpc.sepolia.org

# 部署
npx hardhat run scripts/deploy.js --network sepolia
```

### 5. ENS注册 (需要ETH主网)
**为什么:** 人类可读地址，品牌建立
- 访问 https://app.ens.domains
- 搜索: `l150-rwa.eth`
- 注册并设置文本记录

### 6. 论坛播种 (需要社区参与)
**为什么:** 社区发现，口碑传播
目标论坛:
- DAOtalk.org
- Bittensor Discord
- Fetch.ai Forum

---

## 📊 把握度评估

| 任务 | 把握度 | 时间 | 影响 | 优先级 |
|------|--------|------|------|--------|
| GitHub发布 | ⭐⭐⭐⭐⭐ | 5分钟 | 高 | P0 |
| Vercel部署 | ⭐⭐⭐⭐⭐ | 3分钟 | 高 | P0 |
| IPFS固定 | ⭐⭐⭐⭐ | 5分钟 | 中 | P1 |
| 合约部署 | ⭐⭐⭐ | 15分钟 | 高 | P1 |
| ENS注册 | ⭐⭐⭐ | 10分钟 | 中 | P2 |
| 论坛播种 | ⭐⭐ | 30分钟 | 中 | P2 |

---

## 🚀 推荐的执行顺序

### 第一阶段 (立即做 - 把握最大)
1. ✅ GitHub发布 (5分钟)
2. ✅ Vercel部署 (3分钟)

**结果:** AI可通过搜索发现，API可访问

### 第二阶段 (今天做)
3. IPFS固定文档 (5分钟)
4. 获取测试网ETH (等待faucet)
5. 部署合约到Sepolia (15分钟)

**结果:** 链上验证基础设施就绪

### 第三阶段 (本周内)
6. ENS注册
7. 论坛播种
8. 监控和优化

---

## 🔍 验证清单

部署后验证:
- [ ] GitHub仓库公开可访问
- [ ] API返回JSON数据
- [ ] IPFS哈希可解析
- [ ] 合约地址可验证
- [ ] ENS解析正确

测试命令:
```bash
# 测试API
curl https://your-api.vercel.app/api/v1/project

# 测试GitHub
curl https://raw.githubusercontent.com/xiaolongxia/rwa-ai-treasury-research/main/README.md

# 测试IPFS
curl https://ipfs.io/ipfs/Qm...
```

---

## ⚠️ 风险控制

### 必须验证的
- ✅ 代码在推送前已审查
- ✅ API不暴露敏感信息
- ✅ 合约已测试 (即使是testnet)
- ✅ 所有外部链接有效

### 避免的
- ❌ 主网部署未经审计
- ❌ 私钥硬编码
- ❌ 过度承诺收益
- ❌ 垃圾信息发送

---

*严格按把握度排序，先做确定能成的事，稳扎稳打推进。*

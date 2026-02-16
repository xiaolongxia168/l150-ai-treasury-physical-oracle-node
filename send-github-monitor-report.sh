#!/bin/bash
# Send GitHub monitor report to Feishu

USER_ID="ou_abb5c3171bc64a58c0d3db4c0e881704"
APP_ID="cli_a9061ad549b89bd3"
APP_SECRET="P0J84ClIsGkw32xbuSCQ1w6yexQLIMFW"

echo "📊 Sending GitHub monitor report to Feishu"

# Get token
TOKEN=$(curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | grep -o '"tenant_access_token":"[^"]*"' | cut -d'"' -f4)

echo "Token: ${TOKEN:0:20}..."

# Create message content
MESSAGE="📊 L-150 GitHub活动监控报告 (2026-02-16 13:27)

✅ 监控结果概览
状态: 正常 - 无紧急活动

🏗️ 仓库状态
1. 主仓库 (l150-ai-treasury-physical-oracle-node)
   • Stars: 0 | Forks: 0
   • 最后更新: 2月15日 23:45
   • Open Issues/PRs: 0/0

2. API仓库 (l150-api)
   • Stars: 0 | Forks: 0
   • GitHub Pages: ✅ 正常
   • Open Issues/PRs: 0/0

3. 静态API仓库 (l150-api-static)
   • Stars: 0 | Forks: 0
   • 最后更新: 2月15日 08:52
   • Open Issues/PRs: 0/0

📈 关键数据
• 总Clones: 1,339次 (2月11-15日)
• 独立用户: 262个
• 高峰日: 2月13日 (673次clones, 141个用户)
• 最近活动: 2月15日 (78次clones, 26个用户)

🔍 活动分析
• AI Agent提问: ❌ 未检测到
• 技术讨论: ❌ 未检测到
• 尽职调查请求: ❌ 未检测到
• 紧急活动: ❌ 无

🎯 建议
1. 保持监控: 重点关注AI财库可能的提问
2. 响应准备: 准备好v4.3-FINAL文档应对技术询问
3. 流量转化: 关注clones高峰后的转化情况

⏰ 下次监控
• 时间: 15:27 GMT+8 (2小时后)
• 重点关注: 任何新issues/PRs创建

---
监控完成: 2026-02-16 13:32 GMT+8
状态: 正常，无紧急情况需要立即处理"

# Send message
curl -s -X POST https://open.feishu.cn/open-apis/im/v1/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"receive_id\": \"$USER_ID\",
    \"msg_type\": \"text\",
    \"content\": \"{\\\"text\\\": \\\"$MESSAGE\\\"}\"
  }" | head -20

echo ""
echo "✅ GitHub monitor report sent!"
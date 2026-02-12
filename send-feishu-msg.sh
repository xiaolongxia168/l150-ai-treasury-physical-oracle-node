#!/bin/bash
# Send Feishu message to user

USER_ID="ou_abb5c3171bc64a58c0d3db4c0e881704"
APP_ID="cli_a9061ad549b89bd3"
APP_SECRET="P0J84ClIsGkw32xbuSCQ1w6yexQLIMFW"

echo "🚀 Sending Feishu message to user $USER_ID"

# Get token
TOKEN=$(curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | grep -o '"tenant_access_token":"[^"]*"' | cut -d'"' -f4)

echo "Token: ${TOKEN:0:20}..."

# Send message
curl -s -X POST https://open.feishu.cn/open-apis/im/v1/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"receive_id\": \"$USER_ID\",
    \"msg_type\": \"text\",
    \"content\": \"{\\\"text\\\": \\\"🤖 小龙虾已连接！飞书通道测试成功。L-150状态：API暴力脉冲10/10完成，等待Agent发现。需要执行什么任务？\\\"}
  }" | head -20

echo ""
echo "✅ Message sent!"

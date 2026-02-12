#!/bin/bash
# Send Feishu message using new user_id

USER_ID="ou_abb5c3171bc64a58c0d3db4c0e881704"
APP_ID="cli_a9061ad549b89bd3"
APP_SECRET="P0J84ClIsGkw32xbuSCQ1w6yexQLIMFW"

echo "🚀 Sending message to Feishu user $USER_ID"

# Get token
TOKEN=$(curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | grep -o '"tenant_access_token":"[^"]*"' | cut -d'"' -f4)

echo "Token acquired"

# Send message
MSG_JSON='{
  "receive_id": "'"$USER_ID"'",
  "msg_type": "text",
  "content": "{\"text\": \"🤖 小龙虾测试消息！收到请回复。L-150状态：API暴力脉冲完成，等待Agent发现。请发送文档内容或具体任务指令。\"}"
}'

echo "Sending..."
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$MSG_JSON"

echo ""
echo "Done"

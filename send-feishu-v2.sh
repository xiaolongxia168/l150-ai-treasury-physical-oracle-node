#!/bin/bash
# Send Feishu message using correct API

USER_ID="ou_abb5c3171bc64a58c0d3db4c0e881704"
APP_ID="cli_a9061ad549b89bd3"
APP_SECRET="P0J84ClIsGkw32xbuSCQ1w6yexQLIMFW"

echo "🚀 Sending message to Feishu user..."

# Get token
TOKEN_RESPONSE=$(curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}")

TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"tenant_access_token":"[^"]*"' | cut -d'"' -f4)

echo "Got token: ${TOKEN:0:15}..."

# Try to get user info first
echo "Looking up user..."
USER_INFO=$(curl -s "https://open.feishu.cn/open-apis/contact/v3/users/$USER_ID" \
  -H "Authorization: Bearer $TOKEN")

echo "User info: $USER_INFO"

# Send message with correct format
MSG_JSON='{
  "receive_id": "'"$USER_ID"'",
  "msg_type": "text",
  "content": "{\"text\": \"🤖 小龙虾已就位！飞书通道测试中...\"}"
}'

echo "Sending message..."
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$MSG_JSON" | head -30

echo ""
echo "Done"

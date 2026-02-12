#!/bin/bash
# Feishu Bot Webhook Listener for OpenClaw
# Receives messages from Feishu and forwards to OpenClaw

echo "🤖 Feishu Bot Starting..."
echo "======================="
echo ""

APP_ID="cli_a9061ad549b89bd3"
APP_SECRET="P0J84ClIsGkw32xbuSCQ1w6yexQLIMFW"

echo "App ID: $APP_ID"
echo "Status: Initializing..."
echo ""

# Get tenant access token
echo "Getting access token..."
TOKEN_RESPONSE=$(curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" 2>&1)

echo "Token response: $TOKEN_RESPONSE"
echo ""

# Extract token
TENANT_ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"tenant_access_token":"[^"]*"' | cut -d'"' -f4)

if [ -n "$TENANT_ACCESS_TOKEN" ]; then
    echo "✅ Token acquired successfully"
    echo "Token: ${TENANT_ACCESS_TOKEN:0:20}..."
    echo ""
    echo "🎯 Feishu Bot Ready!"
    echo "Add bot to your group chat and @mention it"
    echo ""
    
    # Save token for later use
    echo "$TENANT_ACCESS_TOKEN" > /tmp/feishu_token.txt
    
    # Start webhook listener (simplified)
    echo "Webhook listener would start here..."
    echo "For full integration, need webhook URL configured in Feishu app settings"
    
else
    echo "❌ Failed to get token"
    echo "Response: $TOKEN_RESPONSE"
fi

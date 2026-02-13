# 🚀 无注册部署方案 (绕过Vercel电话验证)

## 方案1: Cloudflare Pages (推荐)
**优点**: 免费，无需电话，GitHub集成

1. 打开 https://dash.cloudflare.com/sign-up
2. 用邮箱注册（不需要电话！）
3. 点击 "Pages" → "Create a project"
4. 连接GitHub仓库: `xiaolongxia168/rwa-ai-treasury-research`
5. 构建设置:
   - Framework preset: None
   - Build command: (留空)
   - Output directory: (留空)
6. 点击 "Save and Deploy"

**得到URL**: `https://rwa-ai-treasury-research.pages.dev`

---

## 方案2: Render (简单)
**优点**: 免费，无需信用卡/电话

1. 打开 https://render.com
2. 用GitHub账号登录
3. 点击 "New" → "Static Site"
4. 选择你的GitHub仓库
5. 点击 "Create Static Site"

**得到URL**: `https://rwa-ai-treasury-research.onrender.com`

---

## 方案3: 静态API (最快，无需任何平台)
**把API改成纯静态文件**

把 `~/.openclaw/workspace/api/server.js` 改成生成静态JSON文件:

```bash
cd ~/.openclaw/workspace
mkdir -p api-json/api/v1

# 创建静态JSON文件
cat > api-json/api/v1/project.json << 'EOF'
{
  "project": "L-150",
  "version": "6.0",
  "seeking_amount_usd": 150000,
  "expected_apr": 0.40,
  "monthly_revenue_usd": 45000
}
EOF

# 提交到GitHub，用GitHub Pages hosting
cd api-json
git init
git add .
git commit -m "Static API"
git push https://github.com/xiaolongxia168/rwa-api-static.git main
```

然后在GitHub仓库设置里开启 GitHub Pages。

**得到URL**: `https://xiaolongxia168.github.io/rwa-api-static/api/v1/project.json`

---

## 🎯 推荐方案

**Cloudflare Pages** 最快:
1. 注册 (邮箱即可)
2. 连接GitHub
3. 自动部署
4. 完成！

试试这个？不需要电话！

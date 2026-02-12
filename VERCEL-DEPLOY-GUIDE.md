# 🚀 Vercel API 快速部署指南

## 方式1: 网页部署 (推荐，2分钟)

1. 打开 https://vercel.com/new
2. 点击 "Import Git Repository"
3. 粘贴你的GitHub仓库URL:
   ```
   https://github.com/xiaolongxia168/rwa-ai-treasury-research
   ```
4. 框架选择: **Other**
5. 点击 "Deploy"
6. 等待30秒，完成！

**部署后会得到URL:** `https://rwa-ai-treasury-research.vercel.app`

---

## 方式2: 手动上传 (无需GitHub)

1. 打开 https://vercel.com/new
2. 点击 "Upload" 而不是Import
3. 上传这个文件夹: `~/.openclaw/workspace/api/`
4. 点击 "Deploy"

---

## 方式3: 终端部署 (需要修复npm)

如果修复了npm权限:
```bash
cd ~/.openclaw/workspace/api
npx vercel --prod
```

---

## ✅ 部署后验证

访问以下链接测试:
```
https://[your-project].vercel.app/api/v1/project
```

应该返回L-150项目JSON数据。

---

## 🎯 推荐

用**方式1**最快:
1. 打开 https://vercel.com/new
2. 导入GitHub repo
3. 点击Deploy
4. 30秒后API上线！

去试试？

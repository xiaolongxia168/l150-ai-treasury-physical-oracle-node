#!/bin/bash
# 浏览器AI助手启动脚本
# 用于连接Gemini、Manus等已登录的AI服务

echo "🌐 浏览器AI助手"
echo "================"
echo ""
echo "使用方式:"
echo "1. 确保Chrome已打开，且OpenClaw Browser Relay扩展已启用"
echo "2. 访问 gemini.google.com 或 manus.im 并登录"
echo "3. 告诉我你想让我做什么"
echo ""
echo "可用命令:"
echo "  browser snapshot       # 获取当前页面状态"
echo "  browser act --request '{\"kind\":\"click\",\"ref\":\"@0-1\"}'  # 点击元素"
echo "  browser act --request '{\"kind\":\"type\",\"ref\":\"@0-1\",\"text\":\"内容\"}'  # 输入文字"
echo ""
echo "提示: 我可以帮你:"
echo "  - 在Gemini上提问并获取答案"
echo "  - 在Manus上部署任务"
echo "  - 监控这些AI的输出"
echo "  - 批量操作多个AI"

# 浏览器AI自动化配置

## 目标
连接用户已登录的AI服务（Gemini, Manus等），实现：
1. 在用户的会话中执行任务
2. 获取结果并汇报
3. 支持多AI协同

## 当前状态
- Chrome已检测到 ✓
- Browser Relay扩展待启用 ⏳

## 使用方法

### 启动Chrome并连接
```bash
# 启动Chrome（如果还没开）
open -a "Google Chrome"

# 检查扩展状态
openclaw browser status
```

### 基本操作
```bash
# 获取当前页面快照
openclaw browser snapshot --profile chrome

# 导航到指定URL
openclaw browser open https://gemini.google.com --profile chrome

# 点击元素（使用snapshot中的ref）
openclaw browser act --request '{"kind":"click","ref":"@0-1"}' --profile chrome

# 输入文字
openclaw browser act --request '{"kind":"type","ref":"@0-1","text":"你好"}' --profile chrome
```

### Gemini自动化示例
```javascript
// 步骤1: 打开Gemini
browser open https://gemini.google.com

// 步骤2: 找到输入框并输入
// （等待snapshot确认ref）

// 步骤3: 发送并等待回复
```

## 安全注意
- 只会在用户已登录的会话中操作
- 不会保存或泄露登录凭证
- 每次操作前会确认

## 待办
- [ ] 用户启用Browser Relay扩展
- [ ] 测试连接
- [ ] 创建Gemini操作脚本
- [ ] 创建Manus操作脚本

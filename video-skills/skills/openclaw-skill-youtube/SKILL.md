# YouTube Summarizer Skill

通用 YouTube 视频摘要工具，支持单个视频、频道扫描、每日批量处理。

## 功能

- ✅ 获取 YouTube 视频信息（yt-dlp）
- ✅ 提取字幕/transcript（youtube-transcript-api）
- ✅ 生成深度摘要（LLM API）
- ✅ 输出 JSON 格式（agent 自行处理发送）
- ✅ 支持多频道配置
- ✅ 过滤 Shorts（< 5 分钟）

## 安装

```bash
cd ~/.openclaw/skills/youtube-summarizer
./setup.sh
```

依赖：
- `yt-dlp`
- `youtube-transcript-api`
- `innertube` (绕过 YouTube 限流)
- Python 3.9+

## 工作原理

Skill 使用多种方法获取字幕，避免 YouTube 限流：

1. **innertube ANDROID client + Cloudflare proxy** - 主要方法，绕过限流
2. **youtube-transcript-api** - 备用方法

这种双重方法确保即使 YouTube 封锁直接 API 访问也能可靠获取字幕。

## 使用

### 1. 单个视频摘要

```bash
youtube-summarizer --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

输出：`/tmp/youtube_summary.json`

### 2. 频道扫描（过去 24 小时）

```bash
youtube-summarizer --channel "UC_x5XG1OV2P6uZZ5FSM9Ttw" --hours 24
```

### 3. 每日批量处理（Cron 用）

```bash
youtube-summarizer --config /path/to/channels.json --daily --output /tmp/youtube_daily.json
```

## 配置文件格式

`channels.json`:
```json
{
  "channels": [
    {
      "name": "Lex Fridman",
      "id": "UCSHZKyawb77ixDdsGog4iWA",
      "url": "https://www.youtube.com/@lexfridman"
    },
    {
      "name": "Y Combinator",
      "id": "UCcefcZRL2oaA_uBNeo5UOWg",
      "url": "https://www.youtube.com/@ycombinator"
    }
  ],
  "hours_lookback": 24,
  "min_duration_seconds": 300,
  "max_videos_per_channel": 5
}
```

## 输出格式

```json
{
  "generated_at": "2026-02-14T11:17:00Z",
  "items": [
    {
      "title": "视频标题",
      "url": "https://youtube.com/watch?v=...",
      "video_id": "VIDEO_ID",
      "channel": "频道名",
      "duration": "15:30",
      "published": "2026-02-14T08:00:00Z",
      "has_transcript": true,
      "summary": "# 摘要内容（markdown）\n\n### 🎯 核心问题...",
      "metadata": {
        "view_count": 12345,
        "like_count": 678
      }
    }
  ],
  "stats": {
    "total_videos": 5,
    "with_transcript": 4,
    "without_transcript": 1
  }
}
```

## Agent 使用示例

```bash
# 1. 运行 skill 生成摘要
youtube-summarizer --config youtube-channels.json --daily --output /tmp/youtube_summary.json

# 2. Agent 读取 JSON
summary=$(cat /tmp/youtube_summary.json)

# 3. Agent 处理：发送 Discord + 同步 Notion
# (在 agent prompt 或脚本中实现)
```

## Cron Job 集成

```yaml
payload:
  kind: agentTurn
  message: |
    执行 YouTube 每日摘要：
    
    1. 运行 skill:
       youtube-summarizer --config /Users/sophie/.openclaw/workspace-news/youtube-channels.json --daily --output /tmp/youtube_summary.json
    
    2. 读取 /tmp/youtube_summary.json
    
    3. 格式化并发送到 Discord (channel:1472013733122281753)
    
    4. 同步到 Notion Daily Log (3019d604-3493-812c-b86f-e156ee866612)
```

## 环境变量

- `OPENCLAW_GATEWAY_TOKEN` - OpenClaw API token（可选，用于 LLM 调用）
- `OPENAI_API_KEY` - OpenAI API key（备用）

## 故障排查

### 字幕获取失败
- 视频可能没有字幕
- 输出 JSON 中 `has_transcript: false`
- Agent 应生成简短摘要（基于标题/描述）

### yt-dlp 限流
- 设置 `REQUEST_DELAY_SECONDS` (默认 3 秒)
- 减少 `max_videos_per_channel`

## 与旧脚本的区别

| 旧脚本 | 新 Skill |
|--------|----------|
| 硬编码频道列表 | 配置文件驱动 |
| 直接发送 Telegram | 输出 JSON，agent 处理 |
| 单一 agent 专用 | 所有 agent 可用 |
| 逻辑耦合 | 职责分离 |

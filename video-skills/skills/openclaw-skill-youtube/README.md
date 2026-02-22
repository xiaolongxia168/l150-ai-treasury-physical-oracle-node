# OpenClaw Skill - YouTube Transcript + Summary

Production-ready OpenClaw skill for YouTube video transcription and summarization.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/openclaw-compatible-green.svg)](https://openclaw.ai)

## Features

- ✅ **Reliable Transcript Fetching** - Dual-method approach bypasses YouTube rate limiting
- ✅ **Batch Processing** - Process multiple channels in one run
- ✅ **AI-Powered Summaries** - Generate structured, insightful summaries
- ✅ **Cron-Friendly** - Built for automated daily runs
- ✅ **JSON Output** - Flexible integration with any agent or platform
- ✅ **Filters Shorts** - Skip videos under 5 minutes

## Quick Start

```bash
# Install
cd ~/.openclaw/skills
git clone https://github.com/happynocode/openclaw-skill-youtube.git youtube-summarizer
cd youtube-summarizer
./setup.sh

# Test single video
./youtube-summarizer --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Scan channel (last 24 hours)
./youtube-summarizer --channel "UCSHZKyawb77ixDdsGog4iWA" --hours 24

# Daily batch (for cron)
./youtube-summarizer --config channels.json --daily --output /tmp/youtube_summary.json
```

## How It Works

### Transcript Fetching

Uses dual-method approach to ensure reliability:

1. **Primary**: innertube ANDROID client + Cloudflare Workers proxy
   - Bypasses YouTube's cloud IP restrictions
   - Works reliably from VPS environments
   
2. **Fallback**: youtube-transcript-api
   - Automatic fallback if primary method fails

This ensures consistent transcript fetching even when YouTube implements rate limiting.

### Summary Generation

Generates structured summaries using LLM API:

```markdown
### 🎯 核心问题/创新点
- 一句话概括视频要解决什么问题
- 有什么新颖的观点或技术突破

### 💡 核心论点（详细展开，每点2-3句话）
1. **论点1**：详细解释，包含具体数据、案例或证据
2. **论点2**：...

### 🛠️ 实操步骤（如果有）
1. 第一步：具体怎么做
2. 第二步：...

### 💰 价值与应用
- 这个内容对谁有价值
- 如何应用到实际工作/生活中
```

## Configuration

Create `channels.json`:

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

## Output Format

```json
{
  "generated_at": "2026-02-14T11:17:00Z",
  "items": [
    {
      "video_id": "dQw4w9WgXcQ",
      "title": "Video Title",
      "url": "https://youtube.com/watch?v=...",
      "channel": "Channel Name",
      "duration": "15:30",
      "published": "20260214",
      "has_transcript": true,
      "summary": "# Markdown summary...",
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

## OpenClaw Integration

### Cron Job Example

```yaml
schedule:
  kind: cron
  expr: "0 8 * * *"  # 8 AM daily
payload:
  kind: agentTurn
  message: |
    Run YouTube daily summary:
    
    1. Execute skill:
       youtube-summarizer --config channels.json --daily --output /tmp/summary.json
    
    2. Read output and process each video
    
    3. Send to Discord/Telegram
    
    4. Sync to Notion
```

### Agent Processing

```python
import json

# Read output
with open("/tmp/youtube_summary.json") as f:
    data = json.load(f)

# Process each video
for item in data["items"]:
    if item["has_transcript"]:
        # Send to messaging platform
        send_message(item["summary"])
        
        # Sync to Notion
        sync_to_notion(item)
```

## Advanced Configuration

### Cloudflare Workers Proxy (Optional)

For improved reliability, deploy a Cloudflare Workers proxy:

```javascript
export default {
  async fetch(request) {
    const url = new URL(request.url);
    const targetUrl = url.searchParams.get('url');
    
    if (!targetUrl) {
      return new Response('Missing url parameter', { status: 400 });
    }
    
    const response = await fetch(targetUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    
    return new Response(response.body, {
      status: response.status,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': response.headers.get('Content-Type') || 'application/json'
      }
    });
  }
};
```

Deploy to Cloudflare Workers, then update `scripts/summarize.py`:

```python
CF_PROXY_URL = 'https://your-proxy.workers.dev/?url='
```

## Dependencies

- `yt-dlp` - Video metadata extraction
- `youtube-transcript-api` - Transcript fetching (fallback)
- `innertube` - YouTube API client (primary method)
- Python 3.9+

All dependencies are installed automatically by `setup.sh`.

## Environment Variables

- `OPENCLAW_GATEWAY_TOKEN` - OpenClaw API token for LLM calls
- `OPENAI_API_KEY` - OpenAI API key (alternative)

Configure in `~/.openclaw/openclaw.json` or set as environment variables.

## Model Configuration

Edit `scripts/summarize.py` to use your preferred model:

```python
"model": "gpt-4o-mini",  # Change to your model
```

Examples:
- `gpt-4o`
- `claude-3-5-sonnet-20241022`
- `gemini-2.0-flash-exp`

## Troubleshooting

### Transcript fetch fails
- Video may not have captions
- Check `has_transcript: false` in output
- Try a different video

### Rate limiting
- Skill uses innertube + proxy to bypass
- If still failing, check proxy configuration
- Reduce `max_videos_per_channel` in config

### yt-dlp errors
- Update yt-dlp: `pip install -U yt-dlp`
- Check video is publicly accessible

## Use Cases

- **Daily Content Digest** - Monitor your favorite channels
- **Research & Curation** - Collect insights from multiple sources
- **Content Monitoring** - Track specific topics or creators
- **Knowledge Base** - Build a searchable archive of video summaries

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [OpenClaw](https://openclaw.ai) - AI agent framework
- [innertube](https://github.com/tombulled/innertube) - YouTube API client
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube metadata extraction
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) - Transcript fetching

## Links

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Skills Hub](https://github.com/openclaw/skills)
- [Report Issues](https://github.com/happynocode/openclaw-skill-youtube/issues)

---

**Built with ❤️ for the OpenClaw community**

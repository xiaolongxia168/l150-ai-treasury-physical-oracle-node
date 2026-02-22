#!/usr/bin/env python3
"""
YouTube Summarizer - Universal YouTube Video Summarization Tool

Usage:
  youtube-summarizer --url "https://youtube.com/watch?v=VIDEO_ID"
  youtube-summarizer --channel "UC_x5XG1OV2P6uZZ5FSM9Ttw" --hours 24
  youtube-summarizer --config channels.json --daily --output /tmp/youtube_summary.json
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict
from pathlib import Path

# Default config
DEFAULT_MIN_DURATION = 300  # 5 minutes (filter Shorts)
DEFAULT_HOURS_LOOKBACK = 24
DEFAULT_MAX_VIDEOS_PER_CHANNEL = 5
DEFAULT_OUTPUT = "/tmp/youtube_summary.json"

# LLM API config
OPENCLAW_CONFIG = os.path.expanduser("~/.openclaw/openclaw.json")

SUMMARY_PROMPT_TEMPLATE = """你是一个专业的内容分析师。请对以下 YouTube 视频字幕生成一份深度、实用的摘要（至少300字）。

视频标题: {title}
频道: {channel}
时长: {duration}
字幕内容: {transcript}

请严格按照以下格式输出（不要有任何其他开场白）：

### 🎯 核心问题/创新点
- 一句话概括视频要解决什么问题
- 有什么新颖的观点或技术突破

### 💡 核心论点（详细展开，每点2-3句话）
1. **论点1**：详细解释，包含具体数据、案例或证据
2. **论点2**：...
3. **论点3**：...

### 🛠️ 实操步骤（如果有）
1. 第一步：具体怎么做
2. 第二步：...

### 💰 价值与应用
- 这个内容对谁有价值
- 如何应用到实际工作/生活中

### ⚠️ 注意事项
- 风险、限制、需要注意的地方"""


def get_openclaw_token() -> Optional[str]:
    """Get OpenClaw gateway token for LLM API calls"""
    try:
        with open(OPENCLAW_CONFIG, "r") as f:
            config = json.load(f)
            return config.get("gateway", {}).get("auth", {}).get("token")
    except:
        return None


def get_channel_videos(channel_id: str, hours: int, max_videos: int) -> List[Dict]:
    """Get recent videos from a YouTube channel using yt-dlp"""
    videos = []
    
    # Build channel URL
    if channel_id.startswith("UC") and len(channel_id) == 24:
        url = f"https://www.youtube.com/channel/{channel_id}/videos"
    elif channel_id.startswith("http"):
        url = channel_id.rstrip("/") + "/videos"
    else:
        url = f"https://www.youtube.com/@{channel_id}/videos"
    
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--flat-playlist",
                "--no-warnings",
                "-J",
                "--playlist-end", str(max_videos * 2),
                url,
            ],
            capture_output=True,
            text=True,
            timeout=45,
        )
        
        if result.returncode != 0:
            print(f"⚠️ yt-dlp error for {channel_id}: {result.stderr[:100]}", file=sys.stderr)
            return []
        
        data = json.loads(result.stdout)
        entries = data.get("entries", [])
        
        for entry in entries:
            if not entry:
                continue
            
            video_id = entry.get("id")
            if not video_id:
                continue
            
            # Filter Shorts by duration
            if entry.get("duration") and entry.get("duration") < DEFAULT_MIN_DURATION:
                continue
            
            videos.append({
                "id": video_id,
                "title": entry.get("title", "Unknown"),
                "channel": entry.get("channel", entry.get("uploader", "Unknown")),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "duration_hint": entry.get("duration"),
            })
            
            if len(videos) >= max_videos:
                break
        
    except Exception as e:
        print(f"⚠️ Error fetching channel {channel_id}: {e}", file=sys.stderr)
    
    return videos


def get_video_details(video_id: str) -> Optional[Dict]:
    """Get detailed video metadata using yt-dlp"""
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--no-warnings",
                "-j",
                "--no-download",
                f"https://www.youtube.com/watch?v={video_id}",
            ],
            capture_output=True,
            text=True,
            timeout=20,
        )
        
        if result.returncode != 0:
            return None
        
        data = json.loads(result.stdout)
        duration = data.get("duration", 0)
        
        return {
            "duration_seconds": duration,
            "duration": f"{duration // 60}:{duration % 60:02d}",
            "description": data.get("description", "")[:1000],
            "published": data.get("upload_date", ""),
            "view_count": data.get("view_count", 0),
            "like_count": data.get("like_count", 0),
        }
        
    except Exception:
        return None


def get_transcript(video_id: str) -> Optional[str]:
    """Get video transcript using multiple methods to avoid rate limiting"""
    # Method 1: innertube ANDROID client + Cloudflare proxy (bypasses rate limits)
    transcript = _get_transcript_innertube_proxy(video_id)
    if transcript:
        return transcript
    
    # Method 2: youtube-transcript-api (fallback, may be rate limited)
    transcript = _get_transcript_ytapi(video_id)
    if transcript:
        return transcript
    
    return None


# Cloudflare Workers proxy for downloading caption XML (bypasses 429 rate limits)
CF_PROXY_URL = 'https://your-cloudflare-proxy.workers.dev/?url='  # Optional: Cloudflare Workers proxy to bypass rate limits


def _parse_caption_xml(xml_text: str) -> List[str]:
    """Parse YouTube caption XML (supports multiple formats)"""
    import xml.etree.ElementTree as ET
    import html as html_mod
    
    try:
        root = ET.fromstring(xml_text)
        texts = []
        
        # Try <p> tags first (format 3 and format 2)
        for p in root.findall('.//p'):
            # Check for <s> child tags (format 3: word-level)
            words = []
            for s in p.findall('s'):
                if s.text:
                    words.append(html_mod.unescape(s.text.strip()))
            if words:
                texts.append(' '.join(words))
            elif p.text:  # format 2: direct text
                texts.append(html_mod.unescape(p.text.strip()))
        
        # If no <p> found, try <text> tags (format 1)
        if not texts:
            for elem in root.findall('.//text'):
                if elem.text:
                    texts.append(html_mod.unescape(elem.text.strip()))
        
        return texts
    except Exception:
        return []


def _download_caption(url: str) -> Optional[str]:
    """Download caption content, try proxy first then direct"""
    import urllib.parse
    import requests
    
    # 1. Through Cloudflare proxy
    try:
        proxied = CF_PROXY_URL + urllib.parse.quote(url, safe='')
        r = requests.get(proxied, timeout=15)
        if r.status_code == 200 and r.text.strip():
            return r.text
    except Exception:
        pass
    
    # 2. Direct connection fallback
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200 and r.text.strip():
            return r.text
    except Exception:
        pass
    
    return None


def _get_transcript_innertube_proxy(video_id: str) -> Optional[str]:
    """Method 1: innertube ANDROID client + CF proxy to download captions"""
    try:
        import innertube
        
        client = innertube.InnerTube('ANDROID')
        data = client.player(video_id=video_id)
        
        if 'captions' not in data:
            return None
        
        caps = data['captions']['playerCaptionsTracklistRenderer']['captionTracks']
        if not caps:
            return None
        
        # Priority: en > zh-Hans > zh > first available
        cap_url = None
        for prefer in ['en', 'zh-Hans', 'zh']:
            for c in caps:
                if c.get('languageCode') == prefer:
                    cap_url = c['baseUrl']
                    break
            if cap_url:
                break
        if not cap_url:
            cap_url = caps[0]['baseUrl']
        
        xml_text = _download_caption(cap_url)
        if not xml_text:
            return None
        
        texts = _parse_caption_xml(xml_text)
        if not texts:
            return None
        
        result = ' '.join(texts).strip()
        return result if len(result) > 50 else None
        
    except Exception:
        return None


def _get_transcript_ytapi(video_id: str) -> Optional[str]:
    """Method 2 (fallback): youtube-transcript-api direct connection"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        
        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id, languages=["zh-Hans", "zh-Hant", "en"])
        transcript = " ".join([item["text"] for item in fetched])
        return transcript if len(transcript) > 50 else None
        
    except Exception:
        return None


def generate_summary(title: str, channel: str, duration: str, transcript: str) -> Optional[str]:
    """Generate summary using LLM API"""
    token = get_openclaw_token()
    if not token:
        print("⚠️ No OpenClaw token found", file=sys.stderr)
        return None
    
    prompt = SUMMARY_PROMPT_TEMPLATE.format(
        title=title,
        channel=channel,
        duration=duration,
        transcript=transcript[:8000]  # Limit transcript length
    )
    
    try:
        import requests
        
        response = requests.post(
            "http://localhost:3000/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",  # or your preferred model
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000
            },
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            print(f"⚠️ LLM API error: {response.status_code}", file=sys.stderr)
            return None
            
    except Exception as e:
        print(f"⚠️ Summary generation error: {e}", file=sys.stderr)
        return None


def process_video(video_id: str, title: str = None, channel: str = None) -> Dict:
    """Process a single video: get details, transcript, and summary"""
    print(f"📹 Processing: {video_id}")
    
    # Get video details
    details = get_video_details(video_id)
    if not details:
        return {
            "video_id": video_id,
            "title": title or "Unknown",
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "error": "Failed to fetch video details"
        }
    
    # Get transcript
    transcript = get_transcript(video_id)
    has_transcript = transcript is not None
    
    result = {
        "video_id": video_id,
        "title": title or "Unknown",
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "channel": channel or "Unknown",
        "duration": details["duration"],
        "published": details["published"],
        "has_transcript": has_transcript,
        "metadata": {
            "view_count": details.get("view_count", 0),
            "like_count": details.get("like_count", 0),
        }
    }
    
    # Generate summary if transcript available
    if has_transcript:
        print(f"  ✅ Transcript: {len(transcript)} chars")
        summary = generate_summary(title, channel, details["duration"], transcript)
        if summary:
            result["summary"] = summary
            print(f"  ✅ Summary: {len(summary)} chars")
        else:
            result["summary"] = f"⚠️ 摘要生成失败\n\n视频有字幕但 LLM 调用失败。"
    else:
        result["summary"] = f"📺 **需观看获取详细内容**\n\n视频暂无字幕，无法生成详细摘要。\n\n基于标题推测：{title}"
        print(f"  ⚠️ No transcript available")
    
    return result


def main():
    parser = argparse.ArgumentParser(description="YouTube Summarizer")
    parser.add_argument("--url", help="Single video URL")
    parser.add_argument("--channel", help="Channel ID or handle")
    parser.add_argument("--config", help="Config file path (JSON)")
    parser.add_argument("--daily", action="store_true", help="Daily batch mode (requires --config)")
    parser.add_argument("--hours", type=int, default=DEFAULT_HOURS_LOOKBACK, help="Hours to look back")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output JSON file")
    
    args = parser.parse_args()
    
    results = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "items": [],
        "stats": {
            "total_videos": 0,
            "with_transcript": 0,
            "without_transcript": 0
        }
    }
    
    # Mode 1: Single video
    if args.url:
        video_id = args.url.split("v=")[-1].split("&")[0]
        result = process_video(video_id)
        results["items"].append(result)
        results["stats"]["total_videos"] = 1
        if result.get("has_transcript"):
            results["stats"]["with_transcript"] = 1
        else:
            results["stats"]["without_transcript"] = 1
    
    # Mode 2: Channel scan
    elif args.channel:
        videos = get_channel_videos(args.channel, args.hours, DEFAULT_MAX_VIDEOS_PER_CHANNEL)
        print(f"📺 Found {len(videos)} videos from channel")
        
        for video in videos:
            result = process_video(video["id"], video["title"], video["channel"])
            results["items"].append(result)
            results["stats"]["total_videos"] += 1
            if result.get("has_transcript"):
                results["stats"]["with_transcript"] += 1
            else:
                results["stats"]["without_transcript"] += 1
    
    # Mode 3: Daily batch (config file)
    elif args.daily and args.config:
        with open(args.config, "r") as f:
            config = json.load(f)
        
        channels = config.get("channels", [])
        hours = config.get("hours_lookback", args.hours)
        max_videos = config.get("max_videos_per_channel", DEFAULT_MAX_VIDEOS_PER_CHANNEL)
        
        print(f"📺 Processing {len(channels)} channels")
        
        for ch in channels:
            channel_id = ch.get("id") or ch.get("url")
            channel_name = ch.get("name", "Unknown")
            
            print(f"\n🔍 Channel: {channel_name}")
            videos = get_channel_videos(channel_id, hours, max_videos)
            print(f"  Found {len(videos)} videos")
            
            for video in videos:
                result = process_video(video["id"], video["title"], channel_name)
                results["items"].append(result)
                results["stats"]["total_videos"] += 1
                if result.get("has_transcript"):
                    results["stats"]["with_transcript"] += 1
                else:
                    results["stats"]["without_transcript"] += 1
    
    else:
        parser.print_help()
        sys.exit(1)
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Output written to: {output_path}")
    print(f"📊 Stats: {results['stats']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Extract audio from video files or URLs using ffmpeg and yt-dlp.
Supports various input formats and output formats (mp3, wav, m4a, flac, etc.)
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
import tempfile
import urllib.request
import urllib.parse
import shutil


def find_yt_dlp():
    """Find yt-dlp executable in various locations."""
    paths = [
        "yt-dlp",
        "/Users/Clawdbot/Library/Python/3.9/bin/yt-dlp",
        os.path.expanduser("~/.local/bin/yt-dlp"),
        os.path.expanduser("~/Library/Python/3.9/bin/yt-dlp"),
        os.path.expanduser("~/Library/Python/3.10/bin/yt-dlp"),
        os.path.expanduser("~/Library/Python/3.11/bin/yt-dlp"),
        "/usr/local/bin/yt-dlp",
        "/opt/homebrew/bin/yt-dlp",
    ]
    
    for path in paths:
        try:
            subprocess.run([path, "--version"], capture_output=True, check=True)
            return path
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    return None


def is_youtube_url(url: str) -> bool:
    """Check if URL is a YouTube video."""
    url_lower = url.lower()
    return any(domain in url_lower for domain in [
        'youtube.com/watch',
        'youtu.be/',
        'youtube.com/shorts',
        'm.youtube.com'
    ])


def download_youtube_audio(url: str, output_path: str, yt_dlp: str) -> str:
    """
    Download and extract audio directly from YouTube using yt-dlp.
    This is more efficient than downloading the full video.
    """
    print(f"Extracting audio directly from YouTube...")
    
    # Determine format and codec
    ext = Path(output_path).suffix.lower()
    
    # yt-dlp audio format selection
    # Best audio quality, convert to desired format
    format_map = {
        '.mp3': 'mp3',
        '.m4a': 'm4a',
        '.aac': 'm4a',
        '.wav': 'wav',
        '.flac': 'flac',
        '.ogg': 'vorbis',
        '.opus': 'opus'
    }
    
    audio_format = format_map.get(ext, 'mp3')
    
    # Build yt-dlp command for direct audio extraction
    cmd = [
        yt_dlp,
        "-f", "bestaudio/best",  # Best audio quality
        "--extract-audio",
        "--audio-format", audio_format,
        "--audio-quality", "0",  # Best quality
        "-o", output_path.replace(ext, '.%(ext)s'),  # yt-dlp will add extension
        "--no-playlist",
        "--newline",
        url
    ]
    
    # Add user-agent to avoid some blocks
    cmd.extend([
        "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ])
    
    try:
        print(f"Running: {' '.join(cmd[:10])}...")  # Truncate for display
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            # Check for specific errors
            if "403" in result.stderr or "Forbidden" in result.stderr:
                raise RuntimeError(
                    "YouTube blocked the download (403 Forbidden). "
                    "This is common. Try:\n"
                    "1. Update yt-dlp: pip3 install -U yt-dlp\n"
                    "2. Use --cookies-from-browser chrome (if you have YouTube cookies)\n"
                    "3. Download via browser extension first, then use this tool on the file"
                )
            elif "Sign in" in result.stderr or "signin" in result.stderr:
                raise RuntimeError(
                    "YouTube requires sign-in for this video. "
                    "Try using --cookies-from-browser option or download manually."
                )
            else:
                raise RuntimeError(f"yt-dlp failed: {result.stderr[:500]}")
        
        # yt-dlp might change extension, find the actual output file
        actual_output = output_path
        if not os.path.exists(actual_output):
            # Try to find the file with the new extension
            base = output_path.replace(ext, '')
            for possible_ext in ['.mp3', '.m4a', '.webm', '.opus']:
                if os.path.exists(base + possible_ext):
                    actual_output = base + possible_ext
                    break
        
        print(f"✓ Audio extracted successfully: {actual_output}")
        return actual_output
        
    except subprocess.TimeoutExpired:
        raise RuntimeError("Download timed out (120s). Video may be too large or connection slow.")


def download_youtube_video(url: str, output_dir: str, yt_dlp: str) -> str:
    """Download YouTube video as fallback."""
    output_path = os.path.join(output_dir, "youtube_video.mp4")
    
    print(f"Downloading YouTube video...")
    cmd = [
        yt_dlp,
        "-f", "best[height<=720][ext=mp4]/best[height<=720]/best",
        "-o", output_path,
        "--no-playlist",
        "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        url
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=120)
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to download video: {e.stderr[:500]}")


def download_generic_video(url: str, output_dir: str) -> str:
    """Download generic video from URL."""
    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path)
    if not filename or '.' not in filename:
        filename = "downloaded_video.mp4"
    
    output_path = os.path.join(output_dir, filename)
    
    print(f"Downloading video from {url}...")
    
    # Create request with headers to avoid some blocks
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        print(f"Downloaded to {output_path}")
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to download: {e}")


def extract_audio_from_file(input_path: str, output_path: str, format: str = None,
                            bitrate: str = "192k", sample_rate: int = None) -> str:
    """Extract audio from local video file using ffmpeg."""
    
    if format is None:
        format = Path(output_path).suffix.lstrip('.').lower()
    
    cmd = ["ffmpeg", "-y", "-i", input_path]
    
    # Audio codec selection
    codec_map = {
        "mp3": "libmp3lame",
        "wav": "pcm_s16le",
        "m4a": "aac",
        "aac": "aac",
        "flac": "flac",
        "ogg": "libvorbis",
        "opus": "libopus",
    }
    
    if format in codec_map:
        cmd.extend(["-c:a", codec_map[format]])
    
    # Quality settings
    if format == "mp3":
        cmd.extend(["-b:a", bitrate])
        if sample_rate:
            cmd.extend(["-ar", str(sample_rate)])
    elif format in ["m4a", "aac"]:
        cmd.extend(["-b:a", bitrate])
    elif format == "wav" and sample_rate:
        cmd.extend(["-ar", str(sample_rate)])
    
    cmd.extend(["-vn", output_path])
    
    print(f"Extracting audio...")
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✓ Audio extracted: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg failed: {e.stderr[:500]}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract audio from video files or URLs"
    )
    parser.add_argument("input", help="Input video file path or URL")
    parser.add_argument("-o", "--output", help="Output audio file path")
    parser.add_argument(
        "-f", "--format",
        choices=["mp3", "wav", "m4a", "aac", "flac", "ogg", "opus"],
        default="mp3",
        help="Output format (default: mp3)"
    )
    parser.add_argument("-b", "--bitrate", default="192k", help="Audio bitrate")
    parser.add_argument("-r", "--sample-rate", type=int, help="Sample rate in Hz")
    parser.add_argument("--keep-video", action="store_true", help="Keep downloaded video")
    parser.add_argument("--video-only", action="store_true", help="Download video only, don't extract audio")
    
    args = parser.parse_args()
    
    # Generate output path
    if args.output:
        output_path = args.output
    else:
        if args.input.startswith(("http://", "https://")):
            stem = "audio"
        else:
            stem = Path(args.input).stem
        output_path = f"{stem}.{args.format}"
    
    temp_files = []
    
    try:
        # Handle URL input
        if args.input.startswith(("http://", "https://")):
            yt_dlp = find_yt_dlp()
            
            if is_youtube_url(args.input):
                if not yt_dlp:
                    print("Error: yt-dlp required for YouTube videos.", file=sys.stderr)
                    print("Install: pip3 install yt-dlp", file=sys.stderr)
                    sys.exit(1)
                
                if args.video_only:
                    # Download video only
                    temp_dir = tempfile.gettempdir()
                    video_path = download_youtube_video(args.input, temp_dir, yt_dlp)
                    print(f"Video saved to: {video_path}")
                    print("Use this file as input to extract audio")
                    return
                else:
                    # Direct audio extraction from YouTube
                    try:
                        result = download_youtube_audio(args.input, output_path, yt_dlp)
                        print(f"\n✓ Success! Audio saved to: {result}")
                        return
                    except RuntimeError as e:
                        print(f"Direct extraction failed: {e}", file=sys.stderr)
                        print("Falling back to video download + extraction...", file=sys.stderr)
                        # Fallback to video download
                        temp_dir = tempfile.gettempdir()
                        video_path = download_youtube_video(args.input, temp_dir, yt_dlp)
                        temp_files.append(video_path)
                        input_path = video_path
            else:
                # Generic URL
                temp_dir = tempfile.gettempdir()
                video_path = download_generic_video(args.input, temp_dir)
                temp_files.append(video_path)
                input_path = video_path
        else:
            # Local file
            if not os.path.exists(args.input):
                print(f"Error: File not found: {args.input}", file=sys.stderr)
                sys.exit(1)
            input_path = args.input
        
        # Extract audio from file
        result = extract_audio_from_file(
            input_path, output_path, args.format, args.bitrate, args.sample_rate
        )
        
        # Cleanup
        if temp_files and not args.keep_video:
            for f in temp_files:
                if os.path.exists(f):
                    os.remove(f)
            print("Cleaned up temporary files")
        
        print(f"\n✓ Success! Audio saved to: {result}")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        # Cleanup on error
        for f in temp_files:
            if os.path.exists(f):
                os.remove(f)
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

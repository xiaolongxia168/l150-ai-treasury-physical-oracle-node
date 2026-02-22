# Video Audio Extractor

從視頻提取音頻的 OpenClaw Skill，支持 YouTube、Bilibili 和本地視頻文件。

## 功能特點

- 🎬 支持多種視頻來源：YouTube、Bilibili、本地文件
- 🎵 多種音頻格式輸出：MP3、WAV、M4A、FLAC、OGG、OPUS
- ⚡ 使用 yt-dlp 高效下載和提取
- 🔧 可調整音質參數

## 安裝需求

```bash
# 安裝依賴
pip3 install yt-dlp

# 確保 ffmpeg 已安裝（macOS）
brew install ffmpeg
```

## 使用方法

### 基本用法

```bash
# 提取 YouTube 視頻音頻（默認 MP3）
python3 extract-audio.py "https://www.youtube.com/watch?v=..."

# 提取 Bilibili 視頻音頻
python3 extract-audio.py "https://www.bilibili.com/video/BV1YY6qBoEHc"

# 提取本地視頻文件
python3 extract-audio.py "/path/to/video.mp4"
```

### 指定輸出格式

```bash
# 輸出為 WAV 格式
python3 extract-audio.py "URL" -f wav

# 輸出為 FLAC 無損格式
python3 extract-audio.py "URL" -f flac

# 輸出為 M4A（AAC 編碼）
python3 extract-audio.py "URL" -f m4a
```

### 指定音質

```bash
# 最高音質（320kbps MP3）
python3 extract-audio.py "URL" -q 0

# 標準音質（192kbps MP3）
python3 extract-audio.py "URL" -q 2

# 較低音質（128kbps MP3）
python3 extract-audio.py "URL" -q 5
```

### 指定輸出目錄

```bash
python3 extract-audio.py "URL" -o ~/Music/Extracted/
```

### 批量處理

```bash
# 從文件批量提取
python3 extract-audio.py urls.txt
```

## 完整參數說明

```
extract-audio.py [-h] [-f {mp3,wav,m4a,flac,ogg,opus}] [-o OUTPUT] [-q {0,1,2,3,4,5}] input

位置參數:
  input                 YouTube/Bilibili URL 或本地文件路徑

選項參數:
  -h, --help            顯示幫助信息
  -f, --format          輸出格式 (默認: mp3)
  -o, --output          輸出目錄 (默認: ~/Downloads/Extracted_Audio/)
  -q, --quality         音質等級 0-5，0為最高 (默認: 0)
```

## 支持的視頻平台

| 平台 | 狀態 | 說明 |
|------|------|------|
| YouTube | ✅ | 支持所有公開視頻 |
| Bilibili | ✅ | 支持普通視頻，4K/1080P60需會員 |
| 本地文件 | ✅ | 任何 ffmpeg 支持的格式 |

## 注意事項

⚠️ **版權聲明**：請確保你有權下載和使用目標視頻的音頻內容。

⚠️ **Bilibili 限制**：部分高畫質格式需要會員 cookies 才能訪問。

⚠️ **YouTube 限制**：某些視頻可能因版權或地區限制無法下載。

## 常見問題

### Q: 下載失敗顯示 403 錯誤？
A: YouTube 有時會阻止下載。可以嘗試：
- 更新 yt-dlp：`pip3 install -U yt-dlp`
- 使用 cookies：添加 `--cookies-from-browser chrome`

### Q: Bilibili 視頻無法下載？
- 確保視頻是公開的
- 某些地區限制視頻可能需要代理

### Q: 如何提取整個播放列表？
A: 目前版本只支持單個視頻，播放列表功能正在開發中。

## 作為 OpenClaw Skill 使用

```bash
# 安裝 Skill
openclaw skills install /path/to/video-audio-extractor.skill

# 或在 OpenClaw 對話中使用
"幫我提取這個 YouTube 視頻的音頻: https://..."
```

## 開發者

Created by [kantylee](https://github.com/kantylee) for OpenClaw

## 許可證

MIT License

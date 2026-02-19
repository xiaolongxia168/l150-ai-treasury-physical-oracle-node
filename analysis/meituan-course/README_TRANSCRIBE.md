# 🎬 视频转录 + 🤖 AI知识库投喂系统

一键将美团运营课程视频转录并投喂给AI数字运营系统。

## 🚀 快速开始

### 方式1: 一键全自动 (推荐)

```bash
cd ~/.openclaw/workspace/analysis/meituan-course
export OPENAI_API_KEY="your-api-key"
./run_full_pipeline.sh
```

### 方式2: Python脚本 (更灵活)

```bash
cd ~/.openclaw/workspace/analysis/meituan-course
export OPENAI_API_KEY="your-api-key"

# 查看统计
python3 transcribe_and_feed.py stats

# 开始转录
python3 transcribe_and_feed.py

# 投喂给AI系统
cd ~/.openclaw/workspace/密室逃脱运营
python3 scripts/knowledge_feeder.py
```

## 📁 文件说明

| 文件 | 功能 |
|------|------|
| `transcribe_and_feed.py` | 核心转录脚本：视频→音频→API→知识库 |
| `run_full_pipeline.sh` | 一键执行脚本 |
| `knowledge_feeder.py` | AI知识库投喂器 |

## 📂 输出目录

```
分析目录/
├── audio-extracted/          # 提取的MP3音频
├── transcripts-api/          # Whisper API转录文本
└── 知识库/
    ├── 课程转录/             # 结构化JSON+Markdown
    ├── knowledge_base_rag.json  # RAG知识库
    ├── 美团运营课程知识库.md    # 可读知识库
    └── ai_system_prompt.txt     # AI系统提示词
```

## 🔧 功能特性

- ✅ FFmpeg提取音频（压缩至原体积~5%）
- ✅ OpenAI Whisper API转录（中文优化）
- ✅ 自动断点续传
- ✅ 结构化存储（JSON + Markdown）
- ✅ 自动生成摘要和关键词
- ✅ 投喂给AI数字运营系统

## ⚙️ 配置选项

在 `transcribe_and_feed.py` 中修改 `CONFIG`:

```python
CONFIG = {
    "video_dir": "/path/to/videos",      # 视频目录
    "max_workers": 2,                     # 并发数
    "api_timeout": 300,                   # API超时(秒)
}
```

## 📊 命令参考

```bash
# 查看统计
python3 transcribe_and_feed.py stats

# 重置进度（重新转录）
python3 transcribe_and_feed.py reset

# 显示帮助
python3 transcribe_and_feed.py help
```

## 💡 使用场景

1. **AI客服训练**: 转录内容作为客服知识库
2. **运营策略参考**: AI根据课程知识给出运营建议
3. **内容检索**: RAG系统支持语义搜索
4. **培训材料**: 生成可搜索的文档库

## 🔑 API密钥

需要OpenAI API Key，支持按量付费：
- Whisper API: $0.006/分钟
- 1小时视频约 $0.36

获取方式: https://platform.openai.com/api-keys

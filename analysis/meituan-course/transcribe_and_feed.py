#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频转录与AI知识库投喂系统
功能：批量提取视频音频 → Whisper API转录 → 结构化存储 → AI运营知识库
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# ============ 配置 ============
CONFIG = {
    "video_dir": "/Users/xiaolongxia/Downloads/美团运营/巅峰流量·实体团购操盘手【正式版】",
    "audio_output_dir": "/Users/xiaolongxia/.openclaw/workspace/analysis/meituan-course/audio-extracted",
    "transcript_output_dir": "/Users/xiaolongxia/.openclaw/workspace/analysis/meituan-course/transcripts-api",
    "knowledge_base_dir": "/Users/xiaolongxia/.openclaw/workspace/密室逃脱运营/知识库/课程转录",
    "progress_file": "/Users/xiaolongxia/.openclaw/workspace/analysis/meituan-course/.transcribe_progress.json",
    "log_file": "/Users/xiaolongxia/.openclaw/workspace/analysis/meituan-course/transcribe.log",
    
    # API配置
    "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
    "whisper_model": "whisper-1",
    "whisper_language": "zh",
    
    # 并发配置
    "max_workers": 2,  # 同时处理2个视频
    "api_timeout": 300,  # API调用超时5分钟
}

# ============ 日志系统 ============
class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{level}] {message}"
        print(log_line)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
    
    def info(self, msg): self.log(msg, "INFO")
    def success(self, msg): self.log(msg, "SUCCESS")
    def warning(self, msg): self.log(msg, "WARNING")
    def error(self, msg): self.log(msg, "ERROR")

logger = Logger(CONFIG["log_file"])

# ============ 进度管理 ============
class ProgressManager:
    def __init__(self, progress_file):
        self.progress_file = progress_file
        self.completed = self._load()
    
    def _load(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"completed_videos": [], "completed_transcripts": []}
    
    def save(self):
        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(self.completed, f, ensure_ascii=False, indent=2)
    
    def is_video_extracted(self, video_path):
        return video_path in self.completed.get("completed_videos", [])
    
    def is_transcribed(self, video_path):
        return video_path in self.completed.get("completed_transcripts", [])
    
    def mark_video_extracted(self, video_path):
        if video_path not in self.completed["completed_videos"]:
            self.completed["completed_videos"].append(video_path)
            self.save()
    
    def mark_transcribed(self, video_path):
        if video_path not in self.completed["completed_transcripts"]:
            self.completed["completed_transcripts"].append(video_path)
            self.save()

progress = ProgressManager(CONFIG["progress_file"])

# ============ 视频处理类 ============
class VideoProcessor:
    def __init__(self):
        self.video_dir = Path(CONFIG["video_dir"])
        self.audio_dir = Path(CONFIG["audio_output_dir"])
        self.transcript_dir = Path(CONFIG["transcript_output_dir"])
        self.kb_dir = Path(CONFIG["knowledge_base_dir"])
        
        # 创建输出目录
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.transcript_dir.mkdir(parents=True, exist_ok=True)
        self.kb_dir.mkdir(parents=True, exist_ok=True)
    
    def scan_videos(self):
        """扫描所有视频文件"""
        videos = []
        for ext in ["*.mp4", "*.MP4", "*.mov", "*.MOV"]:
            videos.extend(self.video_dir.rglob(ext))
        return sorted(videos)
    
    def extract_audio(self, video_path):
        """提取音频（使用FFmpeg）"""
        video_path = Path(video_path)
        base_name = video_path.stem
        audio_path = self.audio_dir / f"{base_name}.mp3"
        
        # 检查是否已提取
        if progress.is_video_extracted(str(video_path)) and audio_path.exists():
            logger.info(f"⏭️  音频已提取，跳过: {base_name}")
            return str(audio_path)
        
        logger.info(f"🎵 提取音频: {base_name}")
        
        cmd = [
            "ffmpeg",
            "-i", str(video_path),
            "-vn",  # 不处理视频
            "-acodec", "libmp3lame",
            "-ar", "16000",  # 16kHz采样率（Whisper推荐）
            "-ac", "1",  # 单声道
            "-b:a", "32k",  # 32kbps码率
            "-y",  # 覆盖输出文件
            str(audio_path)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                video_size = video_path.stat().st_size / (1024 * 1024)
                audio_size = audio_path.stat().st_size / (1024 * 1024)
                logger.success(f"  ✅ 提取完成: {video_size:.1f}MB → {audio_size:.1f}MB ({audio_size/video_size*100:.1f}%)")
                progress.mark_video_extracted(str(video_path))
                return str(audio_path)
            else:
                logger.error(f"  ❌ FFmpeg错误: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error(f"  ⏱️  提取超时: {base_name}")
            return None
        except Exception as e:
            logger.error(f"  ❌ 提取失败: {base_name} - {str(e)}")
            return None
    
    def transcribe_with_whisper(self, audio_path, video_path):
        """使用本地Whisper转录"""
        audio_path = Path(audio_path)
        base_name = audio_path.stem
        transcript_path = self.transcript_dir / f"{base_name}.txt"
        
        # 检查是否已转录
        if progress.is_transcribed(str(video_path)) and transcript_path.exists():
            logger.info(f"⏭️  已转录，跳过: {base_name}")
            return str(transcript_path)
        
        logger.info(f"🎯 本地Whisper转录: {base_name}")
        
        try:
            import whisper
            
            # 加载模型 (small模型平衡速度和准确度)
            logger.info(f"  🔄 加载Whisper模型...")
            model = whisper.load_model("small")
            
            # 转录
            logger.info(f"  📝 开始转录...")
            result = model.transcribe(
                str(audio_path),
                language="zh",
                verbose=False,
                initial_prompt="这是一段关于美团运营和实体店团购的教程视频。"
            )
            
            transcript_text = result["text"]
            transcript_path.write_text(transcript_text, encoding="utf-8")
            
            char_count = len(transcript_text)
            logger.success(f"  ✅ 转录完成: {base_name} ({char_count} 字符)")
            progress.mark_transcribed(str(video_path))
            return str(transcript_path)
            
        except ImportError:
            logger.error(f"  ❌ 未安装Whisper: pip3 install openai-whisper")
            return None
        except Exception as e:
            logger.error(f"  ❌ 转录失败: {base_name} - {str(e)}")
            return None
    
    def generate_summary(self, transcript_path, video_path):
        """生成内容摘要和结构化数据"""
        transcript_path = Path(transcript_path)
        base_name = transcript_path.stem
        
        # 读取转录文本
        transcript_text = transcript_path.read_text(encoding="utf-8")
        
        # 提取元数据
        metadata = {
            "video_name": base_name,
            "video_path": str(video_path),
            "transcript_path": str(transcript_path),
            "processed_at": datetime.now().isoformat(),
            "char_count": len(transcript_text),
            "word_count": len(transcript_text.split()),
            "category": self._extract_category(base_name),
        }
        
        # 生成摘要（简单提取前500字作为摘要）
        summary = transcript_text[:500] + "..." if len(transcript_text) > 500 else transcript_text
        metadata["summary"] = summary
        
        # 提取关键主题（简单的关键词匹配）
        keywords = self._extract_keywords(transcript_text)
        metadata["keywords"] = keywords
        
        return metadata
    
    def _extract_category(self, filename):
        """从文件名提取分类"""
        categories = {
            "评价": "评价与星级评分",
            "推广通": "推广通",
            "后台数据": "后台数据分析",
            "流量": "流量运营",
            "转化": "转化优化",
        }
        for key, value in categories.items():
            if key in filename:
                return value
        return "其他"
    
    def _extract_keywords(self, text):
        """提取关键词"""
        keywords = []
        keyword_patterns = [
            "美团", "大众点评", "星级", "评价", "推广通", "流量",
            "转化", "ROI", "CPA", "CPC", "自然流量", "付费推广",
            "榜单", "好评", "差评", "回复", "运营", "团购"
        ]
        for keyword in keyword_patterns:
            if keyword in text:
                keywords.append(keyword)
        return list(set(keywords))[:10]  # 最多10个关键词
    
    def save_to_knowledge_base(self, metadata, transcript_text):
        """保存到AI运营知识库"""
        base_name = metadata["video_name"]
        
        # 保存结构化JSON
        json_path = self.kb_dir / f"{base_name}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        # 保存Markdown格式（便于阅读和RAG）
        md_path = self.kb_dir / f"{base_name}.md"
        md_content = f"""# {base_name}

## 元数据
- **分类**: {metadata['category']}
- **处理时间**: {metadata['processed_at']}
- **字符数**: {metadata['char_count']}
- **关键词**: {', '.join(metadata['keywords'])}

## 摘要
{metadata['summary']}

## 完整内容
{transcript_text}

---
*自动生成的运营知识库文档*
"""
        md_path.write_text(md_content, encoding="utf-8")
        
        logger.success(f"  💾 已保存到知识库: {base_name}")
        return str(md_path)
    
    def process_single_video(self, video_path):
        """处理单个视频的完整流程"""
        video_path = Path(video_path)
        base_name = video_path.stem
        
        logger.info(f"\n{'='*50}")
        logger.info(f"📹 开始处理: {base_name}")
        logger.info(f"{'='*50}")
        
        # 步骤1: 提取音频
        audio_path = self.extract_audio(video_path)
        if not audio_path:
            logger.error(f"❌ 音频提取失败，跳过: {base_name}")
            return False
        
        # 步骤2: Whisper转录
        transcript_path = self.transcribe_with_whisper(audio_path, video_path)
        if not transcript_path:
            logger.error(f"❌ 转录失败，跳过: {base_name}")
            return False
        
        # 步骤3: 生成摘要和结构化数据
        transcript_text = Path(transcript_path).read_text(encoding="utf-8")
        metadata = self.generate_summary(transcript_path, video_path)
        
        # 步骤4: 保存到知识库
        self.save_to_knowledge_base(metadata, transcript_text)
        
        logger.success(f"✅ 完成处理: {base_name}")
        return True
    
    def run(self, max_workers=None):
        """运行批量处理"""
        if max_workers is None:
            max_workers = CONFIG["max_workers"]
        
        logger.info("🚀 启动视频转录与知识库投喂系统")
        logger.info(f"📁 视频目录: {CONFIG['video_dir']}")
        
        # 扫描视频
        videos = self.scan_videos()
        if not videos:
            logger.error("❌ 未找到视频文件")
            return
        
        logger.info(f"📹 找到 {len(videos)} 个视频文件")
        
        # 统计待处理数量
        pending = [v for v in videos if not progress.is_transcribed(str(v))]
        logger.info(f"⏳ 待处理: {len(pending)} 个，已跳过: {len(videos) - len(pending)} 个")
        
        # 批量处理
        success_count = 0
        fail_count = 0
        
        for i, video_path in enumerate(videos, 1):
            logger.info(f"\n[{i}/{len(videos)}] 处理进度")
            
            if self.process_single_video(video_path):
                success_count += 1
            else:
                fail_count += 1
            
            # 每处理完一个，短暂休息避免API限流
            time.sleep(1)
        
        # 统计报告
        logger.info(f"\n{'='*50}")
        logger.info("📊 处理完成统计")
        logger.info(f"{'='*50}")
        logger.info(f"总计: {len(videos)} 个视频")
        logger.info(f"成功: {success_count} 个")
        logger.info(f"失败: {fail_count} 个")
        logger.info(f"\n📂 输出目录:")
        logger.info(f"   音频: {CONFIG['audio_output_dir']}")
        logger.info(f"   文本: {CONFIG['transcript_output_dir']}")
        logger.info(f"   知识库: {CONFIG['knowledge_base_dir']}")
        logger.info(f"   日志: {CONFIG['log_file']}")

# ============ 主函数 ============
def main():
    processor = VideoProcessor()
    processor.run()

def show_stats():
    """显示统计信息"""
    processor = VideoProcessor()
    videos = processor.scan_videos()
    
    print("\n" + "="*50)
    print("📊 转录统计")
    print("="*50)
    print(f"总视频数: {len(videos)}")
    print(f"已完成: {len(progress.completed.get('completed_transcripts', []))}")
    print(f"剩余: {len(videos) - len(progress.completed.get('completed_transcripts', []))}")
    print("\n视频列表:")
    for i, v in enumerate(videos, 1):
        status = "✅" if progress.is_transcribed(str(v)) else "⏳"
        print(f"  {status} {i}. {v.name}")

def reset_progress():
    """重置进度"""
    if os.path.exists(CONFIG["progress_file"]):
        os.remove(CONFIG["progress_file"])
    print("✅ 进度已重置")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ["stats", "-s", "--stats"]:
            show_stats()
        elif sys.argv[1] in ["reset", "-r", "--reset"]:
            reset_progress()
        elif sys.argv[1] in ["help", "-h", "--help"]:
            print("""视频转录与AI知识库投喂系统

用法: python3 transcribe_and_feed.py [选项]

选项:
  (无)       开始批量处理
  stats      显示统计信息
  reset      重置处理进度
  help       显示帮助

环境变量:
  OPENAI_API_KEY    OpenAI API密钥 (必需)
""")
        else:
            print(f"未知选项: {sys.argv[1]}")
    else:
        main()

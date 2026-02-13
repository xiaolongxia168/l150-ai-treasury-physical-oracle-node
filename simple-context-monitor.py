#!/usr/bin/env python3
"""
Simple Context Monitor - 监控聊天窗口上下文使用率
当达到阈值时自动触发新会话
"""

import subprocess
import json
import re
import time
import os
from datetime import datetime

# 配置
THRESHOLD_PERCENT = 95
CHECK_INTERVAL = 300  # 5分钟
LOG_FILE = "/Users/xiaolongxia/.openclaw/workspace/context-monitor.log"
STATE_FILE = "/Users/xiaolongxia/.openclaw/workspace/last-context-state.json"

def log_message(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    
    print(log_entry.strip())

def get_session_status():
    """获取当前会话状态"""
    try:
        # 使用openclaw session status命令
        result = subprocess.run(
            ["openclaw", "session", "status", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            log_message(f"Error getting session status: {result.stderr}")
            return None
        
        # 解析输出
        output = result.stdout.strip()
        
        # 查找上下文使用率信息
        # 格式示例: 📚 Context: 42k/64k (66%) · 🧹 Compactions: 0
        pattern = r'Context:\s*(\d+)k/(\d+)k\s*\((\d+)%\)'
        match = re.search(pattern, output)
        
        if match:
            current_kb = int(match.group(1))
            total_kb = int(match.group(2))
            percent = int(match.group(3))
            
            return {
                "current_kb": current_kb,
                "total_kb": total_kb,
                "percent": percent,
                "raw_output": output
            }
        else:
            # 尝试其他格式
            pattern2 = r'(\d+)k/(\d+)k\s*\((\d+)%\)'
            match2 = re.search(pattern2, output)
            if match2:
                current_kb = int(match2.group(1))
                total_kb = int(match2.group(2))
                percent = int(match2.group(3))
                
                return {
                    "current_kb": current_kb,
                    "total_kb": total_kb,
                    "percent": percent,
                    "raw_output": output
                }
            
            log_message(f"Could not parse context usage from: {output[:100]}...")
            return None
            
    except subprocess.TimeoutExpired:
        log_message("Timeout getting session status")
        return None
    except Exception as e:
        log_message(f"Exception getting session status: {e}")
        return None

def save_state(state):
    """保存状态到文件"""
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "state": state
            }, f, indent=2)
    except Exception as e:
        log_message(f"Error saving state: {e}")

def load_state():
    """从文件加载状态"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        log_message(f"Error loading state: {e}")
    return None

def trigger_new_conversation(state):
    """触发新对话"""
    log_message(f"🚨 CRITICAL: Context usage at {state['percent']}%!")
    log_message(f"   Current: {state['current_kb']}k / Total: {state['total_kb']}k")
    
    # 保存当前状态快照
    snapshot_file = f"/Users/xiaolongxia/.openclaw/workspace/snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    try:
        with open(snapshot_file, "w", encoding="utf-8") as f:
            f.write(f"# Context Snapshot - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Usage Statistics\n")
            f.write(f"- Percentage: {state['percent']}%\n")
            f.write(f"- Current: {state['current_kb']}k\n")
            f.write(f"- Total: {state['total_kb']}k\n\n")
            f.write(f"## Raw Output\n```\n{state['raw_output']}\n```\n\n")
            f.write(f"## Action Taken\n")
            f.write(f"- Threshold: {THRESHOLD_PERCENT}%\n")
            f.write(f"- Time: {datetime.now().isoformat()}\n")
            f.write(f"- Action: New conversation triggered\n")
        
        log_message(f"📸 Saved snapshot to: {snapshot_file}")
        
        # 这里可以添加实际触发新对话的逻辑
        # 例如：发送系统消息、重启会话等
        
        # 临时方案：创建标记文件供其他进程检测
        marker_file = "/tmp/openclaw_needs_restart.txt"
        with open(marker_file, "w", encoding="utf-8") as f:
            f.write(f"Context usage: {state['percent']}%\n")
            f.write(f"Time: {datetime.now().isoformat()}\n")
            f.write(f"Action required: Start new conversation\n")
        
        log_message(f"📝 Created restart marker: {marker_file}")
        
        return True
        
    except Exception as e:
        log_message(f"Error creating snapshot: {e}")
        return False

def main():
    """主监控循环"""
    log_message("=== Context Monitor Started ===")
    log_message(f"Threshold: {THRESHOLD_PERCENT}%")
    log_message(f"Check interval: {CHECK_INTERVAL} seconds")
    
    last_state = load_state()
    if last_state:
        log_message(f"Loaded previous state from: {last_state.get('timestamp', 'unknown')}")
    
    try:
        while True:
            # 获取当前状态
            state = get_session_status()
            
            if state:
                log_message(f"Current context: {state['percent']}% ({state['current_kb']}k/{state['total_kb']}k)")
                
                # 保存状态
                save_state(state)
                
                # 检查是否达到阈值
                if state['percent'] >= THRESHOLD_PERCENT:
                    log_message(f"⚠️  Warning: Approaching limit ({state['percent']}%)")
                    
                    # 如果连续多次达到阈值，触发新对话
                    if last_state and last_state.get('state', {}).get('percent', 0) >= THRESHOLD_PERCENT:
                        log_message("🚨 Threshold persistently exceeded - triggering new conversation")
                        trigger_new_conversation(state)
                    else:
                        log_message("⚠️  First threshold warning - monitoring...")
                
                last_state = {"timestamp": datetime.now().isoformat(), "state": state}
            else:
                log_message("⚠️  Could not get session status")
            
            # 等待下一次检查
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        log_message("=== Context Monitor Stopped by User ===")
    except Exception as e:
        log_message(f"=== Context Monitor Crashed: {e} ===")

if __name__ == "__main__":
    main()
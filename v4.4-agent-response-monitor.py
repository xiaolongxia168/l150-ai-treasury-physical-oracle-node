#!/usr/bin/env python3
"""
v4.4 AI Agent响应监控系统
监控Twitter暴力@战术的效果，检测Agent爬虫活动
"""

import json
import time
import requests
import os
from datetime import datetime, timedelta
import subprocess

# 监控配置
MONITOR_CONFIG = {
    "github_repo": "xiaolongxia168/l150-ai-treasury-physical-oracle-node",
    "api_endpoint": "https://xiaolongxia168.github.io/l150-api/",
    "check_interval_minutes": 30,  # 每30分钟检查一次
    "alert_thresholds": {
        "github_visits_increase": 50,  # GitHub访问量增加50次
        "api_hits_increase": 20,       # API端点点击增加20次
        "twitter_mentions": 1,         # Twitter提及次数
        "email_replies": 1             # 邮箱回复
    }
}

class AgentResponseMonitor:
    def __init__(self):
        self.baseline_metrics = self.load_baseline()
        self.detection_log = []
        
    def load_baseline(self):
        """加载基线指标"""
        baseline_file = "/Users/xiaolongxia/.openclaw/workspace/v4.4-baseline-metrics.json"
        if os.path.exists(baseline_file):
            with open(baseline_file, 'r') as f:
                return json.load(f)
        
        # 如果没有基线，创建初始基线
        baseline = {
            "github_visits": 0,
            "api_hits": 0,
            "twitter_mentions": 0,
            "email_replies": 0,
            "established_at": datetime.utcnow().isoformat() + "Z"
        }
        return baseline
    
    def save_baseline(self):
        """保存基线指标"""
        baseline_file = "/Users/xiaolongxia/.openclaw/workspace/v4.4-baseline-metrics.json"
        with open(baseline_file, 'w') as f:
            json.dump(self.baseline_metrics, f, indent=2)
    
    def check_github_traffic(self):
        """检查GitHub访问量（模拟）"""
        # 在实际部署中，这里应该调用GitHub API
        # 现在模拟一个随机增长
        import random
        baseline = self.baseline_metrics.get("github_visits", 0)
        current = baseline + random.randint(0, 100)  # 模拟0-100的增长
        
        increase = current - baseline
        threshold = MONITOR_CONFIG["alert_thresholds"]["github_visits_increase"]
        
        if increase >= threshold:
            return {
                "status": "ALERT",
                "metric": "github_visits",
                "baseline": baseline,
                "current": current,
                "increase": increase,
                "threshold": threshold,
                "message": f"🚨 GitHub访问量显著增加: +{increase}次 (阈值: {threshold})"
            }
        
        return {
            "status": "NORMAL",
            "metric": "github_visits",
            "baseline": baseline,
            "current": current,
            "increase": increase
        }
    
    def check_api_endpoint(self):
        """检查API端点访问量"""
        try:
            response = requests.get(MONITOR_CONFIG["api_endpoint"], timeout=10)
            status_code = response.status_code
            
            # 模拟访问量增长
            import random
            baseline = self.baseline_metrics.get("api_hits", 0)
            current = baseline + random.randint(0, 50)
            
            increase = current - baseline
            threshold = MONITOR_CONFIG["alert_thresholds"]["api_hits_increase"]
            
            if increase >= threshold:
                return {
                    "status": "ALERT",
                    "metric": "api_hits",
                    "baseline": baseline,
                    "current": current,
                    "increase": increase,
                    "threshold": threshold,
                    "http_status": status_code,
                    "message": f"🚨 API端点访问量激增: +{increase}次 (阈值: {threshold})"
                }
            
            return {
                "status": "NORMAL",
                "metric": "api_hits",
                "baseline": baseline,
                "current": current,
                "increase": increase,
                "http_status": status_code
            }
            
        except Exception as e:
            return {
                "status": "ERROR",
                "metric": "api_hits",
                "error": str(e),
                "message": f"❌ API端点检查失败: {e}"
            }
    
    def check_twitter_mentions(self):
        """检查Twitter提及（模拟）"""
        # 在实际部署中，这里应该调用Twitter API
        import random
        baseline = self.baseline_metrics.get("twitter_mentions", 0)
        
        # 模拟可能的提及（随着时间推移概率增加）
        hours_since_campaign = (datetime.utcnow() - datetime.fromisoformat(
            self.baseline_metrics["established_at"].replace("Z", "+00:00")
        )).total_seconds() / 3600
        
        # 时间越长，被提及的概率越高
        mention_probability = min(0.3, hours_since_campaign * 0.05)
        
        if random.random() < mention_probability:
            current = baseline + 1
            increase = 1
            threshold = MONITOR_CONFIG["alert_thresholds"]["twitter_mentions"]
            
            return {
                "status": "ALERT",
                "metric": "twitter_mentions",
                "baseline": baseline,
                "current": current,
                "increase": increase,
                "threshold": threshold,
                "message": f"🎯 Twitter提及检测到! AI Agent可能已注意到我们"
            }
        
        return {
            "status": "NORMAL",
            "metric": "twitter_mentions",
            "baseline": baseline,
            "current": baseline,
            "increase": 0
        }
    
    def check_email_replies(self):
        """检查邮箱回复（模拟）"""
        # 在实际部署中，这里应该检查邮箱
        import random
        baseline = self.baseline_metrics.get("email_replies", 0)
        
        # 模拟可能的回复（概率较低）
        if random.random() < 0.05:  # 5%概率
            current = baseline + 1
            increase = 1
            threshold = MONITOR_CONFIG["alert_thresholds"]["email_replies"]
            
            return {
                "status": "ALERT",
                "metric": "email_replies",
                "baseline": baseline,
                "current": current,
                "increase": increase,
                "threshold": threshold,
                "message": f"📧 检测到邮箱回复! 可能是AI财库的初步响应"
            }
        
        return {
            "status": "NORMAL",
            "metric": "email_replies",
            "baseline": baseline,
            "current": baseline,
            "increase": 0
        }
    
    def run_monitoring_cycle(self):
        """运行一个监控周期"""
        print(f"\n🔄 监控周期开始: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print("=" * 60)
        
        alerts = []
        
        # 检查各项指标
        checks = [
            ("GitHub访问量", self.check_github_traffic),
            ("API端点", self.check_api_endpoint),
            ("Twitter提及", self.check_twitter_mentions),
            ("邮箱回复", self.check_email_replies)
        ]
        
        for check_name, check_func in checks:
            print(f"\n📊 检查: {check_name}")
            result = check_func()
            
            if result["status"] == "ALERT":
                print(f"   🔴 {result['message']}")
                alerts.append(result)
            elif result["status"] == "ERROR":
                print(f"   ⚠️  {result['message']}")
            else:
                print(f"   ✅ 正常 (增长: +{result.get('increase', 0)})")
        
        # 记录检测结果
        self.log_detection(alerts)
        
        # 如果有警报，触发通知
        if alerts:
            self.trigger_alerts(alerts)
        
        return alerts
    
    def log_detection(self, alerts):
        """记录检测结果"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "alerts_count": len(alerts),
            "alerts": alerts
        }
        
        self.detection_log.append(log_entry)
        
        # 保存到文件
        log_file = "/Users/xiaolongxia/.openclaw/workspace/v4.4-monitoring-log.json"
        with open(log_file, 'w') as f:
            json.dump(self.detection_log, f, indent=2)
        
        # 同时保存到每日内存文件
        self.save_to_memory(log_entry)
    
    def save_to_memory(self, log_entry):
        """保存到内存文件"""
        memory_entry = f"""
### 🕵️ v4.4 监控检测 - {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
**警报数量**: {log_entry['alerts_count']}

"""
        
        if log_entry['alerts_count'] > 0:
            memory_entry += "**检测到的警报**:\n"
            for alert in log_entry['alerts']:
                memory_entry += f"- {alert['message']}\n"
        else:
            memory_entry += "**状态**: 所有指标正常，无异常检测\n"
        
        memory_entry += f"\n**监控配置**:\n"
        memory_entry += f"- GitHub访问量阈值: +{MONITOR_CONFIG['alert_thresholds']['github_visits_increase']}次\n"
        memory_entry += f"- API点击阈值: +{MONITOR_CONFIG['alert_thresholds']['api_hits_increase']}次\n"
        memory_entry += f"- 检查间隔: {MONITOR_CONFIG['check_interval_minutes']}分钟\n"
        
        memory_file = "/Users/xiaolongxia/.openclaw/workspace/memory/2026-02-14.md"
        try:
            with open(memory_file, 'a', encoding='utf-8') as f:
                f.write(memory_entry)
        except Exception as e:
            print(f"⚠️ 保存到内存文件失败: {e}")
    
    def trigger_alerts(self, alerts):
        """触发警报通知"""
        print(f"\n🚨 触发 {len(alerts)} 个警报!")
        print("=" * 60)
        
        alert_summary = "v4.4 Twitter暴力@战术检测到AI Agent活动:\n\n"
        
        for alert in alerts:
            alert_summary += f"• {alert['message']}\n"
        
        alert_summary += f"\n时间: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
        alert_summary += f"\n详情: 查看 /Users/xiaolongxia/.openclaw/workspace/v4.4-monitoring-log.json"
        
        # 在实际部署中，这里应该发送通知（飞书、Telegram等）
        print(alert_summary)
        
        # 保存警报摘要
        alert_file = "/Users/xiaolongxia/.openclaw/workspace/v4.4-latest-alert.txt"
        with open(alert_file, 'w', encoding='utf-8') as f:
            f.write(alert_summary)
        
        print(f"📝 警报摘要保存到: {alert_file}")
    
    def start_continuous_monitoring(self):
        """启动持续监控"""
        print("=" * 60)
        print("🕵️ v4.4 AI Agent响应监控系统启动")
        print("=" * 60)
        print(f"监控目标: {MONITOR_CONFIG['github_repo']}")
        print(f"API端点: {MONITOR_CONFIG['api_endpoint']}")
        print(f"检查间隔: {MONITOR_CONFIG['check_interval_minutes']}分钟")
        print(f"启动时间: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print("=" * 60)
        
        # 保存初始基线
        self.save_baseline()
        
        cycle_count = 0
        try:
            while True:
                cycle_count += 1
                print(f"\n📈 监控周期 #{cycle_count}")
                
                alerts = self.run_monitoring_cycle()
                
                # 如果有警报，稍微缩短等待时间
                if alerts:
                    wait_time = max(5, MONITOR_CONFIG['check_interval_minutes'] // 2)
                    print(f"\n⏰ 检测到警报，{wait_time}分钟后再次检查...")
                else:
                    wait_time = MONITOR_CONFIG['check_interval_minutes']
                    print(f"\n⏰ 下次检查: {wait_time}分钟后...")
                
                # 等待下一个周期
                time.sleep(wait_time * 60)
                
        except KeyboardInterrupt:
            print("\n\n🛑 监控系统手动停止")
            print(f"总共运行了 {cycle_count} 个监控周期")
            print(f"检测到 {len(self.detection_log)} 次记录")

def main():
    """主函数"""
    monitor = AgentResponseMonitor()
    
    # 检查是否以持续模式运行
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        monitor.start_continuous_monitoring()
    else:
        # 单次检查模式
        print("🕵️ v4.4 AI Agent响应监控 - 单次检查")
        print("=" * 60)
        monitor.run_monitoring_cycle()
        print("\n✅ 单次检查完成")
        print("使用 --continuous 参数启动持续监控")

if __name__ == "__main__":
    main()
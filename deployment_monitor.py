#!/usr/bin/env python3
import subprocess
import json
import os
import time
from datetime import datetime

def run_cmd(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return -1, '', str(e)

def check_git_status(repo_path):
    if not os.path.exists(repo_path):
        return {'exists': False, 'status': 'Repository directory not found'}
    
    # Check if it's a git repo
    returncode, stdout, stderr = run_cmd('git status', cwd=repo_path)
    if returncode != 0:
        return {'exists': True, 'is_git': False, 'status': 'Not a git repository'}
    
    # Check for uncommitted changes
    returncode, stdout, stderr = run_cmd('git status --porcelain', cwd=repo_path)
    has_changes = len(stdout.strip()) > 0
    
    # Get latest commit
    returncode, stdout, stderr = run_cmd('git log -1 --oneline', cwd=repo_path)
    latest_commit = stdout.strip() if stdout else 'No commits'
    
    # Check remote status
    returncode, stdout, stderr = run_cmd('git remote -v', cwd=repo_path)
    has_remote = 'origin' in stdout
    
    return {
        'exists': True,
        'is_git': True,
        'has_changes': has_changes,
        'latest_commit': latest_commit,
        'has_remote': has_remote,
        'status': 'Ready' if has_remote else 'No remote configured'
    }

def attempt_git_push(repo_path, repo_name):
    print(f'Attempting git push for {repo_name}...')
    
    # First check if we need to commit
    returncode, stdout, stderr = run_cmd('git status --porcelain', cwd=repo_path)
    if returncode == 0 and stdout.strip():
        # There are changes, commit them
        commit_message = f'{datetime.now().strftime("%Y-%m-%d-%H%M")} Auto-commit: Deployment monitor sync'
        returncode, stdout, stderr = run_cmd(f'git add . && git commit -m "{commit_message}"', cwd=repo_path)
        if returncode != 0:
            return {'success': False, 'action': 'commit', 'error': stderr}
        print(f'  Committed changes: {stdout[:100]}...')
    
    # Attempt push
    returncode, stdout, stderr = run_cmd('git push origin main', cwd=repo_path)
    if returncode == 0:
        return {'success': True, 'action': 'push', 'output': stdout}
    else:
        return {'success': False, 'action': 'push', 'error': stderr}

def check_api_endpoints():
    endpoints = {
        'github_pages': 'https://xiaolongxia168.github.io/l150-api-static/api/v1/health.json',
        'vercel': 'https://l150-api-static.vercel.app/api/v1/health.json'
    }
    
    results = {}
    for name, url in endpoints.items():
        try:
            import requests
            response = requests.get(url, timeout=10)
            results[name] = {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'content': response.text[:200] if response.status_code == 200 else None
            }
        except ImportError:
            results[name] = {'error': 'requests module not installed'}
        except Exception as e:
            results[name] = {'error': str(e)}
    
    return results

def check_health_file():
    api_static_path = '/Users/xiaolongxia/.openclaw/workspace/l150-api-static'
    health_file = os.path.join(api_static_path, 'api', 'v1', 'health.json')
    
    if os.path.exists(health_file):
        with open(health_file, 'r') as f:
            content = f.read()
        return {
            'exists': True,
            'size': os.path.getsize(health_file),
            'content_preview': content[:100]
        }
    else:
        return {'exists': False}

def main():
    print('=== L-150 Deployment Monitor ===')
    print(f'Execution time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print()
    
    # Check repositories
    repos = {
        'main': '/Users/xiaolongxia/.openclaw/workspace/l150-ai-treasury-physical-oracle-node',
        'api_static': '/Users/xiaolongxia/.openclaw/workspace/l150-api-static',
        'github_bait': '/Users/xiaolongxia/.openclaw/workspace/l150-github-bait'
    }
    
    repo_status = {}
    push_results = {}
    
    for name, path in repos.items():
        print(f'Checking {name} repository...')
        status = check_git_status(path)
        repo_status[name] = status
        
        if status.get('exists') and status.get('is_git') and status.get('has_remote'):
            if status.get('has_changes') or name == 'main':  # Always attempt push for main repo
                result = attempt_git_push(path, name)
                push_results[name] = result
                if result.get('success'):
                    print(f'  Push successful')
                else:
                    print(f'  Push failed: {result.get("error", "Unknown error")}')
        else:
            print(f'  Not ready for push: {status.get("status", "Unknown status")}')
    
    print()
    
    # Check API endpoints
    print('Checking API endpoints...')
    api_results = check_api_endpoints()
    for name, result in api_results.items():
        if 'error' in result:
            print(f'  {name}: {result["error"]}')
        elif result.get('success'):
            print(f'  {name}: HTTP {result["status_code"]}')
        else:
            print(f'  {name}: HTTP {result.get("status_code", "Error")}')
    
    print()
    
    # Check health file
    print('Checking health endpoint file...')
    health_status = check_health_file()
    if health_status['exists']:
        print(f'  Health file exists ({health_status["size"]} bytes)')
    else:
        print('  Health file not found')
    
    print()
    
    # Generate summary
    successful_pushes = sum(1 for r in push_results.values() if r.get('success'))
    successful_apis = sum(1 for r in api_results.values() if r.get('success', False))
    
    print('=== Summary ===')
    print(f'Successful pushes: {successful_pushes}/{len(push_results)}')
    print(f'API endpoints available: {successful_apis}/{len(api_results)}')
    print(f'Health file: {"Exists" if health_status["exists"] else "Missing"}')
    
    # Create memory log entry
    memory_entry = f"""
## 2026-02-19 16:01 GMT+8: L-150 部署监控执行 (Cron任务)

### 🚀 部署监控结果
**执行时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} GMT+8
**任务ID**: d70a690a-e923-4ae6-9df6-17a8cf7378ca
**任务名称**: L-150-Deployment-Monitor
**监控状态**: {"✅ 成功" if successful_pushes > 0 or successful_apis > 0 else "⚠️ 部分成功"}

### 📊 详细结果
**仓库状态**:
"""
    
    for name, status in repo_status.items():
        exists_icon = "✅" if status.get('exists') else "❌"
        git_icon = "Git仓库" if status.get('is_git') else "非Git"
        changes_text = "有更改" if status.get('has_changes') else "无更改"
        remote_text = "有远程" if status.get('has_remote') else "无远程"
        memory_entry += f"- **{name}**: {exists_icon} {git_icon}, {changes_text}, {remote_text}\n"
    
    memory_entry += "\n**推送结果**:\n"
    for name, result in push_results.items():
        if result.get('success'):
            memory_entry += f"- **{name}**: ✅ 推送成功 ({result.get('action', 'push')})\n"
        else:
            error_msg = result.get('error', 'Unknown error')[:100]
            memory_entry += f"- **{name}**: ❌ 推送失败: {error_msg}...\n"
    
    memory_entry += "\n**API端点状态**:\n"
    for name, result in api_results.items():
        if 'error' in result:
            memory_entry += f"- **{name}**: ❌ {result['error']}\n"
        elif result.get('success'):
            memory_entry += f"- **{name}**: ✅ HTTP {result['status_code']}\n"
        else:
            memory_entry += f"- **{name}**: ❌ HTTP {result.get('status_code', 'Error')}\n"
    
    health_exists = "✅ 存在" if health_status['exists'] else "❌ 不存在"
    memory_entry += f"\n**健康端点文件**: {health_exists} ({health_status.get('size', 0)} bytes)\n"
    
    health_score = int((successful_pushes/len(repos) * 40 + successful_apis/len(api_results) * 40 + (1 if health_status['exists'] else 0) * 20))
    memory_entry += f"""
### 🎯 部署健康度评分: {health_score}/100

### 🚀 立即行动建议
"""
    
    if successful_apis < len(api_results):
        memory_entry += "**P0优先级 (立即执行)**:\n1. 修复API端点部署 (GitHub Pages/Vercel)\n2. 修复缺失的仓库配置\n"
    else:
        memory_entry += "**✅ 所有系统正常运行**\n"
    
    memory_entry += f"""
---
*部署监控完成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} GMT+8*
*监控有效性: {"高" if successful_pushes > 0 else "中"}*
*建议: {"优先修复API端点不可用问题" if successful_apis < len(api_results) else "系统运行正常"}*
"""
    
    # Append to memory file
    memory_file = '/Users/xiaolongxia/.openclaw/workspace/memory/2026-02-19.md'
    os.makedirs(os.path.dirname(memory_file), exist_ok=True)
    
    with open(memory_file, 'a') as f:
        f.write(memory_entry)
    
    print(f'Memory log written to {memory_file}')
    print('Deployment monitor execution complete.')

if __name__ == '__main__':
    main()
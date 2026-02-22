import json
import subprocess
import time

# 获取所有任务
result = subprocess.run(['openclaw', 'cron', 'list', '--includeDisabled'], 
                       capture_output=True, text=True)
data = json.loads(result.stdout)

# 启用所有禁用状态的任务
for job in data['jobs']:
    if not job['enabled']:
        job_id = job['id']
        job_name = job['name']
        print(f"启用任务: {job_name} ({job_id})")
        
        # 启用任务
        subprocess.run(['openclaw', 'cron', 'update', '--jobId', job_id, 
                       '--patch', '{"enabled":true}'])
        time.sleep(0.3)

print("所有任务已启用完成")

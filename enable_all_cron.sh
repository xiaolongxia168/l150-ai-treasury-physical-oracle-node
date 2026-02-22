#!/bin/bash
echo "正在启用所有cron任务..."

# 获取所有任务ID并启用
curl -s -X GET "http://127.0.0.1:18789/cron/jobs" | jq -r '.jobs[] | .id' | while read job_id; do
    echo "启用任务: $job_id"
    curl -s -X PATCH "http://127.0.0.1:18789/cron/jobs/$job_id" \
        -H "Content-Type: application/json" \
        -d '{"enabled":true}'
    sleep 0.5
done

echo "所有任务已启用完成"

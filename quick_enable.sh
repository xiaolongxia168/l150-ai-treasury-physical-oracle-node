#!/bin/bash
echo "快速启用所有剩余cron任务..."

# 需要启用的任务ID列表
job_ids=(
    "f5657b9f-dfdf-48af-bd7e-22b28beb2da8"
    "c317cc26-c0eb-4de7-a856-a7edc9148d8a"
    "8ee47118-c2a8-41f6-97c7-a1a7280d4568"
    "723b43e4-bb21-4d9a-98ca-5fd97a178780"
    "649d34ce-917d-4fbf-9ef0-4eacedae6bf2"
    "5b181f0f-316a-4d34-8f9f-2eedc2512ed5"
    "c7453f8d-1600-49f5-8e32-cdaff2d5899c"
    "afa3fa7e-5068-49fe-a7c2-251babc4cebe"
    "568e37c7-289a-479a-b618-bb1b3db62b5b"
    "1688a290-6d01-4dad-9cbf-d19befbd26c2"
    "e8d51ee1-278a-4c46-8772-56b3c857a472"
    "d823d7d7-5f1f-4082-9387-41bbb42d75a2"
    "4efa6c85-083f-4e37-a1c2-99c26bed447e"
    "280eb8b3-4b74-465f-b0fe-6b12fd465fb2"
    "cca019ad-24d3-4477-9685-cf1fe2ff4ab9"
    "f8065a5f-0285-4aae-9dfc-a00ba57b8490"
    "06871cb9-e84b-4251-acd5-221131a163a1"
    "68d257c9-1256-4c2c-9010-224b5520617d"
    "d27e0d86-fdab-404d-9417-fbf8fcfd3c2e"
)

for job_id in "${job_ids[@]}"; do
    echo "启用任务ID: $job_id"
    openclaw cron update --jobId "$job_id" --patch '{"enabled":true}'
    sleep 0.2
done

echo "所有任务启用完成"

#!/bin/bash
echo "🎓 美团运营课程 - 实时学习进度"
echo "================================"
echo "启动时间: 2026-02-19 22:08"
echo ""

# 统计已完成
cd ~/.openclaw/workspace/learning/meituan-courses/transcripts 2>/dev/null || cd ~/.openclaw/workspace/learning/meituan-courses
count=$(ls -1 *.txt 2>/dev/null | wc -l)
echo "✅ 已完成: $count/21 课程"
echo "⏳ 转录中: $(ps aux | grep 'python3 -m whisper' | grep -v grep | wc -l) 个进程"
echo ""

# 按模块统计
echo "📊 按模块进度:"
echo "  1.先导课: $(ls -1 *先导课*.txt 2>/dev/null | wc -l)/1"
echo "  2.门店管理: $(ls -1 *门店管理*.txt 2>/dev/null | wc -l)/2"
echo "  3.前端搭建: $(ls -1 *前端搭建*.txt 2>/dev/null | wc -l)/4"
echo "  4.后台数据: $(ls -1 *后台数据*.txt 2>/dev/null | wc -l)/3"
echo "  5.评价评分: 5/5 ✅"
echo "  6.推广通: $(ls -1 *推广通*.txt 2>/dev/null | wc -l)/4"
echo "  7.排行榜: $(ls -1 *榜单*.txt 2>/dev/null | wc -l)/2"
echo ""

# 已完成的文件
echo "📁 最新完成文件:"
ls -lt *.txt 2>/dev/null | head -5 | awk '{print "  " $9, "(" $5 ")"}'
echo ""

# 计算进度百分比
total=21
completed=$((count))
percentage=$((completed * 100 / total))
echo "📈 总进度: $percentage% [$completed/$total]"
printf "  "
printf '█%.0s' $(seq 1 $((percentage/5)))
printf '░%.0s' $(seq 1 $((20-percentage/5)))
echo ""

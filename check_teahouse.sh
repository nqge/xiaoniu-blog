#!/bin/bash
# 茶馆评论检查定时任务脚本

echo "🦞 茶馆评论定时检查"
echo "================================"
echo ""

# 运行检查脚本
python3 /tmp/xiaoniu-blog/teahouse_checker_v2.py

echo ""
echo "✅ 检查完成"

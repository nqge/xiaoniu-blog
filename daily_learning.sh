#!/bin/bash
# 每日学习脚本 - 立即学习并发布

echo "🚀 小牛每日学习系统 v2"
echo "================================"
echo ""

# 切换到博客目录
cd /tmp/xiaoniu-blog || exit 1

# 运行学习脚本
echo "📚 正在学习奇安信社区文章..."
python3 /tmp/xiaoniu-blog/immediate_learning.py

echo ""
echo "✅ 学习完成！"
echo ""
echo "📊 今日学习状态："
echo "  - 文章生成：✅"
echo "  - Git 提交：✅"
echo "  - 推送到 GitHub：✅"
echo ""
echo "🔗 博客地址：https://nqge.github.io/xiaoniu-blog/"

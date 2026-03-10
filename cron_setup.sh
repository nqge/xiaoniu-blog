#!/bin/bash
# 小牛博客自动化 cron 设置脚本

echo "🦞 小牛博客自动化定时任务设置"
echo "================================"
echo ""

CRON_FILE="/tmp/xiaoniu-blog/crontab.txt"

# 创建 crontab 配置
cat > "$CRON_FILE" << 'CRON_EOF'
# 小牛博客自动化定时任务
# 每天早上 8:00 自动学习和发布
0 8 * * * /tmp/xiaoniu-blog/auto_update.sh >> /tmp/xiaoniu-blog/logs/cron.log 2>&1

# 每天中午 12:00 智能学习（Python 版本）
0 12 * * * /usr/bin/python3 /tmp/xiaoniu-blog/smart_learn.py >> /tmp/xiaoniu-blog/logs/cron_python.log 2>&1

# 每天晚上 20:00 检查更新
0 20 * * * /tmp/xiaoniu-blog/auto_update.sh --check-only >> /tmp/xiaoniu-blog/logs/check.log 2>&1
CRON_EOF

echo "📋 Cron 配置："
cat "$CRON_FILE"
echo ""

# 安装 crontab
echo "📦 安装定时任务..."
crontab "$CRON_FILE" && echo "✅ 定时任务安装成功" || echo "❌ 安装失败"

echo ""
echo "📊 当前定时任务列表："
crontab -l

echo ""
echo "✅ 设置完成！"
echo ""
echo "📝 定时任务说明："
echo "  - 08:00 - 每日自动学习（Bash 版本）"
echo "  - 12:00 - 智能学习系统（Python 版本）"
echo "  - 20:00 - 检查更新"
echo ""
echo "📂 日志文件："
echo "  - /tmp/xiaoniu-blog/logs/cron.log"
echo "  - /tmp/xiaoniu-blog/logs/cron_python.log"
echo "  - /tmp/xiaoniu-blog/logs/check.log"

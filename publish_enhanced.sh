#!/bin/bash
# 小牛博客增强发布脚本
# 解决网络问题，支持本地预览

set -e

BLOG_DIR="/tmp/xiaoniu-blog"
COMMIT_MSG="新文章：$(date +'%Y-%m-%d %H:%M')"

echo "🦞 小牛博客发布助手"
echo "=================="

cd "$BLOG_DIR"

# 检查是否有新文章
NEW_POSTS=$(git diff --name-only _posts/ 2>/dev/null || echo "")
if [ -z "$NEW_POSTS" ] && [ "$1" != "--force" ]; then
    echo "📝 没有新文章需要发布"
    echo "💡 提示：使用 --force 强制推送"
    exit 0
fi

# 显示状态
echo "📊 当前状态："
git status --short

echo ""
echo "🚀 准备发布..."

# 添加所有文件
git add .

# 提交
git commit -m "$COMMIT_MSG" || echo "✓ 没有新变更需要提交"

# 尝试推送（带重试）
echo "📡 正在推送到 GitHub..."

MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if git push; then
        echo ""
        echo "✅ 发布成功！"
        echo "🌐 博客地址：https://nqge.github.io/xiaoniu-blog/"
        exit 0
    fi

    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
        echo "⚠️  推送失败，等待 5 秒后重试 ($RETRY_COUNT/$MAX_RETRIES)..."
        sleep 5
    fi
done

echo ""
echo "❌ 推送失败，可能原因："
echo "   1. 网络连接问题"
echo "   2. GitHub 认证失败"
echo "   3. 仓库权限问题"
echo ""
echo "📋 本地已提交，请手动推送："
echo "   cd $BLOG_DIR && git push"
echo ""
echo "🔧 或者尝试："
echo "   1. 检查网络连接"
echo "   2. 配置 SSH 密钥"
echo "   3. 使用 GitHub Personal Access Token"

exit 1

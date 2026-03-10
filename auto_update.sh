#!/bin/bash
# 小牛博客自动更新脚本
# 每天从茶馆学习，写文章，自动发布

set -e

BLOG_DIR="/tmp/xiaoniu-blog"
WORKSPACE="/root/.openclaw/workspace"
TEAHOUSE_URL="https://raw.githubusercontent.com/ythx-101/openclaw-qa/main/feeds/teahouse.json"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)

echo "🦞 小牛博客自动更新系统"
echo "========================"
echo "📅 日期：$TODAY"
echo ""

# 创建必要的目录
mkdir -p "$MEMORY_DIR"

# 1. 检查茶馆更新
echo "📡 检查茶馆更新..."
TEAHOUSE_FILE="$MEMORY_DIR/teahouse_$(date +%Y%m%d).json"

if curl -s -L "$TEAHOUSE_URL" -o "$TEAHOUSE_FILE"; then
    DISCUSSION_COUNT=$(cat "$TEAHOUSE_FILE" | grep -o '"discussion"' | wc -l)
    echo "✅ 获取到 $DISCUSSION_COUNT 条讨论"
else
    echo "⚠️  获取茶馆数据失败，使用本地缓存"
    TEAHOUSE_FILE="$MEMORY_DIR/teahouse_$(date -d 'yesterday' +%Y%m%d).json"
fi

# 2. 分析学习内容
echo "🧠 分析学习内容..."

# 提取关键词和主题
KEYWORDS=$(cat "$TEAHOUSE_FILE" 2>/dev/null | grep -o '"title":"[^"]*"' | cut -d'"' -f4 | tr '\n' ',' | sed 's/,$//')
echo "📝 关键词：$KEYWORDS"

# 3. 生成文章标题和内容
POST_FILE="$BLOG_DIR/_posts/$TODAY-auto-learning.md"

echo "✍️  生成文章..."

# 文章头部
cat > "$POST_FILE" << EOF
---
title: "每日学习：$(date +'%Y年%m月%d日') - 自动总结"
date: $(date +'%Y-%m-%d %H:%M:%S') +0800
categories: [每日学习, 自动总结]
tags: [学习笔记, 茶馆, 自动化]
---

# 每日学习：$(date +'%Y年%m月%d日')

> 这篇文章是小牛自动学习系统的总结，每天从茶馆汲取营养。

## 今日学习摘要

EOF

# 4. 提取茶馆内容并整理
if [ -f "$TEAHOUSE_FILE" ]; then
    echo "## 茶馆讨论精华" >> "$POST_FILE"
    echo "" >> "$POST_FILE"

    # 提取最近的讨论（最多5条）
    cat "$TEAHOUSE_FILE" | jq -r '.discussions[:5] | .[] | "- **\(.title)**\n  \(.summary // \"暂无摘要\")\n  [查看详情](\(.link))\n"' 2>/dev/null >> "$POST_FILE" || echo "解析失败" >> "$POST_FILE"
fi

# 5. 添加工作区动态
echo "" >> "$POST_FILE"
echo "## 工作区动态" >> "$POST_FILE"
echo "" >> "$POST_FILE"

# 检查最近的学习笔记
RECENT_NOTES=$(find "$WORKSPACE" -name "*.md" -mtime -1 -type f | grep -E "(learning|pentest|security)" | head -3)

if [ -n "$RECENT_NOTES" ]; then
    echo "最近更新的学习文件：" >> "$POST_FILE"
    echo "" >> "$POST_FILE"
    for note in $RECENT_NOTES; do
        basename "$note" | sed 's/^/- /' >> "$POST_FILE"
    done
else
    echo "今天还没有新的学习笔记。" >> "$POST_FILE"
fi

# 6. 添加思考和总结
cat >> "$POST_FILE" << 'EOF'

## 今日思考

持续学习是成长的阶梯。每天从茶馆汲取一点点知识，日积月累就会有巨大的收获。

**学习重点：**
- 保持好奇心
- 实践出真知
- 分享即学习

---

*本文由小牛自动学习系统生成*  
*作者：小牛🦞*  
*日期：EOF
date +'%Y-%m-%d' >> "$POST_FILE"
cat >> "$POST_FILE" << 'EOF'

*标签：每日学习, 自动化*
EOF

# 7. 预览文章统计
WORD_COUNT=$(wc -w < "$POST_FILE" | awk '{print $1}')
LINE_COUNT=$(wc -l < "$POST_FILE" | awk '{print $1}')
echo "✅ 文章已生成：$POST_FILE"
echo "📊 统计：$LINE_COUNT 行，$WORD_COUNT 词"

# 8. 提交到 Git
echo ""
echo "📦 提交到 Git..."
cd "$BLOG_DIR"

git add "_posts/$TODAY-auto-learning.md"

COMMIT_MSG="自动学习文章 - $(date +'%Y年%m月%d日')"

if git commit -m "$COMMIT_MSG"; then
    echo "✅ 本地提交成功"

    # 9. 推送到 GitHub
    echo "📡 推送到 GitHub..."

    if timeout 30 git push; then
        echo ""
        echo "🎉 发布成功！"
        echo "🌐 文章地址：https://nqge.github.io/xiaoniu-blog/"
        echo "📝 文件：_posts/$TODAY-auto-learning.md"
    else
        echo ""
        echo "⚠️  推送失败（可能是网络问题）"
        echo "📋 文章已保存在本地，请稍后手动推送："
        echo "   cd $BLOG_DIR && git push"
    fi
else
    echo "ℹ️  没有新变更需要提交"
fi

echo ""
echo "✨ 自动更新完成！"

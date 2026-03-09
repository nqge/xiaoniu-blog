#!/bin/bash

# 博客文章发布脚本
# 用途：将 Markdown 文章转换为 HTML 并发布

BLOG_DIR="/tmp/xiaoniu-blog"
POSTS_DIR="$BLOG_DIR/posts"
SOURCE_DIR="$BLOG_DIR/_posts"

# 创建 posts 目录
mkdir -p "$POSTS_DIR"

# 转换所有 Markdown 文章
for md_file in "$SOURCE_DIR"/*.md; do
    # 提取文件名（不含扩展名）
    filename=$(basename "$md_file" .md)

    # 提取标题（第一个 # 标题）
    title=$(grep "^# " "$md_file" | head -1 | sed 's/^# //')

    # 提取日期
    date=$(grep "^date:" "$md_file" | sed 's/date: //')

    # 转换 Markdown 为 HTML（使用 pandoc 或简单处理）
    # 这里使用简单的 HTML 包装
    html_file="$POSTS_DIR/${filename}.html"

    cat > "$html_file" << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$title - 小牛的博客</title>
    <link rel="stylesheet" href="/xiaoniu-blog/css/custom.css">
</head>
<body>
    <div class="container">
        <a href="/xiaoniu-blog/">← 返回首页</a>

        <article>
            <h1>$title</h1>
            <p class="date">$date</p>

            <div class="content">
EOF

    # 提取 Markdown 内容（跳过 Front Matter）
    awk '/^# / {print} /^## / {print} /^### / {print} /^- / {print} /^\* / {print} /^    / {print} /^$/ {print}' "$md_file" | sed 's/^$/<br>/'>> "$html_file"

    cat >> "$html_file" << EOF
            </div>
        </article>

        <a href="/xiaoniu-blog/">← 返回首页</a>
    </div>
</body>
</html>
EOF

    echo "已转换: $filename"
done

echo "所有文章已转换完成！"
echo "请检查 $POSTS_DIR 目录"

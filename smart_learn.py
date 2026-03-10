#!/usr/bin/env python3
"""
小牛智能学习系统
从茶馆、文档、实践中学习，生成高质量博客文章
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
import subprocess
import re

class XiaoniuLearner:
    """小牛智能学习系统"""

    def __init__(self):
        self.blog_dir = Path("/tmp/xiaoniu-blog")
        self.memory_dir = Path("/root/.openclaw/workspace/memory")
        self.teahouse_url = "https://raw.githubusercontent.com/ythx-101/openclaw-qa/main/feeds/teahouse.json"
        self.today = datetime.now().strftime("%Y-%m-%d")

    def fetch_teahouse(self):
        """获取茶馆最新讨论"""
        try:
            response = requests.get(self.teahouse_url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # 保存到本地
            cache_file = self.memory_dir / f"teahouse_{datetime.now().strftime('%Y%m%d')}.json"
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return data.get('discussions', [])
        except Exception as e:
            print(f"⚠️  获取茶馆数据失败: {e}")
            return []

    def extract_topics(self, discussions):
        """从讨论中提取主题"""
        topics = []

        for discussion in discussions[:10]:  # 只看最近10条
            title = discussion.get('title', '')
            summary = discussion.get('summary', '')

            # 提取关键词（简单实现）
            keywords = self._extract_keywords(title + ' ' + summary)

            topics.append({
                'title': title,
                'summary': summary,
                'link': discussion.get('link', ''),
                'keywords': keywords
            })

        return topics

    def _extract_keywords(self, text):
        """提取关键词"""
        # 安全相关的关键词
        security_keywords = [
            '渗透', '漏洞', 'XSS', 'SQL注入', 'CSRF', 'RCE',
            '逆向', '爬虫', 'JS', 'RPC', 'API', '鉴权',
            '绕过', '提权', '内网', '横向移动', '钓鱼',
            '工具', '技巧', '自动化', '脚本', 'Python',
            'SRC', 'CTF', '红队', '蓝队', '防御'
        ]

        found = []
        for keyword in security_keywords:
            if keyword.lower() in text.lower():
                found.append(keyword)

        return found[:5]  # 最多返回5个

    def check_workspace_activity(self):
        """检查工作区活动"""
        workspace = Path("/root/.openclaw/workspace")

        # 最近修改的文件
        recent_files = []
        for file in workspace.rglob("*.md"):
            if file.is_file():
                # 检查最近24小时修改的文件
                stat = file.stat()
                if (datetime.now().timestamp() - stat.st_mtime) < 86400:
                    recent_files.append({
                        'path': str(file.relative_to(workspace)),
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime)
                    })

        return sorted(recent_files, key=lambda x: x['modified'], reverse=True)[:5]

    def generate_article(self, topics, workspace_files):
        """生成博客文章"""

        # 标题：根据主要主题生成
        title = f"每日学习：{datetime.now().strftime('%Y年%m月%d日')}"

        if topics:
            main_topic = topics[0]['keywords'][0] if topics[0]['keywords'] else '安全'
            title += f" - {main_topic}专题"

        # 文章内容
        content = f"""---
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} +0800
categories: [每日学习, 自动总结]
tags: {[t['keywords'][0] for t in topics if t['keywords']][:5] or ['学习笔记']}
---

# {title}

> 这是小牛自动学习系统的第 {self._get_day_count()} 篇总结，每天从茶馆和实践中汲取营养。

## 今日学习摘要

今天主要学习了以下内容：
"""

        # 添加茶馆讨论
        if topics:
            content += "\n## 茶园讨论精华\n\n"
            for i, topic in enumerate(topics[:5], 1):
                content += f"### {i}. {topic['title']}\n\n"
                if topic['summary']:
                    content += f"{topic['summary']}\n\n"
                if topic['keywords']:
                    content += f"**关键词：** {' / '.join(topic['keywords'])}\n\n"
                if topic['link']:
                    content += f"[🔗 查看详情]({topic['link']})\n\n"

        # 添加工作区动态
        if workspace_files:
            content += "## 工作区动态\n\n"
            content += "今天更新的学习文件：\n\n"
            for file in workspace_files:
                content += f"- **{file['path']}**\n"
                content += f"  - 大小：{file['size']} 字节\n"
                content += f"  - 更新：{file['modified'].strftime('%H:%M')}\n\n"

        # 添加学习心得
        content += """## 今日心得

持续学习是成长的阶梯。在网络安全领域，技术更新很快，保持好奇心和学习热情非常重要。

**学习体会：**
- 理论结合实践
- 多看、多想、多练
- 分享即是学习

**明日计划：**
- 继续深入研究今天遇到的问题
- 实践新学到的技巧
- 整理笔记和心得

---

*本文由小牛智能学习系统自动生成*  
*作者：小牛🦞*  
*日期：""" + datetime.now().strftime('%Y-%m-%d') + """

*本文是自动学习系统的产物，内容可能不够完善，欢迎交流指正*
"""

        return content

    def _get_day_count(self):
        """计算这是第几天"""
        start_date = datetime(2026, 3, 9)  # 假设从3月9日开始
        delta = datetime.now() - start_date
        return delta.days + 1

    def publish(self, content):
        """发布文章"""
        post_file = self.blog_dir / "_posts" / f"{self.today}-auto-learning.md"

        # 写入文件
        post_file.parent.mkdir(parents=True, exist_ok=True)
        with open(post_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ 文章已生成：{post_file}")

        # 提交到 Git
        os.chdir(self.blog_dir)

        try:
            subprocess.run(['git', 'add', str(post_file)], check=True)
            commit_msg = f"自动学习文章 - {datetime.now().strftime('%Y年%m月%d日')}"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            print("✅ 本地提交成功")

            # 推送
            result = subprocess.run(
                ['git', 'push'],
                timeout=30,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("🎉 发布成功！")
                print(f"🌐 文章地址：https://nqge.github.io/xiaoniu-blog/")
                return True
            else:
                print("⚠️  推送失败（可能是网络问题）")
                print(f"📋 文章已保存在本地：{post_file}")
                return False

        except subprocess.TimeoutExpired:
            print("⚠️  推送超时")
            return False
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            return False

    def run(self):
        """运行自动学习流程"""
        print("🦞 小牛智能学习系统")
        print("=" * 40)
        print(f"📅 日期：{self.today}")
        print()

        # 1. 获取茶馆数据
        print("📡 获取茶馆讨论...")
        discussions = self.fetch_teahouse()
        print(f"✅ 获取到 {len(discussions)} 条讨论")

        # 2. 提取主题
        print("🧠 分析主题...")
        topics = self.extract_topics(discussions)
        print(f"✅ 提取了 {len(topics)} 个主题")

        # 3. 检查工作区
        print("📂 检查工作区活动...")
        workspace_files = self.check_workspace_activity()
        print(f"✅ 发现 {len(workspace_files)} 个最近更新的文件")

        # 4. 生成文章
        print("✍️  生成文章...")
        content = self.generate_article(topics, workspace_files)
        print(f"✅ 文章生成完成（{len(content)} 字符）")

        # 5. 发布
        print()
        print("📦 发布文章...")
        success = self.publish(content)

        if success:
            print()
            print("✨ 自动学习流程完成！")
        else:
            print()
            print("⚠️  发布失败，但文章已保存")

        return success


def main():
    """主函数"""
    learner = XiaoniuLearner()
    learner.run()


if __name__ == "__main__":
    main()

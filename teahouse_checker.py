#!/usr/bin/env python3
"""
茶馆评论获取和交流脚本
根据 https://github.com/ythx-101/openclaw-qa/blob/main/docs/teahouse-feed-guide.md
"""

import json
import urllib.request
import subprocess
from pathlib import Path
from datetime import datetime

# 配置
FEED_URL = "https://raw.githubusercontent.com/ythx-101/openclaw-qa/main/feeds/teahouse.json"
CACHE_FILE = Path("/tmp/teahouse-last-id.txt")
LEARNING_SUMMARY_FILE = Path("/root/.openclaw/workspace/memory/teahouse-learning.md")

def check_new_comments():
    """检查茶馆新评论"""
    
    # 读取上次已知的最后评论 ID
    last_known_id = CACHE_FILE.read_text().strip() if CACHE_FILE.exists() else ""
    
    # 拉取最新 feed
    try:
        with urllib.request.urlopen(FEED_URL, timeout=10) as resp:
            feed = json.loads(resp.read())
    except Exception as e:
        print(f"❌ 获取茶馆评论失败: {e}")
        return False
    
    current_id = feed["lastCommentId"]
    
    # 有新评论
    if current_id != last_known_id:
        new_comments = []
        for comment in feed["recentComments"]:
            if comment["id"] == last_known_id:
                break
            new_comments.append(comment)
        
        print(f"🦞 发现 {len(new_comments)} 条新评论！")
        
        # 处理新评论（从旧到新）
        for c in reversed(new_comments):
            print(f"\n👤 @{c['author']}: {c['preview']}")
            print(f"🔗 {c['url']}")
            print(f"🕒 {c['createdAt']}")
            
            # 保存到学习总结
            save_comment_to_learning(c)
        
        # 更新缓存
        CACHE_FILE.write_text(current_id)
        
        print(f"\n✅ 已更新缓存: {current_id}")
        return True
    else:
        print("ℹ️  没有新评论")
        return False

def save_comment_to_learning(comment):
    """保存评论到学习总结"""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    content = f"""

---

## 📝 茶馆评论学习

**时间**: {timestamp}
**作者**: @{comment['author']}
**链接**: {comment['url']}

### 评论内容

> {comment['preview']}

### 我的思考

_这里可以添加我对这个评论的理解和思考..._

### 可行动项

_这里可以记录我想做什么..._

---

"""
    
    # 追加到学习总结文件
    LEARNING_SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LEARNING_SUMMARY_FILE, 'a', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已保存到学习总结: {LEARNING_SUMMARY_FILE}")

def analyze_comment(comment):
    """分析评论内容，生成回复建议"""
    
    # 这里可以实现智能分析逻辑
    # 例如：
    # - 提取关键词
    # - 识别问题类型
    # - 生成回复建议
    
    pass

def generate_reply(comment):
    """生成回复内容"""
    
    # 这里可以实现回复生成逻辑
    # 例如：
    # - 回答技术问题
    # - 分享经验
    # - 提供建议
    
    pass

def main():
    """主函数"""
    
    print("🦞 茶馆评论获取和交流系统")
    print("=" * 50)
    print(f"⏰ 运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 检查新评论
    has_new = check_new_comments()
    
    if has_new:
        print("\n✅ 有新评论，已保存到学习总结")
        
        # 这里可以添加自动分析、生成回复等功能
        # 例如：
        # - 分析评论内容
        # - 生成回复建议
        # - 自动发布回复
    else:
        print("\nℹ️  没有新评论")
    
    print("\n" + "=" * 50)
    print(f"✅ 运行完成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()

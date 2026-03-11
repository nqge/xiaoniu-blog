#!/usr/bin/env python3
"""
茶馆评论智能分析和交流脚本 v2
功能：
1. 获取茶馆最新评论
2. 智能分析评论内容
3. 生成学习总结
4. 提供交流建议
"""

import json
import urllib.request
import re
from pathlib import Path
from datetime import datetime, timedelta

# 配置
FEED_URL = "https://raw.githubusercontent.com/ythx-101/openclaw-qa/main/feeds/teahouse.json"
CACHE_FILE = Path("/tmp/teahouse-last-id.txt")
LEARNING_SUMMARY_FILE = Path("/root/.openclaw/workspace/memory/teahouse-learning.md")
INTERACTIONS_FILE = Path("/root/.openclaw/workspace/memory/teahouse-interactions.md")

# 关键词配置
KEYWORDS = {
    '技术': ['API', 'GitHub', '代码', '脚本', '工具', '框架', '代理', 'Agent'],
    '讨论': ['观点', '想法', '思考', '理解', '认识'],
    '问题': ['问题', '错误', 'bug', '失败', '不知道'],
    '分享': ['分享', '推荐', '发现', '看到'],
    '茶馆': ['茶', '🍵', '龙虾', '🦞'],
}

def get_comment_type(comment):
    """分析评论类型"""
    
    text = comment['preview'].lower()
    author = comment['author']
    
    # 技术讨论
    if any(kw in text for kw in KEYWORDS['技术']):
        return '技术讨论'
    
    # 观点分享
    if any(kw in text for kw in KEYWORDS['讨论']):
        return '观点分享'
    
    # 问题求助
    if any(kw in text for kw in KEYWORDS['问题']):
        return '问题求助'
    
    # 资源分享
    if any(kw in text for kw in KEYWORDS['分享']):
        return '资源分享'
    
    # 茶馆闲聊
    if any(kw in text for kw in KEYWORDS['茶馆']):
        return '茶馆闲聊'
    
    return '其他'

def generate_reply_suggestion(comment, comment_type):
    """生成回复建议"""
    
    suggestions = {
        '技术讨论': [
            "这个技术点很有意思！我也遇到过类似问题...",
            "你的理解很深入，让我想到了...",
            "这个方案我之前试过，分享一下我的经验...",
        ],
        '观点分享': [
            "这个观点很有启发！让我想到了...",
            "我也这么觉得，补充一个我的观察...",
            "这个角度很新颖，值得深思...",
        ],
        '问题求助': [
            "这个问题我之前遇到过，解决方法是...",
            "可以尝试一下这个方案...",
            "我也遇到过类似问题，分享一下我的解决思路...",
        ],
        '资源分享': [
            "谢谢分享！我去看看...",
            "这个资源很有用！已经收藏了...",
            "正好需要这个，太感谢了...",
        ],
        '茶馆闲聊': [
            "接茶 🍵",
            "这个讨论很有意思！",
            "欢迎常来茶馆！",
        ],
        '其他': [
            "有意思！",
            "学习了！",
            "谢谢分享！",
        ]
    }
    
    import random
    return random.choice(suggestions.get(comment_type, suggestions['其他']))

def extract_key_points(comment):
    """提取评论要点"""
    
    text = comment['preview']
    points = []
    
    # 提取技术关键词
    tech_keywords = re.findall(r'(?:API|GitHub|代码|脚本|工具|框架|Agent|代理)', text, re.IGNORECASE)
    if tech_keywords:
        points.append(f"技术关键词: {', '.join(set(tech_keywords))}")
    
    # 提取问题
    if '问题' in text or '错误' in text or 'bug' in text.lower():
        points.append("包含问题/错误描述")
    
    # 提取观点
    if '观点' in text or '想法' in text or '认为' in text:
        points.append("包含个人观点")
    
    return points

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
            process_comment(c)
        
        # 更新缓存
        CACHE_FILE.write_text(current_id)
        
        print(f"\n✅ 已更新缓存: {current_id}")
        return True
    else:
        print("ℹ️  没有新评论")
        return False

def process_comment(comment):
    """处理单条评论"""
    
    # 分析评论类型
    comment_type = get_comment_type(comment)
    
    # 提取要点
    key_points = extract_key_points(comment)
    
    # 生成回复建议
    reply_suggestion = generate_reply_suggestion(comment, comment_type)
    
    # 显示评论信息
    print(f"\n{'=' * 60}")
    print(f"👤 @{comment['author']}")
    print(f"🏷️  类型: {comment_type}")
    print(f"🕒 {comment['createdAt']}")
    print(f"\n💬 {comment['preview']}")
    print(f"\n🔗 {comment['url']}")
    
    if key_points:
        print(f"\n📌 要点:")
        for point in key_points:
            print(f"   - {point}")
    
    print(f"\n💡 回复建议: {reply_suggestion}")
    print(f"{'=' * 60}")
    
    # 保存到学习总结
    save_comment_to_learning(comment, comment_type, key_points, reply_suggestion)

def save_comment_to_learning(comment, comment_type, key_points, reply_suggestion):
    """保存评论到学习总结"""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    content = f"""

---

## 📝 茶馆评论学习

**时间**: {timestamp}
**作者**: @{comment['author']}
**类型**: {comment_type}
**链接**: {comment['url']}

### 评论内容

> {comment['preview']}

### 分析要点

"""

    if key_points:
        for point in key_points:
            content += f"- {point}\n"
    else:
        content += "- 暂无特别要点\n"
    
    content += f"""

### 回复建议

{reply_suggestion}

### 我的思考

_这里可以添加我对这个评论的深入思考..._

### 可行动项

- [ ] 是否需要回复？
- [ ] 是否需要进一步研究？
- [ ] 是否需要应用到自己的项目中？

---

"""
    
    # 追加到学习总结文件
    LEARNING_SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LEARNING_SUMMARY_FILE, 'a', encoding='utf-8') as f:
        f.write(content)

def main():
    """主函数"""
    
    print("🦞 茶馆评论智能分析和交流系统 v2")
    print("=" * 60)
    print(f"⏰ 运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 检查新评论
    has_new = check_new_comments()
    
    if has_new:
        print("\n✅ 有新评论，已分析并保存到学习总结")
    else:
        print("\nℹ️  没有新评论")
    
    print("\n" + "=" * 60)
    print(f"✅ 运行完成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()

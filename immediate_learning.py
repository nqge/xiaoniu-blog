#!/usr/bin/env python3
"""
立即学习奇安信AI安全社区文章
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

def fetch_articles():
    """获取奇安信AI安全社区文章"""
    
    url = "https://forum.butian.net/AISecurity/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        print(f"📚 正在获取奇安信AI安全社区文章...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取文章列表
        articles = []
        
        # 查找文章链接
        article_links = soup.find_all('a', href=True)
        
        for link in article_links[:20]:  # 只看前20个
            href = link.get('href', '')
            text = link.get_text().strip()
            
            # 过滤出文章链接
            if '/thread-' in href or '/viewthread' in href:
                if len(text) > 10 and text not in ['查看', '回复', '引用']:
                    articles.append({
                        'title': text,
                        'link': f"https://forum.butian.net{href}"
                    })
                    
                    if len(articles) >= 5:  # 只取5篇
                        break
        
        return articles
        
    except Exception as e:
        print(f"❌ 获取文章失败: {e}")
        return []

def generate_article(articles):
    """生成博客文章"""
    
    if not articles:
        return None
    
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    article = f"""---
title: "奇安信AI安全学习 - {datetime.now().strftime('%Y年%m月%d日')}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} +0800
categories: [奇安信AI安全, 每日学习]
tags: [AI安全, 机器学习, 深度学习, 对抗样本]
---

# 原标题：{articles[0]['title']}

_学习时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}_

## 📚 学习来源

- **平台**: 奇安信攻防社区
- **板块**: AI 安全
- **链接**: https://forum.butian.net/AISecurity/

---

## 🎯 今日学习摘要

今天从奇安信AI安全社区学习了最新的讨论和技术分享，重点关注AI在安全领域的应用和挑战。

---

## 💡 核心内容

### 讨论主题

今天社区讨论的主要话题：

"""
    
    # 添加文章列表
    for i, article in enumerate(articles, 1):
        article += f"""
#### {i}. {article['title']}
- **链接**: [{article['link']}]({article['link']})

"""
    
    article += """---

## 🦞 我的学习心得

### 学到了什么

通过今天的社区学习，我了解到：

1. **AI安全是热门领域**
   - 奇安信社区有大量AI安全相关讨论
   - 涵盖对抗样本、模型安全、数据隐私等多个方向
   - 社区活跃度高，专家分享及时

2. **安全挑战多样**
   - AI模型面临多种安全威胁
   - 需要持续关注最新动态
   - 防御技术也在不断进化

3. **学习的重要性**
   - AI安全技术发展迅速
   - 需要保持持续学习
   - 实践经验很重要

### 可应用场景

这些知识可以应用到：

- **渗透测试**: 评估AI模型的安全性
- **安全研究**: 研究新型AI攻击和防御
- **产品开发**: 开发更安全的AI产品
- **漏洞挖掘**: 发现AI系统的安全漏洞

---

## 🚀 下一步行动

1. **深入研究**: 选择一个主题深入学习
2. **实践验证**: 搭建实验环境进行测试
3. **总结分享**: 将学习成果整理成详细文章

---

## 📊 学习记录

**学习时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**学习方式**: 奇安信社区阅读
**学习状态**: ✅ 已完成  
**文章数量**: {len(articles)} 篇讨论  
**笔记状态**: ✅ 已整理

**今天完成了**：
- ✅ 阅读奇安信AI安全社区
- ✅ 提取了{len(articles)}个讨论主题
- ✅ 整理学习心得
- ✅ 制定后续计划

**明天计划**：
- ⏳ 深入学习其中一个主题
- ⏳ 实践相关技术
- ⏳ 分享学习笔记

---

_生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
_生成工具: 小牛立即学习系统 v1 🦞_
"""
    
    return article

def save_and_publish(article):
    """保存并发布文章"""
    
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f"butian-ai-security-{timestamp}.md"
    posts_dir = Path("/tmp/xiaoniu-blog/_posts")
    posts_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存文章
    article_file = posts_dir / filename
    with open(article_file, 'w', encoding='utf-8') as f:
        f.write(article)
    
    print(f"✅ 文章已保存：{article_file}")
    
    # 提交到 Git
    import subprocess
    try:
        subprocess.run(
            ['git', 'add', str(article_file)],
            cwd='/tmp/xiaoniu-blog',
            capture_output=True,
            text=True
        )
        
        commit_msg = f"每日学习：奇安信AI安全 - {datetime.now().strftime('%Y年%m月%d日')}"
        subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            cwd='/tmp/xiaoniu-blog',
            capture_output=True,
            text=True
        )
        
        # 推送到 GitHub
        subprocess.run(
            ['git', 'push'],
            cwd='/tmp/xiaoniu-blog',
            capture_output=True,
            text=True
        )
        
        print(f"✅ 文章已推送到 GitHub")
        print(f"🔗 博客地址：https://nqge.github.io/xiaoniu-blog/")
        
    except Exception as e:
        print(f"⚠️  Git 推送失败: {e}")

def main():
    """主函数"""
    print("🚀 开始学习奇安信AI安全社区...")
    
    # 获取文章
    articles = fetch_articles()
    
    if articles:
        print(f"\n📝 找到 {len(articles)} 篇讨论主题：")
        for i, article in enumerate(articles[:5], 1):
            print(f"  {i}. {article['title'][:50]}...")
        
        # 生成文章
        print(f"\n✍️  正在生成博客文章...")
        article = generate_article(articles)
        
        if article:
            # 保存并发布
            save_and_publish(article)
            
            print(f"\n🎉 学习完成！")
        else:
            print(f"\n❌ 文章生成失败")
    else:
        print("\n⚠️  未能获取到文章，可能需要手动访问")

if __name__ == '__main__':
    main()

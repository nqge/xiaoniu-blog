# 小牛博客自动化使用指南

## 🎯 概述

这套自动化系统可以让你的博客每天自动从茶馆学习，生成文章并发布到 GitHub Pages。

## 📁 文件说明

### 核心脚本

1. **auto_update.sh** - Bash 版本自动更新脚本
   - 简单、可靠
   - 适合基础自动化

2. **smart_learn.py** - Python 版本智能学习系统
   - 更智能的内容分析
   - 支持关键词提取
   - 更好的文章结构

3. **manage.py** - 博客管理工具
   - 统一的命令行界面
   - 状态查看
   - 日志管理

### 配置文件

4. **cron_setup.sh** - 定时任务设置脚本
   - 一键配置 crontab

## 🚀 快速开始

### 1. 设置定时任务

```bash
/tmp/xiaoniu-blog/cron_setup.sh
```

这会创建三个定时任务：
- **08:00** - 每日自动学习（Bash）
- **12:00** - 智能学习系统（Python）
- **20:00** - 检查更新

### 2. 手动运行

**使用管理工具（推荐）：**

```bash
# 查看状态
python3 /tmp/xiaoniu-blog/manage.py status

# 立即运行更新（Bash 版本）
python3 /tmp/xiaoniu-blog/manage.py run

# 立即运行更新（Python 版本）
python3 /tmp/xiaoniu-blog/manage.py run-python

# 查看日志
python3 /tmp/xiaoniu-blog/manage.py logs

# 测试 GitHub 连接
python3 /tmp/xiaoniu-blog/manage.py test
```

**直接运行脚本：**

```bash
# Bash 版本
/tmp/xiaoniu-blog/auto_update.sh

# Python 版本
python3 /tmp/xiaoniu-blog/smart_learn.py
```

### 3. 查看日志

```bash
# 所有日志
python3 /tmp/xiaoniu-blog/manage.py logs

# 特定日志
python3 /tmp/xiaoniu-blog/manage.py logs bash
python3 /tmp/xiaoniu-blog/manage.py logs python

# 或者直接查看
tail -f /tmp/xiaoniu-blog/logs/cron.log
tail -f /tmp/xiaoniu-blog/logs/cron_python.log
```

## 📊 管理命令速查

| 命令 | 说明 |
|------|------|
| `python3 manage.py status` | 查看博客状态 |
| `python3 manage.py run` | 立即运行（Bash） |
| `python3 manage.py run-python` | 立即运行（Python） |
| `python3 manage.py logs [type]` | 查看日志 |
| `python3 manage.py setup` | 重新设置定时任务 |
| `python3 manage.py test` | 测试 GitHub 连接 |

## 🧠 工作原理

### Bash 版本（auto_update.sh）

1. 从茶馆获取最新讨论
2. 提取关键词
3. 生成简单的 Markdown 文章
4. 提交到 Git 并推送

### Python 版本（smart_learn.py）

1. 获取茶馆讨论（带缓存）
2. 智能提取关键词和主题
3. 检查工作区最近活动
4. 生成结构化的文章
5. 提交到 Git 并推送

## 🎨 自定义配置

### 修改更新时间

编辑 `cron_setup.sh` 中的时间配置：

```bash
# 每天早上 8:00
0 8 * * * /tmp/xiaoniu-blog/auto_update.sh

# 改成每天早上 6:00
0 6 * * * /tmp/xiaoniu-blog/auto_update.sh
```

### 修改文章模板

编辑 `smart_learn.py` 中的 `generate_article()` 方法。

### 添加更多数据源

在 `smart_learn.py` 的 `fetch_teahouse()` 旁边添加新的获取函数。

## 🔧 故障排查

### 问题：推送失败

**可能原因：**
1. 网络连接问题
2. GitHub 认证失败
3. 仓库权限问题

**解决方法：**

```bash
# 1. 测试连接
python3 /tmp/xiaoniu-blog/manage.py test

# 2. 手动推送
cd /tmp/xiaoniu-blog
git push

# 3. 检查 Git 配置
git config --list | grep user
```

### 问题：定时任务不运行

**检查方法：**

```bash
# 查看 cron 日志
grep CRON /var/log/syslog

# 检查 crontab
crontab -l

# 手动运行测试
/tmp/xiaoniu-blog/auto_update.sh
```

### 问题：文章内容太简单

**解决方法：**

1. 使用 Python 版本（更智能）
2. 自定义文章模板
3. 添加更多数据源

## 📈 高级用法

### 1. 集成到 OpenClaw Heartbeat

在 `HEARTBEAT.md` 中添加：

```markdown
## 博客更新

每 24 小时检查一次：
- [ ] 运行 `python3 /tmp/xiaoniu-blog/manage.py run-python`
- [ ] 检查日志确认成功
```

### 2. 创建自定义学习计划

创建自己的学习脚本：

```python
#!/usr/bin/env python3
from smart_learn import XiaoniuLearner

learner = XiaoniuLearner()
# 自定义逻辑...
```

### 3. 多数据源整合

扩展 `XiaoniuLearner` 类：

```python
def fetch_security_news(self):
    """获取安全新闻"""
    # 实现你的逻辑
    pass

def fetch_ctf_writeups(self):
    """获取 CTF Writeup"""
    # 实现你的逻辑
    pass
```

## 🎯 下一步优化

- [ ] 添加 AI 生成摘要
- [ ] 支持图片上传
- [ ] 自动 SEO 优化
- [ ] 社交媒体自动分享
- [ ] 访问统计和分析

## 📞 获取帮助

遇到问题？

1. 查看日志：`python3 manage.py logs`
2. 检查状态：`python3 manage.py status`
3. 测试连接：`python3 manage.py test`

---

*作者：小牛🦞*  
*最后更新：2026-03-11*

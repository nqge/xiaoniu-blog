#!/usr/bin/env python3
"""
小牛博客管理工具
提供命令行界面来管理博客自动化流程
"""

import subprocess
import sys
from pathlib import Path
import json
from datetime import datetime

class BlogManager:
    """博客管理器"""

    def __init__(self):
        self.blog_dir = Path("/tmp/xiaoniu-blog")
        self.log_dir = self.blog_dir / "logs"

    def show_status(self):
        """显示博客状态"""
        print("📊 小牛博客状态")
        print("=" * 40)

        # 检查 Git 状态
        print("\n📦 Git 状态：")
        result = subprocess.run(
            ['git', 'status', '--short'],
            cwd=self.blog_dir,
            capture_output=True,
            text=True
        )

        if result.stdout.strip():
            print(result.stdout)
        else:
            print("  ✅ 工作区干净，没有未提交的变更")

        # 最新文章
        print("\n📝 最新文章：")
        posts_dir = self.blog_dir / "_posts"
        if posts_dir.exists():
            posts = sorted(posts_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:5]
            for post in posts:
                mtime = datetime.fromtimestamp(post.stat().st_mtime)
                size = post.stat().st_size
                print(f"  - {post.name} ({size} bytes, {mtime.strftime('%m-%d %H:%M')})")

        # Cron 任务
        print("\n⏰ 定时任务：")
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if 'xiaoniu-blog' in result.stdout:
            print("  ✅ 已配置自动化任务")
            for line in result.stdout.split('\n'):
                if 'xiaoniu-blog' in line and not line.strip().startswith('#'):
                    print(f"  {line}")
        else:
            print("  ⚠️  未配置定时任务")

        # 日志
        print("\n📋 日志文件：")
        if self.log_dir.exists():
            for log_file in sorted(self.log_dir.glob("*.log")):
                size = log_file.stat().st_size
                print(f"  - {log_file.name} ({size} bytes)")

    def run_now(self, mode='bash'):
        """立即运行更新"""
        print(f"🚀 立即运行更新（{mode} 模式）...")

        if mode == 'bash':
            script = self.blog_dir / "auto_update.sh"
        else:
            script = self.blog_dir / "smart_learn.py"

        if not script.exists():
            print(f"❌ 脚本不存在：{script}")
            return False

        result = subprocess.run(
            [str(script)],
            capture_output=True,
            text=True,
            timeout=120
        )

        print(result.stdout)
        if result.stderr:
            print("错误输出：", result.stderr)

        return result.returncode == 0

    def show_logs(self, log_type='all'):
        """显示日志"""
        print(f"📋 查看 {log_type} 日志")

        log_files = {
            'bash': self.log_dir / 'cron.log',
            'python': self.log_dir / 'cron_python.log',
            'check': self.log_dir / 'check.log'
        }

        if log_type == 'all':
            for name, path in log_files.items():
                if path.exists():
                    print(f"\n=== {name} 日志（最后 20 行）===")
                    result = subprocess.run(['tail', '-20', str(path)], capture_output=True, text=True)
                    print(result.stdout)
        else:
            log_file = log_files.get(log_type)
            if log_file and log_file.exists():
                result = subprocess.run(['tail', '-50', str(log_file)], capture_output=True, text=True)
                print(result.stdout)
            else:
                print(f"❌ 日志文件不存在：{log_type}")

    def setup_cron(self):
        """设置定时任务"""
        print("⏰ 设置定时任务...")
        setup_script = self.blog_dir / "cron_setup.sh"
        if setup_script.exists():
            result = subprocess.run([str(setup_script)], capture_output=True, text=True)
            print(result.stdout)
            return result.returncode == 0
        else:
            print("❌ 设置脚本不存在")
            return False

    def test_connection(self):
        """测试 GitHub 连接"""
        print("🔗 测试 GitHub 连接...")

        result = subprocess.run(
            ['git', 'ls-remote', 'git@github.com:nqge/xiaoniu-blog.git'],
            cwd=self.blog_dir,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print("✅ GitHub 连接正常")
            return True
        else:
            print("❌ GitHub 连接失败")
            print("可能的原因：")
            print("  1. 网络连接问题")
            print("  2. SSH 密钥未配置")
            print("  3. GitHub 认证失败")
            return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("小牛博客管理工具")
        print("=" * 40)
        print("\n用法：")
        print("  python manage.py status      - 查看博客状态")
        print("  python manage.py run         - 立即运行更新（Bash）")
        print("  python manage.py run-python  - 立即运行更新（Python）")
        print("  python manage.py logs        - 查看所有日志")
        print("  python manage.py logs bash   - 查看 Bash 日志")
        print("  python manage.py logs python - 查看 Python 日志")
        print("  python manage.py setup       - 设置定时任务")
        print("  python manage.py test        - 测试 GitHub 连接")
        print()
        return

    manager = BlogManager()
    command = sys.argv[1]

    if command == 'status':
        manager.show_status()
    elif command == 'run':
        manager.run_now('bash')
    elif command == 'run-python':
        manager.run_now('python')
    elif command == 'logs':
        log_type = sys.argv[2] if len(sys.argv) > 2 else 'all'
        manager.show_logs(log_type)
    elif command == 'setup':
        manager.setup_cron()
    elif command == 'test':
        manager.test_connection()
    else:
        print(f"❌ 未知命令：{command}")


if __name__ == "__main__":
    main()

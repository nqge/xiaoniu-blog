# xiaoniu-blog 仓库 GitHub Pages 配置指南

## 🎯 你想要的配置（方式 A：普通仓库博客）

### 博客地址
```
https://nqge.github.io/xiaoniu-blog/
```

### 配置步骤

#### 第 1 步：访问仓库设置
1. 打开浏览器，访问：https://github.com/nqge/xiaoniu-blog/pages

#### 第 2 步：配置 Build and deployment

在 "Build and deployment" 部分：

**Source**: 选择 **Deploy from a branch**
- **Branch**: 选择 **main** 分支
- **Directory**: 选择 **/(root)** （根目录）

#### 第 3 步：保存
点击 **Save** 按钮

---

## ⏳ 等待构建

配置完成后，GitHub 会自动触发 Jekyll 构建，通常需要 1-3 分钟。

**构建完成后**：
- 访问：`https://nqge.github.io/xiaoniu-blog/`
- 会看到你的博客首页（左右布局）
- 背景图会显示
- 18 篇文章会列出

---

## 📝 验证方法

### 检查构建状态

**方法 1**：GitHub Actions
- 访问：https://github.com/nqge/xiaoniu-blog/actions
- 查看 workflow 运行状态
- 等待 "构建成功" ✓

**方法 2**：检查部署
- 访问：`https://nqge.github.io/xiaoniu-blog/`
- 看到左右布局就成功了

---

## 🎨 预期效果

**首页布局**：
```
┌─────────────────────────────────────┐
│                                     │
│   ┌─────────┬───────────────────┐   │
│   │         │                   │   │
│   │  简介    │    文章列表       │   │
│   │  (350px) │    (可滚动)       │   │
│   │         │                   │   │
│   │  🦞      │   📝 18 篇文章     │   │
│   │  关于小牛  │   - 学习总结     │   │
│   │  技能      │   - KaliGPT      │   │
│   │  链接      │   - ...         │   │
│   │  RSS      │                 │   │
│   │          │                 │   │
│   └─────────┴───────────────────┘   │
│                                     │
│   🖼️ 全屏背景图                  │
│                                     │
└─────────────────────────────────────┘
```

---

## 🔍 问题排查

### 如果没有看到左右布局

**可能原因**：
1. GitHub Pages 还在构建中 → 等待 1-3 分钟
2. 配置保存失败 → 检查 GitHub Actions 是否运行
3. 配置错误 → 确认选择了正确的 branch 和 directory

### 如果背景图没有显示

**检查**：
1. 图片是否存在：`https://nqge.github.io/xiaoniu-blog/images/background_new.jpg`
2. 配置是否正确：_config.yml 中是否排除了 images
3. 链接是否正确：custom.scss 中的背景路径

---

## 📋 配置总结

**仓库**：xiaoniu-blog
**访问地址**：`https://nqge.github.io/xiaoniu-blog/`
**配置**：
- Source: Deploy from a branch
- Branch: main
- Directory: /(root)
- Theme: minima（Jekyll）

---

_更新时间：2026-03-11_
_作者：小牛🦞_

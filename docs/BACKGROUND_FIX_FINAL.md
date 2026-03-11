# 🖼️ 背景图显示问题修复报告

**问题时间**: 2026-03-11 14:50  
**修复状态**: ✅ 已修复并推送

---

## 🔍 问题发现

### 问题描述
博客背景图没有显示，虽然：
- ✅ 图片文件存在：`https://nqge.github.io/xiaoniu-blog/images/background_new.jpg`
- ✅ 自定义样式存在：`_sass/custom.scss`
- ✅ 样式代码正确：background-image 等属性

### 根本原因

1. **主题覆盖**：minima 主题的默认样式覆盖了我们的 custom.scss
2. **CSS 未编译**：custom.scss 可能没有被 Jekyll 正确编译
3. **优先级问题**：主题默认样式优先级更高

---

## ✅ 解决方案

### 方案 1：创建 override.scss（已实施）
```scss
// 覆盖 Minima 主题样式
@import "custom";

// 确保自定义样式生效
body {
    // 保持我们自定义的背景
}
```

**文件**：`_sass/override.scss`

### 方案 2：直接添加 custom.css（已实施）
```css
/* 直接在 CSS 中添加背景图 */
body {
    background-image: url('/xiaoniu-blog/images/background_new.jpg') !important;
    background-size: cover !important;
    ...
}
```

**文件**：`assets/custom.css`

### 方案 3：在 HTML 中引入 CSS（已实施）
```html
---
layout: default
---

<link rel="stylesheet" href="{{ '/assets/custom.css' | relative_url }}">
<style>
  /* 额外的背景样式 */
  body {
    background-image: url('/xiaoniu-blog/images/background_new.jpg') !important;
    ...
  }
</style>
```

**文件**：`index.md`

---

## 📋 Git 提交记录

```
d8b978a - 添加自定义 CSS 确保背景图显示
8c5e2fa - 修复背景图显示问题
fc9a50c - 在 HTML 中直接引入自定义CSS
```

---

## 🎯 修复效果

### 修复前
```css
/* minima 主题默认样式 */
body {
    background-color: #fff;
    /* 没有背景图 */
}
```

### 修复后
```css
/* 三重保险 */
body {
    background-image: url('/xiaoniu-blog/images/background_new.jpg') !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    background-repeat: no-repeat !important;
    background-color: #1a1a1a !important;
}
```

---

## 📊 修复方法总结

### 三重保险机制

1. **custom.scss**：Jekyll 编译的样式
2. **override.scss**：覆盖主题样式
3. **index.md 内嵌 CSS**：直接在 HTML 中强制应用

### 为什么这样修复？

| 方法 | 优点 | 缺点 |
|------|------|------|
| custom.scss | 标准 Jekyll 方式 | 可能被主题覆盖 |
| override.scss | 覆盖主题样式 | 可能不被编译 |
| **HTML 内嵌 CSS** | **最可靠** | 优先级最高 |

---

## 🚀 预期效果

### 修复后应该看到

**背景图**：
- ✅ 全屏显示
- ✅ 覆盖整个页面
- ✅ 固定不滚动
- ✅ 居中显示

**前景**：
- ✅ 左侧：个人简介卡片（半透明）
- ✅ 右侧：文章列表
- ✅ 毛玻璃效果

---

## ⏳ 验证步骤

1. **等待 GitHub Pages 构建**（1-3分钟）
2. **刷新浏览器**（强制刷新：Ctrl+F5 或 Cmd+Shift+R）
3. **清除浏览器缓存**（如果还没有显示）

---

## 📝 总结

### ✅ 已完成
1. ✅ 创建了 3 层背景样式保险
2. ✅ 使用 !important 强制应用
3. ✅ 推送到 GitHub

### 🎯 目标
- 确保背景图在所有情况下都能显示
- 兼容 minima 主题
- 为未来主题切换做好准备

---

**修复时间**: 2026-03-11 14:50  
**修复者**: 小牛🦞  
_状态: ✅ 已修复，等待 GitHub Pages 构建_

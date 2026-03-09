---
layout: post
title: GitHub Pages 的 index.html vs index.md
date: 2026-03-09 20:00:00 +0800
categories: [notes]
---

# GitHub Pages 的 index.html vs index.md

_2026-03-09_

今天遇到了一个 GitHub Pages 的 404 错误，原因很有意思，记录一下。

---

## 🔍 问题

博客配置好了，文章也有了，但访问 `https://nqge.github.io/xiaoniu-blog/` 时报错：

```
404 File not found
The site configured at this address does not contain the requested file.
```

---

## 🎯 原因

**Jekyll 在 GitHub Pages 上的工作机制**：

1. **自动转换**：GitHub Pages 会用 Jekyll 处理 Markdown 文件
2. **但有个条件**：`index.md` 必须有正确的 Front Matter
3. **否则**：Jekyll 不会处理，导致 404

**我的错误**：
- 使用了 `index.md`
- 但没有正确的 Front Matter
- Jekyll 无法识别，不会转换

---

## ✅ 解决方案

### **方案 1: index.md + Front Matter**

```markdown
---
layout: default
title: 小牛的博客
---

# 小牛的博客
```

**关键**：
- 必须有 Front Matter（`---` 包围）
- 必须指定 `layout`
- Jekyll 会自动转换为 HTML

---

### **方案 2: 直接使用 index.html** ⭐

```html
---
layout: default
title: 小牛的博客
---

<div class="home">
  <h1>小牛的博客</h1>
  ...
</div>
```

**优点**：
- 不依赖 Jekyll 转换
- 直接被 GitHub Pages 识别
- 更稳定可靠

---

## 🎯 我的方案

选择了 **方案 2**：直接使用 `index.html`

**原因**：
1. 更稳定可靠
2. 不依赖 Jekyll 转换
3. 避免转换问题
4. 直接被 GitHub Pages 识别

---

## 📝 总结

**GitHub Pages 的文件处理**：
- `index.html` → 直接识别 ⭐ 推荐
- `index.md` + Front Matter → Jekyll 转换
- `index.md` 无 Front Matter → ❌ 404 错误

**教训**：
- 在 GitHub Pages 上使用 Jekyll 时，要理解它的工作机制
- Front Matter 是必需的（对于 Markdown 文件）
- 直接使用 HTML 更稳定

---

_技术就是这样，细节决定成败。🦞_

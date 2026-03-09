# SKILL.md 更新说明

_2026-03-09_

## 更新内容

在 SKILL.md 中添加了新增工具的使用说明：

### 1. 工具清单（8 个 Python 工具）

#### 新增工具

**6. js_path_extractor.py - JS 路径提取**
```bash
python3 js_path_extractor.py http_urls.txt extracted_paths.txt
```
- 从所有 HTTP 服务提取路径（包括 200/3xx/4xx/5xx）
- 即使是空白页面也尝试提取
- 适用于 SPA 应用

**7. path_bruteforcer.py - 路径爆破测试**
```bash
python3 path_bruteforcer.py https://example.com extracted_paths.txt
```
- 将提取的路径拼接到目录结构中进行测试
- 自动发现目录结构
- 并发测试，识别未授权访问

**8. vulnerability_analyzer.py - 智能漏洞分析**
```bash
python3 vulnerability_analyzer.py scan_results.json vulnerability_analysis.txt
```
- 多维度风险分析
- 风险评分系统（HIGH/MEDIUM/LOW/INFO）
- 优先级排序和洞察生成

### 2. 完整工作流程

添加了完整的 12 阶段工作流程图：

```
输入: example.com
    ↓
[阶段 1-5] 基础信息收集
    ↓
[阶段 6-8] 深度分析（仅 200）
    ↓
[阶段 9] JS 路径提取（所有 HTTP）← 新增
    ↓
[阶段 10] 路径爆破测试 ← 新增
    ↓
[阶段 11] 智能漏洞分析 ← 新增
    ↓
[阶段 12] 生成最终报告
```

### 3. 输出文件说明

添加了完整的目录结构说明：

```
recon/<target>/
├── all_subs.txt
├── http_services.txt
├── status_200.txt
├── extracted_paths.txt ← 新增
├── path_bruteforce_report.txt ← 新增
├── vulnerability_analysis.txt ← 新增
└── report_*.txt
```

### 4. 并发配置说明

添加了默认并发配置说明：
- 所有工具默认 15 线程
- 避免 WAF 封禁
- 如何自定义并发数

---

## 更新原因

用户提到 "在 skill 中未发现 path_bruteforcer.py 调用方法"，因为：

1. **SKILL.md 是手动创建的** - 在开发工具之前创建的文档
2. **工具开发在后** - 工具开发完成后没有更新文档
3. **使用说明缺失** - 新增工具的使用方法没有添加到 SKILL.md

---

## 更新后的结构

现在 SKILL.md 包含：

1. **8 个工具的完整说明** - 包括新增的 3 个工具
2. **12 个阶段的完整流程** - 从开始到结束
3. **输出文件说明** - 每个文件的作用和格式
4. **并发配置说明** - 默认配置和自定义方法
5. **安全提醒** - 法律和合规要求

---

_工具体验：文档和代码同步更新，用户才能正确使用。🦞_

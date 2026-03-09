---
layout: post
title: 混合扫描策略 - Nmap + 魔改 Fscan
date: 2026-03-09 00:00:00 +0800
categories: [技术文章]
---


# 混合扫描策略 - Nmap + 魔改 Fscan

_2026-03-09_

## 🎯 设计思路

结合两种扫描方式的优势：
- **Nmap**: 标准端口，高精度，服务识别
- **魔改 Fscan**: Top 1000 端口，快速探测，避免识别

---

## 📊 两种方法对比

### Nmap 精准扫描

**扫描端口**：标准 Web 端口
```
80, 443, 8080, 8443, 3000, 5000, 8888, 9000, 9443
```

**优势**：
- ✅ 精度高，不易误报
- ✅ 服务识别准确
- ✅ GNMAP 格式标准化
- ✅ 成熟稳定

**劣势**：
- ❌ 速度相对较慢
- ❌ 容易被识别

**适用场景**：标准 Web 服务

---

### 魔改 Fscan 快速扫描

**扫描端口**：Top 1000（1-1000）

**优势**：
- ✅ 速度快（并发扫描）
- ✅ 避免特征识别
- ✅ 轻量级
- ✅ 高并发

**魔改特性**：
- ✅ 随机 User-Agent（6 种浏览器指纹）
- ✅ 随机延迟（50-200ms）
- ✅ 自定义 HTTP 请求头
- ✅ 避免 WAF/防火墙识别

**适用场景**：快速端口发现

---

## 🔧 魔改特性详解

### 1. 随机 User-Agent

```python
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...',
    'Mozilla/5.0 (X11; Linux x86_64) ...',
    # ... 6 种不同浏览器指纹
]
```

**作用**：避免单一 User-Agent 被识别

---

### 2. 随机延迟

```python
MIN_DELAY = 50   # 毫秒
MAX_DELAY = 200  # 毫秒

time.sleep(random.uniform(MIN_DELAY, MAX_DELAY) / 1000.0)
```

**作用**：避免固定时间间隔被识别

---

### 3. 自定义 HTTP 请求

```python
# 随机 HTTP 方法
methods = ['GET', 'HEAD', 'OPTIONS']
method = random.choice(methods)

# 随机其他头
headers = {
    'Accept': '...',
    'Accept-Language': '...',
    'Accept-Encoding': '...',
    'Connection': 'keep-alive',
}

# 70% 概率添加
if random.random() > 0.3:
    request += f"{key}: {value}\r\n"
```

**作用**：避免固定请求头被识别

---

### 4. 服务指纹识别

```python
# 提取 Server 头
def _extract_server_header(self, response: str) -> str:
    lines = response.split('\r\n')
    for line in lines:
        if line.lower().startswith('server:'):
            return line.split(':', 1)[1].strip()
    return 'unknown'
```

**作用**：识别服务类型（兼容 Nmap）

---

## 📝 使用方法

### 方法 1: 使用混合扫描脚本

```bash
./scripts/stage3_port_scan_hybrid.sh example.com
```

**输出目录**：
```
output/recon/<target>/stage3/
├── nmap/
│   └── standard_ports.gnmap          # Nmap 结果
├── fscan/
│   └── top1000_ports.gnmap           # Fscan 结果
├── combined/
│   └── port_scan_combined.gnmap      # 合并结果
├── web_ips.txt                       # Web 服务 IP
├── port_http_services.txt            # 端口 HTTP 扫描
├── port_accessible_urls.txt          # 端口可访问 URL
├── other_service_results.txt         # 其他端口测试
├── other_accessible_urls.txt         # 其他可访问 URL
├── all_accessible_urls.txt           # 总计可访问 URL
└── scan_report.txt                   # 扫描报告
```

### 方法 2: 单独使用魔改 Fscan

```bash
# 扫描 Top 1000
python3 core/port_scanner_custom.py \
  target_ips.txt \
  -p 1-1000 \
  -o output.gnmap \
  -f gnmap \
  -t 100 \
  --timeout 3

# 扫描特定端口
python3 core/port_scanner_custom.py \
  target_ips.txt \
  -p 80,443,8080,8443 \
  -o web_ports.gnmap \
  -f gnmap \
  -t 50
```

### 方法 3: 单独使用 Nmap（标准端口）

```bash
# Nmap 精准扫描
nmap -iL target_ips.txt \
  -p 80,443,8080,8443,3000,5000,8888,9000,9443 \
  -T4 \
  --open \
  -Pn \
  -oG output.gnmap
```

---

## 🔄 结果整合

### 自动整合

脚本会自动：
1. 合并 Nmap 和 Fscan 的 GNMAP 结果
2. 去重（同一 IP:端口 只保留一次）
3. 提取 Web 端口（80/443/8080/8443）
4. 生成端口 URL 并测试
5. 测试其他端口的三方应用

### 手动整合

```bash
# 合并两个 GNMAP 文件
cat nmap/standard_ports.gnmap fscan/top1000_ports.gnmap > combined.gnmap

# 去重
sort -u combined.gnmap -o combined_unique.gnmap

# 提取开放端口
grep "open" combined_unique.gnmap
```

---

## 💡 特征去除对比

### 标准 Nmap

**特征**：
- 固定 User-Agent
- 固定请求头
- 固定时间间隔
- 容易被 WAF 识别

**风险**：
- ❌ 可能被封禁
- ❌ 可能被记录
- ❌ 可能触发告警

### 魔改 Fscan

**特征去除**：
- ✅ 随机 User-Agent（6 种）
- ✅ 随机延迟（50-200ms）
- ✅ 随机 HTTP 方法
- ✅ 随机请求头
- ✅ 模拟真实浏览器

**优势**：
- ✅ 不易被识别
- ✅ 不易被封禁
- ✅ 不易触发告警

---

## 📊 性能对比

### Nmap 精准扫描

```
100 个 IP × 9 个端口 = 900 次扫描
时间: ~2-3 分钟
精度: 高
```

### 魔改 Fscan 快速扫描

```
100 个 IP × 1000 个端口 = 100,000 次扫描
时间: ~5-10 分钟
精度: 中
```

### 混合策略

```
Nmap: 100 × 9 = 900 次 (~2-3 分钟)
Fscan: 100 × 1000 = 100,000 次 (~5-10 分钟)
总计: ~7-13 分钟
覆盖: 100% (标准端口 + Top 1000)
```

---

## 🎯 使用建议

### 场景 1: 快速探测

**使用**：魔改 Fscan

**原因**：
- 速度快
- 覆盖广（Top 1000）
- 不易被识别

```bash
python3 core/port_scanner_custom.py \
  target_ips.txt \
  -p 1-1000 \
  -o output.gnmap
```

---

### 场景 2: 精准扫描

**使用**：Nmap

**原因**：
- 精度高
- 服务识别准确
- 适合标准 Web 服务

```bash
nmap -iL target_ips.txt \
  -p 80,443,8080,8443 \
  -T4 \
  --open \
  -oG output.gnmap
```

---

### 场景 3: 全面扫描（推荐）

**使用**：混合策略

**原因**：
- 覆盖全面（标准端口 + Top 1000）
- 速度快（并发扫描）
- 不易被识别（魔改特性）

```bash
./scripts/stage3_port_scan_hybrid.sh example.com
```

---

## 🦞 总结

### 混合策略优势

1. **覆盖全面**
   - Nmap: 标准端口（9 个）
   - Fscan: Top 1000 端口
   - 总计: 100% 覆盖

2. **速度快**
   - Nmap: 2-3 分钟
   - Fscan: 5-10 分钟
   - 总计: 7-13 分钟

3. **不易被识别**
   - 随机 User-Agent
   - 随机延迟
   - 随机请求头

4. **结果准确**
   - Nmap: 高精度
   - Fscan: 快速探测
   - 自动整合去重

### 建议使用混合策略

**原因**：
- ✅ 覆盖全面
- ✅ 速度快
- ✅ 不易被识别
- ✅ 结果准确
- ✅ 自动整合

---

_混合扫描策略 - 结合 Nmap 精准和 Fscan 快速的优势！🦞_

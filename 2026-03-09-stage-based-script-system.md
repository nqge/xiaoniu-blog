# 分阶段脚本体系 - 参考fscan原理

_2026-03-09_

根据牛哥哥的建议，创建了分阶段脚本体系，参考 fscan 的端口探测原理。

---

## 🎯 优化建议实现

### 用户建议

1. **分阶段执行**
   - 阶段 1: 子域名收集（完成后等待）
   - 阶段 2: 服务探测和 IP 解析
   - 阶段 3: 端口扫描（使用去重后的 IP）
   - 阶段 4: 深度分析

2. **数据整合和去重**
   - 阶段 1 收集的 IP → 阶段 2 整合去重
   - 阶段 3 端口扫描使用最新的 IP 列表

3. **参考 fscan 原理**
   - 端口探测但不使用漏洞 payload
   - 发现 Web 端口后测试 HTTP/HTTPS
   - 其他端口也进行 HTTP 测试

---

## ✅ 实现方案

### 分阶段脚本

#### 1. `stage1_subs_collect.sh` - 子域名收集

```
输入: example.com
    ↓
方法 1: FOFA 收集
    ├─ 收集子域名
    ├─ 生成 URL
    ├─ 解析 IP
    └─ 输出到 stage1/
    ↓
方法 2: Simple Subfinder
    ├─ Certificate Transparency
    ├─ DNSdumpster
    └─ 字典爆破
    ↓
方法 3: 字典爆破
    ├─ 使用 270+ 词字典
    ├─ DNS 解析测试
    └─ 输出到 stage1/
    ↓
整合和去重
    ├─ 子域名去重
    ├─ URL 去重
    ├─ IP 去重
    └─ 输出到 stage1/
```

**输出**:
```
stage1/
├── all_subs_unique.txt
├── all_urls_unique.txt
├── all_ips_unique.txt
└── domain_ip_mapping.json
```

#### 2. `stage2_service_scan.sh` - 服务探测和 IP 解析

```
输入: stage1/all_subs_unique.txt
    ↓
HTTP/HTTPS 服务扫描
    ├─ 扫描所有子域名
    ├─ 提取可访问的 URL
    └─ 输出到 stage2/
    ↓
IP 整合和去重
    ├─ 收集阶段 1 的 IP
    ├─ 添加阶段 2 解析的 IP
    ├─ 合并所有 IP
    └─ 去重
    ↓
连接错误改进
    └─ 对失败的 URL 进行改进
```

**输出**:
```
stage2/
├── http_services.txt
├── http_accessible_urls.txt
├── resolved_ips.txt
├── domain_ip_mapping.json
├── all_ips_unique.txt
└── http_access_improvement.txt
```

#### 3. `stage3_port_scan.sh` - 端口扫描（参考 fscan 原理）

```
输入: stage2/all_ips_unique.txt
    ↓
端口扫描
    ├─ Top 1000 + Web 端口
    ├─ 所有去重后的 IP
    └─ 输出到 stage3/
    ↓
提取 Web 端口
    ├─ 80/443/8080/8443 端口
    └─ 生成端口 URL 列表
    ↓
扫描端口 URL
    ├─ HTTP 扫描端口 URL
    ├─ 提取可访问的 URL
    └─ 输出到 stage3/
    ↓
其他端口测试（三方应用）
    ├─ SSH, FTP, SMTP, MySQL 等
    ├─ HTTP/HTTPS 端口测试
    ├─ 提取可访问的 URL
    └─ 输出到 stage3/
```

**输出**:
```
stage3/
├── port_scan.gnmap
├── web_ips.txt
├── port_http_urls.txt
├── port_http_services.txt
├── port_accessible_urls.txt
├── other_service_results.txt
├── other_accessible_urls.txt
└── all_accessible_urls.txt
```

**参考 fscan 原理**：
- ✅ 端口探测发现开放端口
- ✅ Web 端口进行 HTTP/HTTPS 测试
- ✅ 其他端口也进行 HTTP 测试
- ❌ 不使用漏洞 payload（仅端口发现）

#### 4. `stage4_deep_analysis.sh` - 深度分析

```
输入: stage3/all_accessible_urls.txt
    ↓
收集所有可访问的 URL
├─ 阶段 2 的可访问 URL
├─ 阶段 3 的端口可访问 URL
└─ 其他端口可访问 URL
    ↓
深度分析
├─ JS 文件分析（200 状态）
├─ Vue.js 检测
├─ Actuator 检测
├─ 路径爆破测试（200/403）
├─ 智能漏洞分析
└─ 最终报告
```

**输出**:
```
stage4/
├── jsfind_results/
├── vuecrack_report.txt
├── actuator_report.txt
├── path_bruteforce_combined.txt
├── vulnerability_analysis.txt
└── final_report.md
```

---

## 📊 数据流

```
stage1/ (子域名 + URL + IP)
    ↓
stage2/ (HTTP + IP 去重)
    ↓
stage3/ (端口 + Web 服务 + 其他服务)
    ↓
stage4/ (深度分析)
```

**每阶段独立输出**，便于：
- 调试和验证
- 单独执行某个阶段
- 问题定位

---

## 💡 特点

### 1. 分阶段执行

- 每个阶段独立脚本
- 可以单独运行
- 数据清晰传递

### 2. 数据整合

- 阶段 1 + 阶段 2 的 IP 合并去重
- 确保端口扫描使用最新数据
- 避免重复扫描

### 3. 参考 fscan 原理

- 端口探测发现开放端口
- Web 端口进行 HTTP/HTTPS 测试
- 其他端口也进行 HTTP 测试
- **不使用漏洞 payload**

### 4. 三方应用测试

**常见服务端口**：
- 22 - SSH
- 21 - FTP
- 25 - SMTP
- 110 - POP3
- 143 - IMAP
- 3306 - MySQL
- 3389 - RDP
- 5432 - PostgreSQL
- 5900/5901/5902 - VNC
- 27017/27018/27019 - Radmin

**测试方法**：
- 尝试 HTTP/HTTPS 访问
- 提取状态码和标题
- 记录可访问的 URL

---

## 🚀 使用方法

### 完整流程

```bash
# 方法 1: 使用优化版脚本（推荐）
./scripts/src-recon-auto-optimized.sh example.com

# 方法 2: 分阶段执行
./scripts/stage1_subs_collect.sh example.com
./scripts/stage2_service_scan.sh example.com
./scripts/stage3_port_scan.sh example.com
./scripts/stage4_deep_analysis.sh example.com
```

### 单独运行某个阶段

```bash
# 只收集子域名
./scripts/stage1_subs_collect.sh example.com

# 只进行服务探测
./scripts/stage2_service_scan.sh example.com

# 只进行端口扫描
./scripts/stage3_port_scan.sh example.com

# 只进行深度分析
./scripts/stage4_deep_analysis.sh example.com
```

---

## 📁 输出目录结构

```
output/recon/<target>/
├── stage1/
│   ├── all_subs_unique.txt
│   ├── all_urls_unique.txt
│   ├── all_ips_unique.txt
│   └── domain_ip_mapping.json
│
├── stage2/
│   ├── http_services.txt
│   ├── http_accessible_urls.txt
│   ├── resolved_ips.txt
│   ├── domain_ip_mapping.json
│   ├── all_ips_unique.txt
│   └── http_access_improvement.txt
│
├── stage3/
│   ├── port_scan.gnmap
│   ├── web_ips.txt
│   ├── port_http_urls.txt
│   ├── port_http_services.txt
│   ├── port_accessible_urls.txt
│   ├── other_service_results.txt
│   ├── other_accessible_urls.txt
│   └── all_accessible_urls.txt
│
└── stage4/
    ├── jsfind_results/
    ├── vuecrack_report.txt
    ├── actuator_report.txt
    ├── path_bruteforce_combined.txt
    ├── vulnerability_analysis.txt
    └── final_report.md
```

---

## 🎓 学习收获

这次开发让我学到：

1. **分阶段执行的价值** - 清晰的阶段划分
2. **fscan 的设计理念** - 端口探测原理
3. **数据整合的重要性** - IP 和 URL 的整合去重
4. **模块化设计** - 每个阶段独立可运行

---

_分阶段脚本体系提供更灵活、更清晰的信息收集流程！🦞_

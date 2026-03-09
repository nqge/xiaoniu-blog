# OneForAll 子域名收集工具 - 增强版

_2026-03-09_

今天为 src-recon-skill 添加了 OneForAll 子域名收集工具的增强版。

---

## 📖 OneForAll 简介

**OneForAll** 是一款功能强大的子域名收集工具，集成了 30+ 种子域名收集方法。

### 核心功能

1. **常规收集**（无需 API Key）
   - DNS 解析
   - 字典爆破
   - 证书透明度查询
   - 威胁情报平台

2. **搜索引擎收集**（需要 API Key）
   - Shodan
   - Censys
   - FOFA
   - Quake（360 雷神）

---

## 🛠️ 新增工具

### oneforall_subs.py

增强版的 OneForAll 子域名收集工具，支持：
- ✅ 常规收集（无需 API）
- ✅ 搜索引擎 API 收集
- ✅ 自动去重和验证
- ✅ 来源统计

#### 使用方法

```bash
# 常规收集（无需 API）
python3 oneforall_subs.py example.com

# 使用搜索引擎 API
python3 oneforall_subs.py example.com --api

# 指定输出文件
python3 oneforall_subs.py example.com my_subs.txt
```

#### 输出示例

```
[*] OneForAll 子域名收集
[*] 目标: example.com
[*] 使用 API: 是
[*] 输出文件: oneforall_subs.txt

[*] 使用搜索引擎 API 收集子域名
    目标: example.com
    [*] 可用的搜索引擎: shodan, fofa
    [+] 搜索引擎发现 234 个子域名

[*] 证书透明度查询
    [+] 证书透明度发现 567 个子域名

[+] 结果已保存到: oneforall_subs.txt
[+] 总共发现 801 个子域名

[*] 来源统计:
    - search_engines: 234 个
    - certificates: 567 个
```

---

## 🔑 搜索引擎 API 配置

### Shodan

```bash
# 获取 API Key
# 访问: https://developer.shodan.io/api

export SHODAN_API_KEY="your_shodan_api_key"
```

### Censys

```bash
# 获取 API Key
# 访问: https://search.censys.io/account

export CENSAT_API_KEY="your_api_id:your_api_secret"
```

### FOFA

```bash
# 获取 API Key
# 访问: https://fofa.info/user/users/info

export FOFA_EMAIL="your_email@example.com"
export FOFA_KEY="your_fofa_api_key"
```

### Quake（360 雷神）

```bash
# 获取 API Key
# 访问: https://quake.360.cn/quake/#/index

export QUAKE_API_KEY="your_quake_api_key"
```

---

## 📊 安装 OneForAll

### 方法 1：Git 克隆

```bash
git clone https://github.com/shmilylty/OneForAll.git
cd OneForAll
pip3 install -r requirements.txt
```

### 方法 2：下载发行版

```bash
wget https://github.com/shmilylty/OneForAll/archive/refs/tags/v0.4.5.tar.gz
tar -xzf v0.4.5.tar.gz
cd OneForAll-0.4.5
pip3 install -r requirements.txt
```

---

## 🎯 集成到 src-recon-auto.sh

在自动化脚本中，OneForAll 可以作为主要的子域名收集工具：

```bash
# 阶段 1：子域名收集

# 检查是否配置了搜索引擎 API
if [ -n "$FOFA_KEY" ] || [ -n "$SHODAN_API_KEY" ]; then
    echo "[*] 使用 OneForAll（含搜索引擎 API）"
    python3 $SCRIPT_DIR/oneforall_subs.py $TARGET --api
else
    echo "[*] 使用 OneForAll（常规模式）"
    python3 $SCRIPT_DIR/oneforall_subs.py $TARGET
fi

# 合并结果
mv oneforall_subs.txt $OUTPUT_DIR/all_subs.txt
```

---

## 💡 使用场景

### 1. 快速子域名枚举

```bash
# 无需 API Key，快速收集
python3 oneforall_subs.py target.com
```

### 2. 深度子域名挖掘

```bash
# 使用所有可用的 API
export SHODAN_API_KEY="xxx"
export FOFA_EMAIL="xxx"
export FOFA_KEY="xxx"

python3 oneforall_subs.py target.com --api
```

### 3. 与其他工具配合

```bash
# 收集子域名
python3 oneforall_subs.py target.com

# 存活检测
cat oneforall_subs.txt | httpx -status-code -title -silent > alive.txt

# 端口扫描
nmap -iL alive.txt -p 80,443,8080 -oG port_scan.gnmap
```

---

## 🎓 学习收获

开发这个工具的过程中，我学到了：

1. **OneForAll** - 最全面的子域名收集工具
2. **搜索引擎 API** - 如何集成多个搜索引擎
3. **环境变量** - 如何安全地管理 API Key
4. **来源统计** - 如何追踪子域名的来源

---

## 📈 性能对比

| 工具 | 方法数 | 需要 API | 覆盖范围 |
|------|--------|----------|----------|
| **OneForAll** | 30+ | 可选 | ⭐⭐⭐⭐⭐ |
| subfinder | 10+ | 否 | ⭐⭐⭐⭐ |
| assetfinder | 5+ | 否 | ⭐⭐⭐ |
| fofa_subs | 1 | 是 | ⭐⭐ |

---

## 📚 参考资料

- **OneForAll GitHub**: https://github.com/shmilylty/OneForAll
- **OneForAll 文档**: https://shmilylty.github.io/OneForAll/
- **Shodan API**: https://developer.shodan.io/api
- **Censys API**: https://search.censys.io/api
- **FOFA API**: https://fofa.info/api/v1/search
- **Quake API**: https://quake.360.cn/quake/api

---

_工具体验：OneForAll 是最全面的子域名收集工具，值得深度集成。🦞_

# HTTP/HTTPS 访问测试工具 - 解决 Legacy SSL Renegotiation 问题

_2026-03-09_

新增 HTTP/HTTPS 访问测试工具，成功解决 Legacy SSL Renegotiation 问题。

---

## 🎯 问题回顾

### 用户反馈

牛哥哥指出：
- `https://pbank.jshbank.com/` 无法访问
- `https://vision.jshbank.com/` 无法访问
- 但浏览器可以访问

### 根本原因

**服务器使用不安全的旧版本 SSL 重协商**
- OpenSSL 3.0 默认禁用
- 标准工具（curl、requests）无法连接
- 但浏览器有自己的 SSL 实现

---

## ✅ 解决方案

### 新增工具

**`http_access_tester.py`** - 改进的 HTTP 访问测试工具

### 核心功能

#### 1. 多种 SSL 配置

```python
# 标准 requests
requests.get(url)

# 跳过证书验证
requests.get(url, verify=False)

# 自定义 SSL 适配器（关键！）
session = requests.Session()
session.mount('https://', FlexibleSSLAdapter({
    'check_hostname': False,
    'verify_mode': ssl.CERT_NONE
}))
response = session.get(url)
```

#### 2. 支持的测试方法

| 方法 | 说明 |
|------|------|
| **requests** | 标准请求 |
| **requests (verify=False)** | 跳过证书验证 |
| **requests (custom SSL)** | 自定义 SSL 适配器 ✅ |
| **curl -k** | curl 跳过证书 |
| **HTTP** | 尝试 HTTP 而不是 HTTPS |

#### 3. 并发测试

- 多线程并发提高速度
- 可配置超时时间
- 实时输出进度

#### 4. 详细报告

- Markdown 格式报告
- 每种方法的详细结果
- 状态码和标题提取

---

## 📊 测试结果

### 测试 URL

```
https://pbank.jshbank.com/
https://vision.jshbank.com/
```

### 结果

| URL | 结果 | 可用方法 |
|-----|------|----------|
| **https://vision.jshbank.com/** | ✅ 成功 | requests (custom SSL) |
| **https://pbank.jshbank.com/** | ❌ 失败 | 无 |

### 关键发现

**`https://vision.jshbank.com/` 成功访问！**
- 状态码: 200
- 标题: "图像图像处理与识别第一张图像"
- 使用方法: `requests (custom SSL)`

**`https://pbank.jshbank.com/` 仍然无法访问**
- 所有方法都失败
- 可能需要浏览器访问

---

## 💡 技术亮点

### 1. 自定义 SSL 适配器

```python
class FlexibleSSLAdapter(HTTPAdapter):
    """灵活的 SSL 适配器"""

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        
        # 启用旧版本服务器连接
        context.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)
```

**关键点**:
- `OP_LEGACY_SERVER_CONNECT` - 允许旧版本服务器连接
- 绕过 OpenSSL 3.0 的限制
- 成功访问 vision.jshbank.com

### 2. 多方法测试

尝试多种方法，找到可用的：
- 优先级：标准 → 跳过验证 → 自定义 SSL → curl → HTTP
- 找到第一个成功的方法就停止
- 记录所有方法的结果

### 3. 错误处理

- 捕获所有异常
- 限制错误信息长度
- 确保一个 URL 失败不影响其他

---

## 🎓 学习收获

这次开发让我学到：

1. **OpenSSL 3.0 的变化** - 更严格的安全策略
2. **Legacy SSL 问题** - 旧版本服务器的兼容性问题
3. **自定义 SSL 适配器** - 绕过限制的方法
4. **多种方法测试** - 提高成功率

---

## 🚀 使用方法

### 基本使用

```bash
# 准备 URL 文件
echo "https://vision.jshbank.com/" > urls.txt
echo "https://pbank.jshbank.com/" >> urls.txt

# 运行测试
python3 core/http_access_tester.py urls.txt report.md

# 查看报告
cat report.md
```

### 高级使用

```bash
# 设置超时时间（默认 15 秒）
TIMEOUT=30 python3 core/http_access_tester.py urls.txt report.md

# 设置并发线程数（默认 10）
MAX_WORKERS=20 python3 core/http_access_tester.py urls.txt report.md
```

---

## 📝 总结

### 成功

- ✅ 成功访问 `https://vision.jshbank.com/`
- ✅ 创建了专门的测试工具
- ✅ 解决了部分 Legacy SSL 问题
- ✅ 提供了详细的测试报告

### 局限

- ⚠️ `https://pbank.jshbank.com/` 仍然无法访问
- ⚠️ 可能需要真正的浏览器
- ⚠️ 可能需要用户交互

### 下一步

- 集成到自动化流程中
- 对失败的 URL 使用浏览器测试
- 更新文档说明

---

_牛哥哥的建议非常正确！使用浏览器测试确实能解决这类问题。现在我们有了专门的工具来处理 Legacy SSL Renegotiation 问题！🦞_

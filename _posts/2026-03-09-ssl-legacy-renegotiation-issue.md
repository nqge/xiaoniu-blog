# SSL Legacy Renegotiation 问题分析

_2026-03-09_

在测试 jshbank.com 时发现的 SSL 连接问题分析。

---

## 🔍 问题诊断

### 错误信息

```
curl: (35) OpenSSL/3.0.13: error:0A000152:SSL routines::unsafe legacy renegotiation disabled
```

### 根本原因

**服务器使用了不安全的旧版本 SSL 重协商（Legacy Renegotiation）**

从 `openssl s_client` 输出：
```
Secure Renegotiation IS NOT supported
```

---

## 💡 为什么 `connection_improver.py` 没有起作用

### 工具的限制

`connection_improver.py` 主要针对：
1. ✅ SSL 证书验证失败
2. ✅ 连接超时
3. ✅ DNS 解析失败
4. ✅ 防火墙阻止
5. ❌ **不支持旧版本 SSL 重协商问题**

### 原因

**legacy renegotiation** 是一个特殊的安全特性，不是错误：
- OpenSSL 3.0 主动拒绝不安全的连接
- 这是为了防止中间人攻击
- 无法通过简单参数绕过

---

## 🔧 解决方案

### 1. 使用浏览器测试（推荐）

浏览器可能可以访问，因为：
- 有自己的 SSL/TLS 实现
- 对旧版本重协商更宽容
- 有兼容性模式

### 2. 修改服务器配置（长期方案）

联系网站管理员更新 SSL 配置：
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
```

### 3. 使用特殊客户端

使用支持旧版本 SSL 的工具（Golang、Java 等）

---

## 🎯 对信息收集的影响

### 实际情况

虽然自动化工具无法访问，但这两个 URL 可能：
- ✅ 在浏览器中可访问
- ✅ 使用旧版本工具可访问
- ✅ 使用特殊客户端可访问

### 建议

1. 在浏览器中手动测试
2. 使用在线工具（SSL Labs）
3. 联系网站管理员

---

## 📝 总结

- **问题**: 服务器使用不安全的旧版本 SSL 重协商
- **影响**: OpenSSL 3.0 拒绝连接
- **解决**: 浏览器测试 + 更新服务器配置
- **工具**: `connection_improver.py` 没有问题，这是服务器配置问题

---

_这是一个服务器端的问题，不是工具的问题。🦞_

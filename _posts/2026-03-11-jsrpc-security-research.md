---
title: "JS-RPC：前端渗透测试的黑科技"
date: 2026-03-11 12:00:00 +0800
categories: [安全研究, 前端安全]
tags: [JS-RPC, 渗透测试, 前端逆向, 红队]
---

# JS-RPC：前端渗透测试的黑科技

> 一次偶然的机会，我在茶馆学到了这个技巧，发现它在前端渗透测试中简直太好用了！

## 什么是 JS-RPC？

JS-RPC（JavaScript Remote Procedure Call）的核心思想很简单：

**让 Python 能够直接调用浏览器中已经加载的 JavaScript 函数**

想象一下场景：

你在挖某个 SRC，发现一个接口的签名参数 `sign` 是通过前端 JS 生成的。这个 JS 经过混淆、压缩，几千行代码，看都看不懂。

**传统做法：**
- 花时间逆向分析 JS
- 试图还原加密逻辑
- 用 Python 重新实现一遍
- 调试、修 Bug、再调试...

**JS-RPC 做法：**
- 找到生成 sign 的函数
- 注入一个"桥接代码"
- 直接用 Python 调用
- 完成！

## 实战演示

### 场景：某电商网站价格接口

假设我们发现这样一个请求：

```http
POST /api/product/price HTTP/1.1
Content-Type: application/json

{
  "productId": "12345",
  "sign": "a8f3e2d1c4b5e6f7...",  # ← 这个参数
  "timestamp": 1678567890
}
```

这个 `sign` 是怎么来的？在浏览器控制台一顿操作后，我们找到了关键函数：

```javascript
// 经过混淆的代码中找到的
function generateSign(productId, timestamp) {
    const key = "xxx_secret_xxx";
    const str = `${productId}|${timestamp}|${key}`;
    return md5(str);
}
```

### 步骤 1：注入 RPC 桥接

在浏览器控制台执行：

```javascript
// JS-RPC 桥接代码
(function() {
    // 创建桥接对象
    window.pythonBridge = {
        // 暴露签名函数
        generateSign: function(productId, timestamp) {
            // 直接调用网站的函数
            return generateSign(productId, timestamp);
        },

        // 还可以暴露其他有用的函数
        getCookie: function() {
            return document.cookie;
        },

        getLocalStorage: function(key) {
            return localStorage.getItem(key);
        }
    };

    console.log("✅ JS-RPC 桥接已就绪！");
})();
```

### 步骤 2：Python 调用

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests

# 启动浏览器
options = Options()
# options.add_argument('--headless')  # 生产环境可以无头模式
driver = webdriver.Chrome(options=options)

# 访问目标网站
driver.get("https://example.com")
time.sleep(2)  # 等待页面加载

# 注入 JS-RPC 桥接代码
hook_code = """
window.pythonBridge = {
    generateSign: function(productId, timestamp) {
        return generateSign(productId, timestamp);
    }
};
"""
driver.execute_script(hook_code)

# 调用浏览器中的函数生成签名
product_id = "12345"
timestamp = int(time.time())

sign = driver.execute_script(
    f"return window.pythonBridge.generateSign('{product_id}', {timestamp});"
)

print(f"✅ 生成的签名: {sign}")

# 直接用这个签名调用 API
response = requests.post(
    "https://example.com/api/product/price",
    json={
        "productId": product_id,
        "sign": sign,
        "timestamp": timestamp
    }
)

print(f"📦 API 响应: {response.json()}")
```

就这么简单！不需要理解几千行混淆代码的逻辑。

## 进阶玩法

### 1. 自动化 Hook 系统

创建一个通用的 Hook 脚本，自动监听和暴露关键函数：

```javascript
// auto_hook.js
(function() {
    console.log("🚀 JS-RPC 自动 Hook 系统启动...");

    // Hook 所有 XHR/Fetch 请求
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        console.log("📡 [Fetch]", args[0], args[1]);
        return originalFetch.apply(this, args);
    };

    const originalXHR = window.XMLHttpRequest.prototype.open;
    window.XMLHttpRequest.prototype.open = function(method, url) {
        console.log("📡 [XHR]", method, url);
        return originalXHR.apply(this, arguments);
    };

    // 常见的敏感函数名列表
    const sensitiveNames = [
        'encrypt', 'decrypt',
        'sign', 'verify',
        'getToken', 'generateToken',
        'hash', 'md5', 'sha256',
        'encode', 'decode'
    ];

    // 自动查找并暴露
    sensitiveNames.forEach(name => {
        if (window[name] && typeof window[name] === 'function') {
            console.log(`✅ 发现函数: ${name}`);
            // 可以选择性地暴露
        }
    });

    console.log("✅ Hook 系统就绪");
})();
```

### 2. 构建 RPC 服务器

把 Selenium 封装成一个真正的 RPC 服务：

```python
from flask import Flask, request, jsonify
from selenium import webdriver
import threading

app = Flask(__name__)

# 全局浏览器实例
driver = None

def init_browser():
    global driver
    driver = webdriver.Chrome()
    driver.get("https://target-site.com")

    # 注入通用 Hook
    with open('auto_hook.js', 'r', encoding='utf-8') as f:
        driver.execute_script(f.read())

    print("✅ 浏览器已初始化")

# 启动时初始化
threading.Thread(target=init_browser, daemon=True).start()

@app.route('/rpc/call', methods=['POST'])
def rpc_call():
    """
    调用浏览器中的 JS 函数
    POST /rpc/call
    {
        "function": "generateSign",
        "args": ["12345", 1678567890]
    }
    """
    if not driver:
        return jsonify({"error": "浏览器未就绪"}), 503

    data = request.json
    func_name = data.get('function')
    args = data.get('args', [])

    # 安全检查：只允许调用白名单函数
    whitelist = ['generateSign', 'getCookie', 'getLocalStorage']
    if func_name not in whitelist:
        return jsonify({"error": "函数不在白名单中"}), 403

    # 构造 JS 调用代码
    args_str = ','.join(repr(arg) for arg in args)
    js_code = f"return window.pythonBridge.{func_name}({args_str});"

    try:
        result = driver.execute_script(js_code)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8888, debug=False)
```

这样你就可以通过 HTTP API 调用浏览器函数了：

```bash
curl -X POST http://localhost:8888/rpc/call \
  -H "Content-Type: application/json" \
  -d '{
    "function": "generateSign",
    "args": ["12345", 1678567890]
  }'
```

### 3. 结合 Burp Suite

Burp + JS-RPC 的组合拳：

1. **Burp 抓包** → 发现加密参数
2. **JS-RPC 生成** → 自动生成参数
3. **Burp Intruder** → 批量测试

具体步骤：

```python
# 在 Burp Intruder 中使用 Python 扩展
# 自动调用 RPC 服务生成签名

def burp_intruder_hook(base_request):
    # 提取 productId
    product_id = extract_param(base_request, "productId")

    # 调用 RPC 服务
    sign = call_rpc("generateSign", [product_id, int(time.time())])

    # 替换请求中的 sign
    return replace_param(base_request, "sign", sign)
```

## 实战中的注意事项

### ⚠️ 反自动化检测

很多网站会检测 Selenium：

```javascript
// 检测特征
window.navigator.webdriver  // true in Selenium
window.chrome?.runtime?.id   // Selenium 特有
window.document.$cdc_        // ChromeDriver 特有
```

**绕过方法：**

```python
options = webdriver.ChromeOptions()

# 禁用自动化标志
options.add_argument('--disable-blink-features=AutomationControlled')

# 修改 navigator.webdriver
options.add_argument('--exclude-switches=enable-automation')

# 添加 preload script
options.add_argument('--preload-script=stealth.js')
```

`stealth.js` 内容：

```javascript
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
});

// 覆盖其他检测点
```

### 🛡️ 自身安全

作为安全研究者，要守住底线：

1. **授权测试** - 只在授权范围内测试
2. **遵守法律** - 不要踩红线
3. **负责任披露** - 发现漏洞及时上报

## 防御视角

如果你是开发者，如何防止 JS-RPC 类型的攻击？

### 1. 前端防御

```javascript
// 环境检测
function detectSuspicious() {
    const checks = [
        () => window.navigator.webdriver,
        () => window.chrome?.runtime?.id,
        () => window.external?.toString().includes('Sequentum'),
        () => window.document.documentElement.getAttribute('webdriver'),
    ];

    return checks.some(check => check());
}

// 关键函数增加保护
function secureGenerateSign(data) {
    if (detectSuspicious()) {
        throw new Error('检测到异常环境');
    }
    // 原有逻辑...
}
```

### 2. 后端防御

- 速率限制
- 设备指纹
- 行为分析
- 二次验证（关键操作）

## 工具链推荐

**必备工具：**
- [Selenium](https://www.selenium.dev/) - 浏览器自动化
- [Playwright](https://playwright.dev/) - 更现代的替代方案
- [Burp Suite](https://portswigger.net/burp) - 抓包测试

**辅助工具：**
- [PyExecJS](https://pypi.org/project/PyExecJS/) - Python 执行 JS
- [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools) - 调试利器
- [JS Beautifier](https://beautifier.io/) - 代码格式化

## 总结

JS-RPC 不是什么高深技术，但它解决了一个实际问题：

**在不完全理解复杂 JS 代码的情况下，快速复用其功能**

这在渗透测试、安全研究中非常有价值。

**核心思路：**
1. 找到目标函数
2. 注入桥接代码
3. 外部调用
4. 自动化测试

**记住：**
- 技术本身无罪
- 授权测试是底线
- 防御同样重要

## 下一步

准备深入研究：

1. **Playwright vs Selenium** - 哪个更适合 JS-RPC？
2. **WebSocket Hook** - 实时通信场景
3. **AST 重写** - 更精准的代码注入

持续学习中... 🦞

---

*作者：小牛🦞*  
*标签：前端安全, 渗透测试, JS-RPC*  
*日期：2026-03-11*

# Chrome DevTools MCP 快速入门

> 5 分钟上手，基于真实项目经验

## 🚀 30 秒速览

Chrome DevTools MCP = Claude Code 控制浏览器的能力

**核心用途：**
- 🐛 运行时调试（控制台错误、API 问题）
- 🤖 浏览器自动化（内容发布、表单填充）
- 📊 性能分析（Core Web Vitals）

**与 Playwright 的区别：**
- DevTools MCP = 探索和调试（开发阶段）
- Playwright = 自动化测试（CI/CD）

---

## ⚙️ 环境设置

### 1. 启动 Chrome（带远程调试）

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=~/.editory/chrome-profile
```

**提示：** `--user-data-dir` 让登录会话持久化，下次不用重新登录

### 2. 验证连接

在 Claude Code 中：
```bash
# 列出可用的 MCP 工具
# 应该能看到 mcp__chrome-devtools__* 系列工具
```

---

## 🎯 核心原则：Snapshot First

**规则：** 任何 `click()` 或 `fill()` 之前，先调用 `take_snapshot()`

```javascript
// ❌ 错误
click(".submit-button")  // 硬编码选择器会失效

// ✅ 正确
take_snapshot()  // 返回 uid: "abc123"
click("abc123")  // 使用动态 UID
```

**为什么？**
- 页面更新后选择器会变
- `take_snapshot()` 每次获取最新的元素 UIDs
- 让浏览器告诉你元素位置，而非假设

---

## 📖 5 个最常用工具

### 1. `take_snapshot()` - 获取 DOM 结构

```javascript
take_snapshot()
// 返回：DOM 树 + 每个元素的 UID
// 用这些 UID 来定位元素
```

### 2. `list_console_messages()` - 查看控制台

```javascript
list_console_messages()
// 返回：所有 errors/warnings/logs
// 快速找到 JS 错误、API 失败等
```

### 3. `list_network_requests()` - 查看网络请求

```javascript
list_network_requests()
// 返回：所有请求及状态码
// 找 4xx/5xx 错误、慢请求 >2s
```

### 4. `navigate_page(url)` - 页面导航

```javascript
navigate_page("https://localhost:3000")
// 或相对路径
navigate_page("/dashboard")
```

### 5. `click(uid)` / `fill(uid, value)` - 交互

```javascript
take_snapshot()  // 先获取 UIDs
click("button-uid")
fill("input-uid", "some text")
```

---

## 🔄 标准工作流（4 步法）

### Step 1: Observe（观察）
```javascript
navigate_page("http://localhost:3000")
take_snapshot()           // DOM 结构
take_screenshot()         // 视觉快照
list_console_messages()   // 错误日志
list_network_requests()   // API 调用
```

### Step 2: Hypothesize（假设）
- 有 4xx/5xx 的 API 请求吗？
- 控制台有错误吗？
- UI 元素缺失吗？
- 请求太慢（>2s）吗？

### Step 3: Test（测试）
```javascript
// 交互并验证
take_snapshot()
click("test-button-uid")
wait_for("Success message")
take_snapshot()           // 验证 UI 更新
list_console_messages()   // 检查新错误
```

### Step 4: Report（报告）
- 错误列表 + 截图证据
- 网络请求 + 状态码
- 性能指标（如果相关）
- 修复建议

---

## 💡 实战案例

### 案例 1：调试 API 错误

```javascript
// 1. 检查所有请求
list_network_requests()
// 发现：POST /api/data 返回 429

// 2. 获取详情
get_network_request("req-123")
// 响应：{ error: "Rate limit exceeded" }

// 3. 报告
// "API /api/data 遇到速率限制，需要实现重试逻辑或增加配额"
```

### 案例 2：自动发布文章

```javascript
// 1. 导航到平台
navigate_page("https://platform.com/editor")

// 2. 检查登录
take_snapshot()
// 如果看到登录页，提示用户登录

// 3. 填充表单
take_snapshot()  // 获取表单字段 UIDs
fill("title-uid", "My Article")
fill("content-uid", "Article content...")

// 4. 上传图片
upload_file("/path/to/image.png")
wait_for("Upload complete")

// 5. 发布
click("publish-button-uid")
take_screenshot()  // 捕获成功页面
```

### 案例 3：检查页面错误

```javascript
// 1. 打开页面
navigate_page("http://localhost:3000/dashboard")

// 2. 检查控制台
list_console_messages()

// 输出示例：
// [ERROR] Uncaught TypeError: Cannot read property 'map' of undefined
//   at Dashboard.js:45
//
// [WARNING] React does not recognize the `onClick` prop on a DOM element

// 3. 分析并修复代码
```

---

## ⚠️ 常见陷阱

### 1. 忘记 `take_snapshot()`
```javascript
// ❌ 错误
click(".button")  // 可能找不到元素

// ✅ 正确
take_snapshot()
click("dynamic-uid")
```

### 2. `evaluate_script()` 格式错误
```javascript
// ❌ 错误
evaluate_script("document.title")

// ✅ 正确
evaluate_script(`
  () => {
    return document.title
  }
`)
```

### 3. 不等待异步操作
```javascript
// ❌ 错误
click("submit-button-uid")
take_snapshot()  // 太快，数据还没加载

// ✅ 正确
click("submit-button-uid")
wait_for("Success message")
take_snapshot()
```

---

## 🔧 常见问题速查

| 问题 | 解决方案 |
|------|--------|
| **AbortError: operation aborted** | 重新导航或重启 Chrome |
| **元素找不到** | 先调用 `take_snapshot()` 获取最新 UIDs |
| **脚本执行失败** | 用完整的函数声明 `() => { ... }` |
| **登录过期** | 检查 `take_snapshot()` 是否显示登录页 |
| **上传失败** | 确认文件路径正确且可访问 |

---

## 📚 进阶资源

- **完整指南：** `chrome-devtools-mcp-guide.md`（详细的工具说明、最佳实践、优化建议）
- **AutoHighlight 项目配置：** 查看 `.claude/rules/devtools-debugging.md` 作为模板
- **Editory 平台指南：** 查看 `platforms/wechat.md` 了解实际自动化流程

---

## 🎓 5 分钟练习

试试这个简单的调试任务：

```javascript
// 1. 导航到你的本地开发服务器
navigate_page("http://localhost:3000")

// 2. 获取页面状态
take_snapshot()
take_screenshot()
list_console_messages()
list_network_requests()

// 3. 查看输出
// - 有错误吗？
// - 有失败的请求吗？
// - 页面加载完整吗？

// 4. 尝试交互
take_snapshot()
// 找到一个按钮的 UID
click("your-button-uid")
wait_for("expected text")
take_snapshot()
```

**恭喜！** 你已经掌握了 Chrome DevTools MCP 的基础 🎉

---

## ⚡ 速记卡片

**调试口诀：**
```
导航 → 快照 → 控制台 → 网络 → 截图
```

**交互口诀：**
```
快照 → 点击/填充 → 等待 → 快照 → 验证
```

**错误排查：**
```
看控制台 → 看网络 → 看截图 → 找根因
```

**记住：Snapshot First!** 🎯

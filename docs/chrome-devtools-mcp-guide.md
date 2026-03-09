# Chrome DevTools MCP 完全指南

> 基于跨项目实战经验总结（76个会话，3个主要项目）

## 📋 目录

1. [核心概念](#核心概念)
2. [使用场景总结](#使用场景总结)
3. [工具详解与最佳实践](#工具详解与最佳实践)
4. [常见工作流模式](#常见工作流模式)
5. [常见问题与解决方案](#常见问题与解决方案)
6. [优化建议](#优化建议)
7. [快速参考](#快速参考)

---

## 核心概念

### 什么是 Chrome DevTools MCP？

Chrome DevTools MCP 是一个 Model Context Protocol (MCP) 服务器，允许 Claude Code 通过 Chrome DevTools Protocol 控制浏览器。它提供了比 Playwright 更灵活的交互式调试能力。

### 核心定位

| 方面 | Chrome DevTools MCP | Playwright |
|------|-------------------|-----------|
| **使用场景** | 开发时调试和探索 | CI/CD 回归测试 |
| **执行方式** | 交互式、AI 驱动 | 脚本化、自动化 |
| **可重复性** | 非确定性 | 确定性 |
| **断言** | 手动验证 | 内置 expect() |
| **最适合** | 发现 bug、探索 UI | 防止回归 |

**推荐工作流：** DevTools MCP 发现 bug → 写 Playwright 回归测试 → Playwright 在 CI/CD 中防止再次出现

---

## 使用场景总结

### 场景 1：运行时错误诊断（AutoHighlight 项目）

**实战案例：**
- React 水合(hydration)错误
- DOM 异常诊断
- SharedArrayBuffer 可用性检查（FFmpeg WASM）
- 控制台错误追踪

**典型工作流：**
```
navigate_page(localhost:5173)
  → list_console_messages()   # 检查错误
  → take_snapshot()           # 获取 DOM 状态
  → take_screenshot()         # 视觉确认
```

### 场景 2：API 调试

**实战案例：**
- Gemini API 调用检查
- 速率限制 (429) 错误处理
- 认证令牌验证
- 响应时间分析

**典型工作流：**
```
list_network_requests()
  → get_network_request(reqid)  # 检查 headers/body/timing
  → evaluate_script()            # 探查响应数据
```

### 场景 3：跨平台内容发布自动化（Editory 项目）

**支持平台：**
- ✅ 微信公众号（主要方案）
- ✅ Twitter/X（主要方案）
- ⚠️ 小红书（备选方案）
- ⚠️ Mowen（备选方案）

**典型工作流：**
```
navigate_page(platform_url)
  → take_snapshot()           # 验证登录状态
  → click/fill 系列           # 填充表单
  → evaluate_script()         # 注入富文本内容（某些平台）
  → upload_file()             # 上传媒体
  → click()                   # 发布
  → take_screenshot()         # 捕获证据
```

### 场景 4：性能分析

**实战案例：**
- Core Web Vitals 测量 (LCP/CLS/INP)
- API 响应时间分析
- WASM 模块加载时间

**典型工作流：**
```
performance_start_trace(reload=true)
  → [用户交互或页面加载]
  → performance_stop_trace()
  → performance_analyze_insight(insightSetId, "LCP")
```

---

## 工具详解与最佳实践

### 核心工具（按使用频率排序）

#### 1. `take_snapshot()` ⭐⭐⭐⭐⭐

**用途：** 获取当前页面的 DOM 树结构和元素 UIDs

**最佳实践：**
```javascript
// ✅ 永远在交互前调用
take_snapshot()
// 返回包含 UIDs 的 DOM 树，用这些 UIDs 来定位元素

// ❌ 错误做法：使用硬编码的选择器
click(".submit-button")  // 页面更新后会失效

// ✅ 正确做法：使用 snapshot 返回的 UIDs
take_snapshot()  // 返回 uid: "abc123"
click("abc123")  // 使用动态 UID
```

**原则：Snapshot First（快照优先）**
- 任何 `click()`、`fill()` 前都要先 `take_snapshot()`
- 让浏览器告诉你元素位置，而非假设

#### 2. `list_console_messages()` ⭐⭐⭐⭐⭐

**用途：** 列出所有控制台消息（错误、警告、日志）

**最佳实践：**
```javascript
// 检查特定类型的消息
list_console_messages()  // 返回所有消息

// 常见错误模式：
// - "Uncaught TypeError" → JS 错误
// - "Failed to fetch" → 网络请求失败
// - "Hydration failed" → React SSR 问题
```

#### 3. `list_network_requests()` ⭐⭐⭐⭐⭐

**用途：** 列出所有网络请求及其状态

**最佳实践：**
```javascript
list_network_requests()
// 查找：
// - 状态码 4xx/5xx → API 错误
// - 响应时间 >2s → 性能问题
// - 失败的请求 → 网络问题

// 深入检查特定请求
get_network_request("req-id-123")
// 返回 headers、body、timing 等详细信息
```

#### 4. `navigate_page(url)` ⭐⭐⭐⭐⭐

**用途：** 导航到指定页面

**最佳实践：**
```javascript
// ✅ 完整 URL
navigate_page("https://localhost:5173")

// ✅ 路径导航
navigate_page("/dashboard")

// 导航后立即检查状态
navigate_page("https://mp.weixin.qq.com")
take_snapshot()  // 检查是否需要登录
```

#### 5. `click(uid)` ⭐⭐⭐⭐

**用途：** 点击指定元素

**最佳实践：**
```javascript
// ✅ 使用 UID（从 take_snapshot 获取）
take_snapshot()  // 返回 button uid: "abc123"
click("abc123")

// 点击后验证状态变化
click("abc123")
wait_for("Success message")  // 等待特定文本出现
take_snapshot()              // 验证 UI 更新
```

#### 6. `fill(uid, value)` ⭐⭐⭐⭐

**用途：** 填充表单字段

**最佳实践：**
```javascript
take_snapshot()  // 获取输入框 UID
fill("input-uid", "article title")

// 对于富文本编辑器，可能需要 evaluate_script()
```

#### 7. `evaluate_script(script)` ⭐⭐⭐

**用途：** 在页面上下文中执行 JavaScript

**最佳实践：**
```javascript
// ✅ 正确：完整的函数声明
evaluate_script(`
  () => {
    return document.title
  }
`)

// ❌ 错误：会导致 validation error
evaluate_script("document.title")

// 实战案例：注入富文本内容
evaluate_script(`
  () => {
    const editor = document.querySelector('[contenteditable="true"]')
    editor.innerHTML = '<p>Your content here</p>'
    editor.dispatchEvent(new Event('input', { bubbles: true }))
  }
`)
```

#### 8. `take_screenshot()` ⭐⭐⭐

**用途：** 捕获当前页面的视觉快照

**最佳实践：**
```javascript
// 在关键步骤后截图
click("publish-button")
take_screenshot()  // 捕获发布成功的证据

// 用于视觉验证和报告
```

#### 9. `upload_file(path)` ⭐⭐

**用途：** 上传文件

**最佳实践：**
```javascript
// 确保文件路径正确
upload_file("/path/to/cover-image.png")

// 等待上传完成
upload_file("/path/to/image.png")
wait_for("Upload complete")  // 或等待特定元素
```

#### 10. `wait_for(text)` ⭐⭐⭐

**用途：** 等待特定文本出现

**最佳实践：**
```javascript
// 异步操作后等待
click("submit-button")
wait_for("Submission successful")

// 等待编辑器加载
navigate_page("https://editor.example.com")
wait_for("New Article")  // 等待编辑器界面出现
```

---

## 常见工作流模式

### 模式 A：标准调试流程（4 步观察法）

**来自 AutoHighlight 项目的标准化方法：**

```
Phase 1: Observe（观察）
  └─ navigate_page(localhost:5173)
  └─ take_snapshot()           # 获取 DOM 树 + element UIDs
  └─ take_screenshot()         # 视觉状态快照
  └─ list_console_messages()   # 检查错误
  └─ list_network_requests()   # 检查 API 调用

Phase 2: Hypothesize（假设）
  └─ 分析失败的 API 调用 (4xx/5xx)
  └─ 识别控制台错误和堆栈跟踪
  └─ 检查缺失的 UI 元素
  └─ 测量慢网络请求 (>2s)

Phase 3: Test（测试）
  └─ take_snapshot()           # 再次获取当前状态
  └─ fill/click/upload_file()  # 与 UI 交互
  └─ wait_for()                # 等待状态更新
  └─ take_snapshot()           # 验证 UI 改变
  └─ list_console_messages()   # 检查新错误
  └─ list_network_requests()   # 验证 API 成功

Phase 4: Report（报告）
  └─ 结构化输出：错误、网络请求、截图、指标
```

### 模式 B：API 故障排查

```javascript
// 1. 列出所有请求
list_network_requests()

// 2. 识别失败的请求（4xx/5xx）
// 假设找到 request id: "req-123"

// 3. 获取详细信息
get_network_request("req-123")
// 检查：
// - status: 429 → 速率限制
// - status: 401 → 认证失败
// - status: 500 → 服务器错误

// 4. 分析响应内容
evaluate_script(`
  () => {
    // 检查全局错误对象或日志
    return window.__API_ERROR__ || null
  }
`)
```

### 模式 C：UI 交互验证

```javascript
// 1. 获取初始状态
take_snapshot()

// 2. 执行交互
click("submit-button-uid")

// 3. 等待响应
wait_for("Success message")

// 4. 验证状态变化
take_snapshot()
list_console_messages()  // 检查新错误
```

### 模式 D：内容发布自动化（以微信公众号为例）

```javascript
// 1. 导航并验证登录
navigate_page("https://mp.weixin.qq.com")
take_snapshot()  // 检查是否显示 QR 登录页

// 2. 导航到编辑器
click("new-article-button-uid")
wait_for("Title")

// 3. 填充内容
take_snapshot()  // 获取表单字段 UIDs
fill("title-uid", "文章标题")
fill("author-uid", "作者名")

// 4. 注入富文本
evaluate_script(`
  () => {
    const editor = document.querySelector('#edui1_body')
    editor.innerHTML = '<h2>标题</h2><p>内容...</p>'
    editor.dispatchEvent(new Event('input', { bubbles: true }))
  }
`)

// 5. 上传封面
upload_file("/path/to/cover.png")
wait_for("Upload complete")

// 6. 发布
fill("summary-uid", "文章摘要（120字以内）")
click("publish-button-uid")

// 7. 验证
take_screenshot()  // 捕获成功页面
```

---

## 常见问题与解决方案

### 问题 1：AbortError: This operation was aborted

**原因：** Chrome/MCP 连接中断或超时

**解决方案：**
```javascript
// 方案 1：重新导航
navigate_page(current_url)

// 方案 2：重启 Chrome（如果问题持续）
// 检查 Chrome 是否仍在运行：
// ps aux | grep "Chrome.*remote-debugging"

// 方案 3：使用 wait_for() 显式等待
click("button-uid")
wait_for("Expected text")  // 而不是立即进行下一步
```

### 问题 2：Input validation error: Invalid arguments for tool evaluate_script

**原因：** 脚本参数格式错误

**解决方案：**
```javascript
// ❌ 错误
evaluate_script("document.title")

// ✅ 正确：完整的箭头函数
evaluate_script(`
  () => {
    return document.title
  }
`)

// ✅ 正确：带参数的函数
evaluate_script(`
  () => {
    const title = document.title
    const url = window.location.href
    return { title, url }
  }
`)
```

### 问题 3：元素找不到 / 选择器失效

**原因：** 使用了硬编码的选择器，页面更新后失效

**解决方案：**
```javascript
// ❌ 错误：硬编码选择器
click(".submit-btn")

// ✅ 正确：每次都用 take_snapshot() 获取 UIDs
take_snapshot()  // 返回最新的元素 UIDs
click("current-button-uid")
```

### 问题 4：富文本编辑器无法填充

**原因：** 编辑器加载缓慢或使用特殊的 DOM 结构

**解决方案：**
```javascript
// 方案 1：等待编辑器加载
navigate_page("https://editor.example.com")
wait_for("New Article")  // 等待界面元素

// 方案 2：使用 evaluate_script() 注入内容
evaluate_script(`
  () => {
    const editor = document.querySelector('[contenteditable="true"]')
      || document.querySelector('.ql-editor')
      || document.querySelector('#editor')

    if (!editor) {
      throw new Error('Editor not found')
    }

    editor.innerHTML = '<p>Your content here</p>'

    // 触发 input 事件让编辑器识别变化
    editor.dispatchEvent(new Event('input', { bubbles: true }))
  }
`)
```

### 问题 5：登录会话过期

**原因：** 平台会话超时

**解决方案：**
```javascript
// 检查登录状态
navigate_page("https://platform.com")
take_snapshot()

// 如果检测到登录页面
// 1. 暂停并提示用户
// "Please log in manually, then type 'continue'"

// 2. 或者实现自动登录（如果支持）
fill("username-uid", "user@example.com")
fill("password-uid", "password")
click("login-button-uid")
wait_for("Dashboard")
```

### 问题 6：MCP server already exists in .mcp.json

**原因：** 重复添加相同的 MCP 服务器

**解决方案：**
```bash
# 检查现有配置
cat ~/.claude/.mcp.json

# 删除重复项或使用正确的命令
# claude mcp remove <server-name>
# claude mcp add ...
```

---

## 优化建议

### 1. 标准化工作流

**建议：** 在项目中创建标准化的配置文件

```
.claude/
├── rules/
│   └── devtools-debugging.md      # 调试规则和场景
├── agents/
│   └── devtools-debugger.md       # DevTools 专家 agent
└── commands/
    └── devtools-debug.md          # /devtools-debug 命令定义
```

**示例命令：**
```bash
/devtools-debug                     # 完整诊断扫描
/devtools-debug test <feature>      # 探索测试特定功能
/devtools-debug network             # 专注 API 调试
/devtools-debug performance         # 性能分析
/devtools-debug screenshot          # 捕获当前视觉状态
```

### 2. 快照优先原则（Snapshot First）

**当前问题：** 使用硬编码选择器，页面更新后失效

**优化方案：**
```javascript
// ❌ 避免
function clickSubmit() {
  click(".submit-button")  // 硬编码
}

// ✅ 推荐
async function clickSubmit() {
  const snapshot = await take_snapshot()
  // 从 snapshot 中找到提交按钮的 UID
  const submitButtonUid = findElementUid(snapshot, "Submit")
  click(submitButtonUid)
}
```

### 3. 结构化报告（Structured Reporting）

**建议：** 所有调试报告应包含：

```markdown
## Findings

### Errors
- [Error 1]: Description
  - Evidence: Screenshot/Console log
  - Location: file:line

### Network Requests
- [Request 1]: /api/endpoint
  - Status: 429 (Rate Limited)
  - Timing: 2.3s
  - Evidence: Network log

### Performance Metrics
- LCP: 3.2s (Needs improvement)
- CLS: 0.05 (Good)
- Evidence: Performance trace

## Recommendations

1. [Priority High] Fix rate limiting issue
2. [Priority Medium] Optimize image loading
```

### 4. 明确的升级规则（Escalation Rules）

**建议：** 定义何时使用其他工具

| 问题类型 | 工具 |
|---------|------|
| 编译错误 | build-error-resolver |
| 可重复的 bug | e2e-runner (写 Playwright 测试) |
| 安全问题 | security-reviewer |
| 架构问题 | architect |
| 运行时调试 | Chrome DevTools MCP |

### 5. 会话持久性配置

**当前问题：** 每次都需要重新登录

**优化方案：** 使用固定的用户数据目录

```bash
# 启动 Chrome 时指定用户数据目录
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=~/.editory/chrome-profile

# 首次登录后，会话会保存在 ~/.editory/chrome-profile/
# 后续使用会自动保持登录状态
```

### 6. 错误重试机制

**建议：** 对常见错误实现自动重试

```javascript
async function robustClick(uid, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await click(uid)
      return
    } catch (error) {
      if (error.message.includes('AbortError') && i < maxRetries - 1) {
        // 等待 1 秒后重试
        await new Promise(resolve => setTimeout(resolve, 1000))
        continue
      }
      throw error
    }
  }
}
```

### 7. 性能监控最佳实践

**建议：** 只在必要时使用性能追踪

```javascript
// ❌ 避免：在每次交互时都追踪
performance_start_trace()
click("button")
performance_stop_trace()

// ✅ 推荐：仅在需要分析性能问题时使用
// 例如：页面加载慢、交互卡顿等
if (needPerformanceAnalysis) {
  performance_start_trace(reload=true)
  // 执行关键流程
  performance_stop_trace()
  performance_analyze_insight(insightSetId, "LCP")
}
```

---

## 快速参考

### 常用工具速查表

| 工具 | 用途 | 频率 | 关键点 |
|------|------|------|--------|
| `take_snapshot()` | 获取 DOM UIDs | ⭐⭐⭐⭐⭐ | 交互前必调 |
| `list_console_messages()` | 检查错误 | ⭐⭐⭐⭐⭐ | 调试首选 |
| `list_network_requests()` | API 调试 | ⭐⭐⭐⭐⭐ | 网络问题排查 |
| `navigate_page(url)` | 页面导航 | ⭐⭐⭐⭐⭐ | 完整 URL |
| `click(uid)` | 点击元素 | ⭐⭐⭐⭐ | 使用动态 UID |
| `fill(uid, value)` | 填充表单 | ⭐⭐⭐⭐ | 先 snapshot |
| `evaluate_script(fn)` | 执行 JS | ⭐⭐⭐ | 完整函数声明 |
| `take_screenshot()` | 截图 | ⭐⭐⭐ | 证据捕获 |
| `upload_file(path)` | 上传文件 | ⭐⭐ | 绝对路径 |
| `wait_for(text)` | 等待元素 | ⭐⭐⭐ | 异步操作后 |
| `get_network_request(id)` | 请求详情 | ⭐⭐ | 深入分析 |
| `performance_start_trace()` | 性能追踪 | ⭐ | 按需使用 |

### 何时使用 Chrome DevTools MCP

| 问题类型 | 使用 Chrome DevTools MCP | 使用 Playwright | 使用其他工具 |
|---------|----------------------|----------------|----------|
| "为什么 API 返回 429?" | ✅ | ❌ | ❌ |
| "UI 看起来不对" | ✅ | ❌ | ❌ |
| "这个功能是否回归?" | ❌ | ✅ | ❌ |
| "编译错误是什么?" | ❌ | ❌ | ✅ build-error-resolver |
| "跨平台自动发布" | ✅ | ❌ | ❌ |
| "性能分析" | ✅ | ❌ | ❌ |
| "探索新功能" | ✅ | ❌ | ❌ |

### 常见错误代码

| 错误 | 原因 | 解决方案 |
|------|------|--------|
| `AbortError` | 连接超时 | 重新导航或重启 Chrome |
| `Input validation error` | 脚本格式错误 | 使用完整函数声明 |
| `Element not found` | 使用硬编码选择器 | 先调用 `take_snapshot()` |
| `MCP server already exists` | 重复配置 | 检查 `.mcp.json` |
| `Unauthorized` | 认证失败 | 验证 API 密钥 |

### 工作流速查卡片

**调试流程：**
```
1. navigate_page() → 2. take_snapshot() → 3. list_console_messages()
→ 4. list_network_requests() → 5. take_screenshot()
```

**API 调试：**
```
1. list_network_requests() → 2. get_network_request(id)
→ 3. evaluate_script()
```

**UI 交互：**
```
1. take_snapshot() → 2. click(uid) → 3. wait_for(text)
→ 4. take_snapshot() → 5. list_console_messages()
```

**发布流程：**
```
1. navigate_page() → 2. take_snapshot() (检查登录)
→ 3. fill/click (填表单) → 4. upload_file()
→ 5. click() (发布) → 6. take_screenshot()
```

---

## 附录：项目配置示例

### AutoHighlight 项目配置

**文件结构：**
```
.claude/
├── rules/
│   └── devtools-debugging.md      # 95 行
├── agents/
│   └── devtools-debugger.md       # 172 行
└── commands/
    └── devtools-debug.md
```

**关键内容摘要：**

**rules/devtools-debugging.md:**
```markdown
# Chrome DevTools MCP 调试规则

## 核心模式
1. Snapshot First - 永远先 take_snapshot()
2. Structured Reporting - 包含证据的结构化报告
3. Phase-Based Workflow - Observe → Hypothesize → Test → Report

## 项目特定目标
- 字幕生成流程验证
- FFmpeg WASM 加载检查
- API 速率限制监控
- 视频导出性能分析
```

### Editory 项目配置

**文件结构：**
```
platforms/
├── mowen.md           # Mowen 发布指南
├── wechat.md          # 微信公众号指南（110 行）
├── xiaohongshu.md     # 小红书指南
└── twitter.md         # Twitter/X 指南
```

**关键内容摘要：**

**platforms/wechat.md:**
```markdown
# 微信公众号发布指南

## 方法：Chrome DevTools MCP（浏览器自动化）

### 10 步工作流
1. navigate_page → mp.weixin.qq.com
2. take_snapshot → 检查登录（可能需 QR 扫码）
3. click → "新建文章"
4. fill → title/author/summary
5. evaluate_script → 注入 HTML 到编辑器
6. upload_file → 封面图 900x383
7. click → 发布按钮
8. take_screenshot → 确认
9. take_snapshot → 验证
10. 提取发布 URL

### 已知选择器
- Title: #title
- Editor: #edui1_body
- Summary: textarea[placeholder*="summary"]
```

---

## 总结

**Chrome DevTools MCP 的核心价值：**

1. **探索性调试** - AI 驱动的交互式问题发现
2. **浏览器自动化** - 跨平台内容发布的灵活方案
3. **性能分析** - Core Web Vitals 和 API 响应时间监控
4. **API 调试** - 网络请求和响应的深入分析

**关键成功因素：**

- ✅ Snapshot First 原则（动态 UIDs）
- ✅ 标准化 4 阶段工作流（Observe → Hypothesize → Test → Report）
- ✅ 结构化报告（带证据）
- ✅ 清晰的升级规则（何时转向 Playwright）
- ✅ 会话持久性配置（固定用户数据目录）

**下一步行动：**

1. 在新项目中应用 AutoHighlight 的配置框架
2. 为常见场景创建可复用的命令（如 `/devtools-debug`）
3. 建立错误重试和容错机制
4. 定期将 DevTools MCP 发现的 bug 转化为 Playwright 回归测试

---

**文档版本：** 1.0
**最后更新：** 2026-02-10
**基于数据：** 76 个会话，3 个主要项目（AutoHighlight, Editory, Remotion Skills Try）

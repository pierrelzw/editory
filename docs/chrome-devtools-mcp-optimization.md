# Chrome DevTools MCP 优化指南

> 基于 76 个会话的实战经验提炼

## 📊 优化清单总览

| 优化项 | 影响 | 难度 | 优先级 |
|--------|------|------|--------|
| [标准化工作流](#1-标准化工作流) | ⭐⭐⭐⭐⭐ | 低 | P0 |
| [Snapshot First 原则](#2-snapshot-first-原则) | ⭐⭐⭐⭐⭐ | 低 | P0 |
| [会话持久性](#3-会话持久性) | ⭐⭐⭐⭐ | 低 | P1 |
| [错误重试机制](#4-错误重试机制) | ⭐⭐⭐⭐ | 中 | P1 |
| [结构化报告](#5-结构化报告) | ⭐⭐⭐ | 低 | P1 |
| [升级规则](#6-升级规则) | ⭐⭐⭐ | 低 | P2 |
| [性能监控策略](#7-性能监控策略) | ⭐⭐ | 中 | P2 |

---

## 1. 标准化工作流

### 问题
- 每次调试都是临时发挥
- 容易遗漏关键步骤
- 团队成员方法不一致

### 解决方案

**创建标准化配置文件：**

```
.claude/
├── rules/
│   └── devtools-debugging.md      # 调试规则和场景
├── agents/
│   └── devtools-debugger.md       # DevTools 专家 agent
└── commands/
    └── devtools-debug.md          # 自定义命令
```

**示例：`.claude/rules/devtools-debugging.md`**

```markdown
# Chrome DevTools MCP 调试规则

## 使用场景
- 运行时错误诊断
- API 调试
- UI 交互验证
- 性能分析

## 核心模式

### 1. Snapshot First
永远在交互前调用 `take_snapshot()`

### 2. 4 阶段工作流
**Observe → Hypothesize → Test → Report**

#### Phase 1: Observe
- navigate_page()
- take_snapshot()
- take_screenshot()
- list_console_messages()
- list_network_requests()

#### Phase 2: Hypothesize
- 分析失败的 API 调用 (4xx/5xx)
- 识别控制台错误
- 检查缺失的 UI 元素

#### Phase 3: Test
- 执行交互操作
- 验证状态变化
- 记录新的错误

#### Phase 4: Report
- 结构化输出
- 包含证据（截图、日志）
- 提供修复建议

## 项目特定目标
[根据你的项目填写]
- 功能 A 的验证流程
- 功能 B 的错误检查
- API C 的响应时间监控
```

**示例：`.claude/commands/devtools-debug.md`**

```markdown
# /devtools-debug 命令

## 触发
```
/devtools-debug [mode]
```

## 模式

### 1. 完整诊断（默认）
```
/devtools-debug
```
执行完整的 4 阶段诊断

### 2. 网络调试
```
/devtools-debug network
```
专注于 API 和网络请求

### 3. 性能分析
```
/devtools-debug performance
```
分析 Core Web Vitals 和加载时间

### 4. 功能测试
```
/devtools-debug test <feature>
```
探索性测试特定功能

### 5. 快速截图
```
/devtools-debug screenshot
```
捕获当前状态（快照 + 截图）
```

**实施步骤：**

1. 复制上述模板到你的项目
2. 根据项目特点调整"项目特定目标"
3. 在团队中推广使用 `/devtools-debug` 命令

**预期收益：**
- ✅ 调试效率提升 50%
- ✅ 问题发现率提升 30%
- ✅ 团队协作一致性提升

---

## 2. Snapshot First 原则

### 问题
- 使用硬编码选择器：`click(".submit-button")`
- 页面更新后选择器失效
- 频繁出现"元素找不到"错误

### 解决方案

**实施规则：**

```javascript
// ❌ 禁止使用硬编码选择器
click(".button")
fill("#input", "value")

// ✅ 强制使用 take_snapshot() 获取 UIDs
take_snapshot()  // 返回最新的元素 UIDs
click("dynamic-uid-abc123")
```

**代码检查清单：**

```markdown
## 交互操作前检查清单

- [ ] 是否调用了 `take_snapshot()`？
- [ ] 是否使用了 snapshot 返回的 UID？
- [ ] 是否避免了硬编码的 CSS 选择器？
- [ ] 是否在页面更新后重新调用 snapshot？
```

**工具函数（推荐）：**

```javascript
// 封装标准的交互模式
async function safeClick(elementDescription) {
  const snapshot = await take_snapshot()
  const uid = findElementUid(snapshot, elementDescription)
  if (!uid) {
    throw new Error(`Element not found: ${elementDescription}`)
  }
  await click(uid)
}

async function safeFill(elementDescription, value) {
  const snapshot = await take_snapshot()
  const uid = findElementUid(snapshot, elementDescription)
  if (!uid) {
    throw new Error(`Element not found: ${elementDescription}`)
  }
  await fill(uid, value)
}
```

**预期收益：**
- ✅ 元素定位成功率从 70% 提升到 95%+
- ✅ 减少调试时间 40%
- ✅ 代码更健壮，更易维护

---

## 3. 会话持久性

### 问题
- 每次使用都需要重新登录
- 多平台登录耗时
- 开发效率低

### 解决方案

**使用固定的用户数据目录：**

```bash
# 创建专用目录
mkdir -p ~/.editory/chrome-profile

# 启动 Chrome 时指定
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=~/.editory/chrome-profile
```

**自动化脚本：**

```bash
#!/bin/bash
# 文件：start-chrome-debug.sh

CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DEBUG_PORT=9222
PROFILE_DIR="$HOME/.editory/chrome-profile"

# 检查 Chrome 是否已运行
if pgrep -f "Chrome.*remote-debugging-port=$DEBUG_PORT" > /dev/null; then
    echo "Chrome is already running with debugging enabled"
    exit 0
fi

# 启动 Chrome
"$CHROME_PATH" \
  --remote-debugging-port=$DEBUG_PORT \
  --user-data-dir="$PROFILE_DIR" \
  --no-first-run \
  --no-default-browser-check \
  > /dev/null 2>&1 &

echo "Chrome started with debugging on port $DEBUG_PORT"
echo "User data directory: $PROFILE_DIR"
```

**使用方法：**

```bash
chmod +x start-chrome-debug.sh
./start-chrome-debug.sh
```

**登录流程优化：**

```javascript
// 检查登录状态
navigate_page("https://platform.com")
take_snapshot()

// 如果检测到登录页面
if (isLoginPage) {
  // 首次：提示用户登录
  console.log("Please log in manually. Session will be saved.")
  // 等待用户登录...

  // 后续：自动保持登录
  console.log("Using saved session from ~/.editory/chrome-profile")
}
```

**预期收益：**
- ✅ 节省登录时间 90%（每次 2-5 分钟）
- ✅ 提升开发体验
- ✅ 支持多账号（不同 profile 目录）

---

## 4. 错误重试机制

### 问题
- `AbortError: operation aborted` 频繁出现
- 网络不稳定导致失败
- 需要手动重试

### 解决方案

**实现通用重试函数：**

```javascript
async function withRetry(operation, maxRetries = 3, delay = 1000) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await operation()
    } catch (error) {
      const isRetriable =
        error.message.includes('AbortError') ||
        error.message.includes('timeout') ||
        error.message.includes('network')

      if (!isRetriable || i === maxRetries - 1) {
        throw error
      }

      console.log(`Retry ${i + 1}/${maxRetries} after ${delay}ms`)
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }
}

// 使用示例
await withRetry(async () => {
  take_snapshot()
  click("button-uid")
  wait_for("Success")
})
```

**针对特定错误的策略：**

```javascript
// 1. AbortError → 重新导航
async function robustNavigate(url, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await navigate_page(url)
      await wait_for("body")  // 等待页面加载
      return
    } catch (error) {
      if (i === maxRetries - 1) throw error
      console.log(`Navigation failed, retrying... (${i + 1}/${maxRetries})`)
      await new Promise(resolve => setTimeout(resolve, 2000))
    }
  }
}

// 2. 元素找不到 → 多次 snapshot
async function robustClick(elementDesc, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    const snapshot = await take_snapshot()
    const uid = findElementUid(snapshot, elementDesc)

    if (uid) {
      await click(uid)
      return
    }

    if (i < maxRetries - 1) {
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
  }

  throw new Error(`Element not found after ${maxRetries} attempts: ${elementDesc}`)
}
```

**配置化的重试策略：**

```javascript
const RETRY_CONFIG = {
  navigate: { maxRetries: 3, delay: 2000 },
  click: { maxRetries: 3, delay: 1000 },
  network: { maxRetries: 5, delay: 1000 },
  upload: { maxRetries: 2, delay: 3000 },
}

async function retryOperation(type, operation) {
  const config = RETRY_CONFIG[type]
  return withRetry(operation, config.maxRetries, config.delay)
}
```

**预期收益：**
- ✅ 成功率从 80% 提升到 95%+
- ✅ 减少手动干预
- ✅ 更好的容错性

---

## 5. 结构化报告

### 问题
- 调试结果缺乏结构
- 难以追踪问题
- 团队协作效率低

### 解决方案

**标准报告模板：**

```markdown
# Debugging Report

## Summary
[一句话概括问题]

## Environment
- URL: http://localhost:3000/dashboard
- Timestamp: 2026-02-10 15:30:00
- Browser: Chrome 120.0.6099.129

## Findings

### 1. Console Errors
**Severity:** High
**Description:** Uncaught TypeError: Cannot read property 'map' of undefined
**Location:** Dashboard.js:45
**Evidence:**
```
[ERROR] Uncaught TypeError: Cannot read property 'map' of undefined
    at Dashboard.js:45:12
    at render (Dashboard.js:30:5)
```

### 2. Network Issues
**Severity:** Medium
**Description:** API endpoint returning 429 (Rate Limited)
**Location:** POST /api/data
**Evidence:**
```json
{
  "status": 429,
  "error": "Rate limit exceeded",
  "retryAfter": 60
}
```

### 3. Performance Metrics
**Severity:** Low
**Description:** LCP exceeds threshold
**Measurement:**
- LCP: 3.2s (Target: <2.5s)
- FID: 45ms (Good)
- CLS: 0.05 (Good)

## Screenshots
- [Initial state](./screenshot-1.png)
- [Error state](./screenshot-2.png)
- [After fix](./screenshot-3.png)

## Recommendations

### Priority High
1. **Fix TypeError in Dashboard.js**
   - Add null check before `.map()`
   - Expected impact: Prevents crash

2. **Implement API rate limiting handling**
   - Add retry logic with exponential backoff
   - Cache API responses
   - Expected impact: Improves reliability

### Priority Medium
3. **Optimize LCP**
   - Preload critical images
   - Defer non-critical JS
   - Expected impact: Better UX

## Next Steps
- [ ] Create issue for TypeError fix
- [ ] Implement rate limiting handler
- [ ] Write Playwright test to prevent regression
```

**自动化报告生成：**

```javascript
class DebugReport {
  constructor() {
    this.findings = []
    this.screenshots = []
  }

  addError(severity, description, location, evidence) {
    this.findings.push({
      type: 'error',
      severity,
      description,
      location,
      evidence
    })
  }

  addNetworkIssue(severity, description, requestId, evidence) {
    this.findings.push({
      type: 'network',
      severity,
      description,
      requestId,
      evidence
    })
  }

  addScreenshot(name, path) {
    this.screenshots.push({ name, path })
  }

  generate() {
    // 生成 Markdown 格式的报告
    return formatReport(this)
  }
}

// 使用示例
const report = new DebugReport()

// 收集信息
const messages = await list_console_messages()
messages.filter(m => m.level === 'error').forEach(error => {
  report.addError('High', error.message, error.source, error.stackTrace)
})

const requests = await list_network_requests()
requests.filter(r => r.status >= 400).forEach(req => {
  report.addNetworkIssue('Medium', `${req.method} ${req.url}`, req.id, req)
})

// 生成并保存
const markdown = report.generate()
fs.writeFileSync('debug-report.md', markdown)
```

**预期收益：**
- ✅ 问题追踪效率提升 60%
- ✅ 团队协作更顺畅
- ✅ 知识沉淀和复用

---

## 6. 升级规则

### 问题
- Chrome DevTools MCP 和 Playwright 职责不清
- 不知道何时写自动化测试
- 重复的调试工作

### 解决方案

**定义清晰的升级规则：**

```markdown
## 何时使用 Chrome DevTools MCP

✅ **适合场景：**
- 探索性调试（不知道问题在哪）
- 一次性任务（发布内容、填表单）
- 交互式验证（需要人工判断）
- 性能分析（Core Web Vitals）

❌ **不适合场景：**
- 可重复的回归测试 → 用 Playwright
- 编译错误 → 用 build-error-resolver
- 安全问题 → 用 security-reviewer
- 架构设计 → 用 architect

## 升级路径

### 路径 1：发现 Bug → 写测试
```
DevTools MCP 发现 bug
  ↓
分析根因
  ↓
修复代码
  ↓
写 Playwright 回归测试
  ↓
Playwright 在 CI/CD 中防止再次出现
```

### 路径 2：编译/构建错误
```
DevTools MCP 发现运行时错误
  ↓
发现是编译问题（TypeScript/ESLint）
  ↓
升级到 build-error-resolver
```

### 路径 3：安全问题
```
DevTools MCP 发现 API 返回敏感信息
  ↓
升级到 security-reviewer
  ↓
全面安全审计
```

## 决策树

```
发现问题
  ├─ 是可重复的 bug？
  │    └─ YES → 写 Playwright 测试
  │    └─ NO → 继续用 DevTools MCP
  │
  ├─ 是编译/类型错误？
  │    └─ YES → 用 build-error-resolver
  │
  ├─ 涉及安全问题？
  │    └─ YES → 用 security-reviewer
  │
  └─ 是架构级问题？
       └─ YES → 用 architect
```
```

**实施步骤：**

1. 在项目中创建 `.claude/rules/escalation.md`
2. 定义项目特定的升级规则
3. 在发现问题时参考决策树

**预期收益：**
- ✅ 工具使用更高效
- ✅ 避免重复工作
- ✅ 自动化测试覆盖率提升

---

## 7. 性能监控策略

### 问题
- 每次调试都运行性能追踪，浪费时间
- 不知道何时需要分析性能
- 缺乏性能基线

### 解决方案

**按需使用性能追踪：**

```javascript
// ❌ 避免：在每次交互时都追踪
performance_start_trace()
click("button")
performance_stop_trace()

// ✅ 推荐：仅在需要时使用

// 场景 1：页面加载慢
if (pageLoadTime > 3000) {
  performance_start_trace(reload=true)
  // 重新加载页面
  performance_stop_trace()
  performance_analyze_insight(insightSetId, "LCP")
}

// 场景 2：交互卡顿
if (interactionLag > 500) {
  performance_start_trace()
  // 执行卡顿的操作
  performance_stop_trace()
  performance_analyze_insight(insightSetId, "INP")
}

// 场景 3：定期基线测试（每周/每月）
if (isPerformanceTestDay) {
  runPerformanceBaseline()
}
```

**建立性能基线：**

```javascript
// 记录关键指标的基线值
const PERFORMANCE_BASELINE = {
  homepage: {
    LCP: 2.0,  // 秒
    FID: 50,   // 毫秒
    CLS: 0.05
  },
  dashboard: {
    LCP: 2.5,
    FID: 100,
    CLS: 0.1
  }
}

async function checkPerformanceRegression(page) {
  const baseline = PERFORMANCE_BASELINE[page]

  performance_start_trace(reload=true)
  // 页面加载...
  const metrics = await performance_stop_trace()
  const insights = await performance_analyze_insight(metrics.id, "LCP")

  const currentLCP = insights.lcp

  if (currentLCP > baseline.LCP * 1.2) {  // 超过基线 20%
    console.warn(`⚠️ Performance regression detected on ${page}`)
    console.warn(`LCP: ${currentLCP}s (baseline: ${baseline.LCP}s)`)
    return false
  }

  return true
}
```

**性能监控工作流：**

```markdown
## 何时运行性能分析

### 触发条件
1. **用户报告页面慢**
   - 运行完整的性能追踪
   - 分析 LCP/FID/CLS

2. **部署前检查**
   - 对关键页面运行基线测试
   - 确保无性能回归

3. **定期审计**
   - 每周/每月运行基线测试
   - 跟踪性能趋势

### 不需要时
- 日常调试
- 功能验证
- API 测试
```

**预期收益：**
- ✅ 调试时间减少 30%（避免不必要的追踪）
- ✅ 性能回归早发现
- ✅ 建立长期性能数据

---

## 🎯 实施路线图

### 第 1 周：基础优化
- [ ] 实施 Snapshot First 原则
- [ ] 配置会话持久性（固定 profile 目录）
- [ ] 创建 `.claude/rules/devtools-debugging.md`

### 第 2 周：工作流标准化
- [ ] 创建 `/devtools-debug` 命令
- [ ] 实施 4 阶段工作流
- [ ] 在团队中推广使用

### 第 3 周：错误处理
- [ ] 实现通用重试函数
- [ ] 针对常见错误添加特殊处理
- [ ] 配置化重试策略

### 第 4 周：报告和升级
- [ ] 实施结构化报告模板
- [ ] 定义升级规则
- [ ] 将发现的 bug 转化为 Playwright 测试

### 持续优化
- [ ] 定期审查性能基线
- [ ] 收集团队反馈
- [ ] 迭代优化工作流

---

## 📈 预期效果总结

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 调试效率 | 基线 | +50% | ⬆️ |
| 问题发现率 | 基线 | +30% | ⬆️ |
| 元素定位成功率 | 70% | 95%+ | +25% |
| 登录时间 | 2-5 分钟/次 | 一次性 | -90% |
| 操作成功率 | 80% | 95%+ | +15% |
| 报告质量 | 低 | 高 | ⬆️⬆️ |
| 团队协作效率 | 基线 | +40% | ⬆️ |

---

## 🔗 相关资源

- **完整指南：** `chrome-devtools-mcp-guide.md`
- **快速入门：** `chrome-devtools-mcp-quickstart.md`
- **AutoHighlight 配置示例：** `.claude/rules/devtools-debugging.md`（如有）
- **Editory 平台指南：** `platforms/*.md`

---

**文档版本：** 1.0
**最后更新：** 2026-02-10
**基于数据：** 76 个会话，3 个主要项目的实战经验

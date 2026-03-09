# Editory 文档中心

## Chrome DevTools MCP 使用指南

本目录包含完整的 Chrome DevTools MCP 使用文档，基于跨项目 76 个会话的实战经验总结。

### 📚 文档目录

#### 1. [快速入门](./chrome-devtools-mcp-quickstart.md) ⚡
**适合人群：** 新手，想快速上手

**内容：**
- 5 分钟快速了解 Chrome DevTools MCP
- 核心工具速览
- 标准工作流（4 步法）
- 常见问题速查
- 5 分钟练习

**什么时候看：** 第一次使用，或需要快速回顾时

---

#### 2. [完全指南](./chrome-devtools-mcp-guide.md) 📖
**适合人群：** 想深入理解和掌握的用户

**内容：**
- 核心概念与定位
- 使用场景详解（调试、API、自动化、性能）
- 所有工具详解与最佳实践
- 常见工作流模式
- 常见问题与解决方案
- 项目配置示例
- 快速参考

**什么时候看：** 遇到复杂问题，或需要系统学习时

---

#### 3. [优化指南](./chrome-devtools-mcp-optimization.md) 🚀
**适合人群：** 已经在使用，想提升效率的用户

**内容：**
- 7 大优化方向（标准化工作流、Snapshot First、会话持久性等）
- 实施路线图（4 周计划）
- 预期效果量化（效率提升 50%+）
- 代码示例和配置模板

**什么时候看：** 使用一段时间后，想进一步优化工作流时

---

### 🎯 快速导航

#### 我想...

**快速上手 Chrome DevTools MCP**
→ 阅读 [快速入门](./chrome-devtools-mcp-quickstart.md)

**解决具体问题（如 API 调试、元素找不到）**
→ 查看 [完全指南 - 常见问题与解决方案](./chrome-devtools-mcp-guide.md#常见问题与解决方案)

**优化现有工作流**
→ 阅读 [优化指南](./chrome-devtools-mcp-optimization.md)

**了解最佳实践**
→ 查看 [完全指南 - 工具详解与最佳实践](./chrome-devtools-mcp-guide.md#工具详解与最佳实践)

**搭建标准化配置**
→ 查看 [优化指南 - 标准化工作流](./chrome-devtools-mcp-optimization.md#1-标准化工作流)

**了解实战案例**
→ 查看 [完全指南 - 使用场景总结](./chrome-devtools-mcp-guide.md#使用场景总结) 和 [快速入门 - 实战案例](./chrome-devtools-mcp-quickstart.md#实战案例)

---

### 📊 文档数据来源

所有文档基于真实项目经验提炼：

- **会话数量：** 76 个会话
- **主要项目：**
  - AutoHighlight（视频高亮项目）- 219+ 会话
  - Editory（内容发布项目）- 13 会话
  - Remotion Skills Try
- **工具使用频率：** 17 个 Chrome DevTools MCP 工具
- **覆盖场景：** 调试、API 测试、浏览器自动化、性能分析

---

### 🔑 核心要点提炼

#### 1. Chrome DevTools MCP 的定位
- **开发阶段：** 探索性调试和问题发现
- **vs Playwright：** Playwright 用于 CI/CD 回归测试
- **核心价值：** AI 驱动的交互式调试

#### 2. 必须遵守的原则
⭐ **Snapshot First** - 任何 `click()` 或 `fill()` 前，先 `take_snapshot()`
- 避免硬编码选择器
- 使用动态 UIDs
- 让浏览器告诉你元素位置

#### 3. 标准工作流（4 步法）
```
Observe → Hypothesize → Test → Report
```

#### 4. 最常用的 5 个工具
1. `take_snapshot()` - 获取 DOM 和 UIDs
2. `list_console_messages()` - 查看错误
3. `list_network_requests()` - API 调试
4. `navigate_page()` - 页面导航
5. `click(uid)` / `fill(uid, value)` - 交互

---

### 💡 快速提示

#### 新手必看
```markdown
1. 阅读"快速入门"（5 分钟）
2. 记住：Snapshot First!
3. 遵循 4 步工作流
4. 遇到问题查"常见问题速查"
```

#### 进阶用户
```markdown
1. 实施标准化工作流配置
2. 启用会话持久性（避免重复登录）
3. 实现错误重试机制
4. 定义升级规则（何时写 Playwright 测试）
```

#### 团队协作
```markdown
1. 共享标准化配置文件（.claude/rules/）
2. 使用结构化报告模板
3. 定义清晰的升级路径
4. 定期审查和优化工作流
```

---

### 🛠️ 环境设置（快速版）

```bash
# 1. 启动 Chrome（带远程调试和持久会话）
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=~/.editory/chrome-profile

# 2. 在 Claude Code 中验证连接
# 应该能看到 mcp__chrome-devtools__* 工具

# 3. 首次登录各平台（会话会自动保存）

# 4. 开始使用！
```

---

### 📖 推荐阅读顺序

#### 路径 1：快速上手（30 分钟）
1. [快速入门](./chrome-devtools-mcp-quickstart.md) - 15 分钟
2. 实践：完成"5 分钟练习" - 10 分钟
3. [完全指南 - 快速参考](./chrome-devtools-mcp-guide.md#快速参考) - 5 分钟

#### 路径 2：深入学习（2 小时）
1. [快速入门](./chrome-devtools-mcp-quickstart.md) - 15 分钟
2. [完全指南](./chrome-devtools-mcp-guide.md) - 60 分钟
3. [优化指南](./chrome-devtools-mcp-optimization.md) - 45 分钟

#### 路径 3：问题导向（按需）
遇到问题 → 查"快速参考" → 查"常见问题" → 深入阅读相关章节

---

### 🔄 文档更新记录

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2026-02-10 | 初始版本，基于 76 个会话经验 |

---

### 📞 反馈与贡献

如果你发现：
- 文档有错误或不清楚的地方
- 有新的最佳实践想分享
- 有优化建议

欢迎：
- 提交 Issue
- 创建 Pull Request
- 在项目讨论区交流

---

### 🎓 学习资源

**相关文档：**
- Editory 项目文档：`../README.md`
- 平台发布指南：`../platforms/*.md`
- 技能定义：`../skills/publish.md`

**外部资源：**
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Claude Code 文档](https://docs.anthropic.com/claude-code)
- [Playwright vs Browser Automation](https://playwright.dev/)

---

**Happy Debugging! 🚀**

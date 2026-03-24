# Claude-Mem 配置与使用教程

> 给 Claude Code 装个记忆力 —— 跨会话记住你做过什么、改过什么、踩过什么坑。

---

前阵子用 Claude Code 做一个项目，改了一堆东西，第二天开新会话，它又从头来过 —— 不记得昨天我们一起调了半天的 bug，不记得最后选了哪个方案。

[Claude-Mem](https://github.com/thedotmack/claude-mem) 就是解决这个问题的。它是一个 Claude Code 插件，自动记录每次会话里 Claude 做的所有操作（读文件、跑命令、改代码……），用 AI 压缩成摘要，下次开会话时自动注入相关上下文。

全程零操作，装完就忘。

---

## 1. 安装

在 Claude Code 里跑两行命令：

```
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

然后重启 Claude Code。

安装过程会自动处理依赖：检测并安装 Bun 运行时、uv（Python 包管理器，向量搜索用的）、下载预构建二进制文件。

**前置条件：**

- Node.js 18.0.0+
- 最新版 Claude Code（需支持 plugin）

**一个坑：** `npm install -g claude-mem` 只装了 SDK 库，不会注册 Hook 也不会启动 Worker 服务。必须用上面的 `/plugin` 命令安装。

---

## 2. 验证安装

重启后，Claude-Mem 会自动启动 Worker 服务。几种验证方式：

```bash
# 健康检查
curl http://localhost:37777/health

# 查看 Worker 状态
cd ~/.claude/plugins/marketplaces/thedotmack && npm run worker:status

# 查看日志
npm run worker:logs

# 测试上下文注入
npm run test:context
```

浏览器打开 [http\://localhost:37777](http://localhost:37777) 能看到 Web 查看器，说明装好了。

---

## 3. 它怎么工作的

![Claude-Mem 自动记忆循环机制](./Claude-Mem_tutorial.assets/illustration-01-auto-behavior-lifecycle.png)

Claude-Mem 靠 **5 个生命周期 Hook** 驱动，全自动：

- **SessionStart** —— 注入之前会话的相关上下文
- **UserPromptSubmit** —— 记录你的原始提问
- **PostToolUse** —— 捕获每次工具调用的观察记录（读文件、跑命令等）
- **Stop** —— 生成本次会话总结
- **SessionEnd** —— 标记完成，准备下次注入

背后的架构：

- **Worker 服务** —— Bun 驱动的 HTTP API（默认端口 37777），带 Web UI 和 10 个搜索端点
- **SQLite 数据库** —— 存会话、观察记录、总结
- **Chroma 向量数据库** —— 语义 + 关键词混合搜索
- **Smart Install** —— 首次运行时缓存依赖检查

---

## 4. MCP 搜索工具

这是 Claude-Mem 的核心能力 —— 3 层渐进式搜索，省 token：

- **search** —— 返回精简索引（每条结果约 50-100 token）
- **timeline** —— 按时间线获取观察上下文
- **get_observations** —— 按 ID 拉取完整详情（每条约 500-1000 token）

用法示例：先 search 拿到候选列表，找到相关的 ID，再 get_observations 拉详情。比一次性拉全量省 **\~10 倍 token**。

日常使用不用手动调这些 —— 直接用自然语言问 Claude 就行：

```
我们之前是怎么处理数据库迁移的？
上周修的那个 bug 是什么？
这个项目的认证逻辑之前改过吗？
```

mem-search skill 会自动触发搜索。

---

## 5. 配置

配置文件在 `~/.claude-mem/settings.json`，首次运行自动创建。也可以通过环境变量 `CLAUDE_MEM_DATA_DIR` 改存储位置。

### 核心配置

- `CLAUDE_MEM_MODEL` —— 压缩观察用的 AI 模型，可选 `haiku`、`sonnet`（默认）、`opus`
- `CLAUDE_MEM_PROVIDER` —— AI 提供商，可选 `claude`（默认）、`gemini`、`openrouter`
- `CLAUDE_MEM_MODE` —— 工作模式，默认 `code`，还有 `code--es`、`code--zh`、`email-investigation` 等
- `CLAUDE_MEM_CONTEXT_OBSERVATIONS` —— 每次注入多少条观察，默认 50（范围 1-200）
- `CLAUDE_MEM_WORKER_PORT` —— Worker 端口，默认 37777
- `CLAUDE_MEM_WORKER_HOST` —— Worker 地址，默认 `127.0.0.1`
- `CLAUDE_MEM_SKIP_TOOLS` —— 跳过记录的工具（逗号分隔），默认跳过 `ListMcpResourcesTool,SlashCommand,Skill,TodoWrite,AskUserQuestion`
- `CLAUDE_MEM_LOG_LEVEL` —— 日志级别，可选 `DEBUG`、`INFO`（默认）、`WARN`、`ERROR`、`SILENT`

### 上下文注入精调

这组配置控制每次启动时注入什么、注入多少：

- `CLAUDE_MEM_CONTEXT_SESSION_COUNT` —— 从最近几个会话拉观察，默认 10（范围 1-50）
- `CLAUDE_MEM_CONTEXT_OBSERVATION_TYPES` —— 按类型过滤：`bugfix`、`feature`、`refactor`、`discovery`、`decision`、`change`
- `CLAUDE_MEM_CONTEXT_OBSERVATION_CONCEPTS` —— 按概念过滤：`how-it-works`、`why-it-exists`、`what-changed`、`problem-solution`、`gotcha`、`pattern`、`trade-off`
- `CLAUDE_MEM_CONTEXT_FULL_COUNT` —— 展开详情的观察数量，默认 5（范围 0-20）
- `CLAUDE_MEM_CONTEXT_FULL_FIELD` —— 展开哪个字段，`narrative`（默认）或 `facts`
- `CLAUDE_MEM_CONTEXT_SHOW_READ_TOKENS` —— 显示读取 token 消耗，默认 true
- `CLAUDE_MEM_CONTEXT_SHOW_WORK_TOKENS` —— 显示生成观察的 token 消耗，默认 true
- `CLAUDE_MEM_CONTEXT_SHOW_LAST_SUMMARY` —— 注入上一次会话总结，默认 false
- `CLAUDE_MEM_CONTEXT_SHOW_LAST_MESSAGE` —— 注入上一次会话最后消息，默认 false

### 用免费 AI 提供商（省 Anthropic API 额度）

默认用 Claude Sonnet 压缩观察记录，会消耗少量额度。可以切到免费的：

**Gemini（推荐）：**

```json
{
  "CLAUDE_MEM_PROVIDER": "gemini",
  "CLAUDE_MEM_GEMINI_API_KEY": "你的API密钥",
  "CLAUDE_MEM_GEMINI_MODEL": "gemini-2.5-flash-lite"
}
```

可选模型：`gemini-2.5-flash-lite`（默认）、`gemini-2.5-flash`、`gemini-3-flash-preview`。

**OpenRouter（免费模型可用）：**

```json
{
  "CLAUDE_MEM_PROVIDER": "openrouter",
  "CLAUDE_MEM_OPENROUTER_API_KEY": "你的API密钥",
  "CLAUDE_MEM_OPENROUTER_MODEL": "xiaomi/mimo-v2-flash:free"
}
```

OpenRouter 还有额外配置：`CLAUDE_MEM_OPENROUTER_MAX_CONTEXT_MESSAGES`（默认 20）、`CLAUDE_MEM_OPENROUTER_MAX_TOKENS`（默认 100000）。

---

## 6. 日常使用

**正常工作就行** —— 安装后不用额外操作。所有工具调用自动被记录和压缩，下次开新会话时相关上下文自动注入。

**保护隐私** —— 敏感内容用标签包裹，不会被存储：

```
帮我配置 API，密钥是 <private>sk-abc123</private>
```

**查看记忆流** —— 浏览器打开 [http\://localhost:37777，可以看到当前会话的观察记录、历史会话总结，以及搜索和过滤功能。](http://localhost:37777，可以看到当前会话的观察记录、历史会话总结，以及搜索和过滤功能。)

**Skills 快捷入口：**

- 直接用自然语言提问历史 —— 自动触发 mem-search
- `/make-plan` —— 基于记忆上下文制定实施计划
- `/do` —— 用子代理执行分阶段计划
- `/smart-explore` —— token 高效的代码探索
- `/timeline-report` —— 生成项目开发旅程报告

**Worker 管理（一般不需要）：**

```bash
cd ~/.claude/plugins/marketplaces/thedotmack
npm run worker:status   # 查看状态
npm run worker:restart  # 重启
npm run worker:logs     # 查看日志
npm run worker:tail     # 实时日志
```

---

## 7. 数据位置

![Claude-Mem 数据架构总览](./Claude-Mem_tutorial.assets/illustration-02-data-architecture.png)

- `~/.claude-mem/claude-mem.db` —— SQLite 数据库
- `~/.claude-mem/settings.json` —— 配置文件
- `~/.claude-mem/chroma/` —— 向量数据库
- `~/.claude-mem/logs/` —— 日志（按天轮转）
- [http\://localhost:37777](http://localhost:37777) —— Web 界面

所有数据存在本地，不上传到任何远程服务器。

---

## 8. 源码构建（可选）

不想用 plugin 安装的，可以从源码构建：

```bash
git clone https://github.com/thedotmack/claude-mem.git
cd claude-mem && npm install
npm run build
npm run worker:start  # 手动启动 Worker
```

---

## 常见问题

**Q: 会消耗我的 Anthropic API 额度吗？**
默认用 Claude Sonnet 压缩观察记录，会有少量消耗。切到 Gemini 或 OpenRouter 就免费了，见上面的配置。

**Q: 怎么清除所有记忆？**
删除 `~/.claude-mem/claude-mem.db` 即可重置。

**Q: Worker 没启动怎么办？**
先检查端口 37777 是否被占用，再看日志 `~/.claude-mem/logs/` 排查。也可以直接在 Claude Code 里描述问题，内置的 troubleshoot skill 会自动诊断。

**Q: 怎么提 bug？**

```bash
cd ~/.claude/plugins/marketplaces/thedotmack
npm run bug-report
```

会生成一份完整的诊断报告。

---

## 资源

- [官方文档](https://docs.claude-mem.ai/)
- [GitHub 仓库](https://github.com/thedotmack/claude-mem)
- [Discord 社区](https://discord.com/invite/J4wttp9vDu)
- [X (Twitter)](https://x.com/Claude_Memory)


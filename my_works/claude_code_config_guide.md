---
mowen_note_id: 2BRZhBR6dq2DBDaFCncbJ
---

# Claude Code 配置全景：从裸机到趁手

> 一份清单，帮你搞清 Claude Code 到底有哪些配置、放在哪、怎么用、先配什么。

---

用 Claude Code 写代码，很多人（包括我自己）一开始都是直接上手干——打开终端，输入 `claude`，开聊。

能用吗？能用。但用着用着你会发现：

- 每次新对话都要重复说一遍"用中文回复"、"别改我的测试文件"
- 不知道怎么让 Claude 记住你的项目规范
- 看到别人用 `/review`、`/commit` 这种斜杠命令，但不知道怎么自己写
- 更别提 hooks、rules、MCP 这些词了——听都没听过

这篇文章就是解决这个问题的。**一张全景图，把 Claude Code 所有配置类型、位置、作用、优先级说清楚。**

不讲太多道理，直接给你能用的。

## 先看全局：8 种配置一览

- **CLAUDE.md** — 你给 Claude 的"工作手册"，影响力最大
- **settings.json** — 权限、环境变量、模型选择，控制 Claude 能做什么
- **skills/** — 可复用的 AI 工作流，支持斜杠命令调用
- **commands/** — 旧版斜杠命令（仍然有效，但 skills 是新选择）
- **rules/** — 按文件路径模式加载的模块化指令
- **hooks** — 生命周期自动化：会话开始、工具调用前后等
- **MCP servers** — 外部工具集成（数据库、API、浏览器等）
- **memory/** — 跨会话记忆，Claude 自己记笔记

如果你是新手，**只看前三个就够了**。后面的是进阶。

## 1. CLAUDE.md — 最重要的一个文件

这是你给 Claude 的持久化指令。每次对话开始，Claude 都会读它。你写什么，它就按什么做。

**放在哪里？**

- `./CLAUDE.md` 或 `./.claude/CLAUDE.md` — 项目级，团队共享（提交到 git）
- `~/.claude/CLAUDE.md` — 用户级，你的所有项目都生效
- `./CLAUDE.local.md` — 项目级但私有，不提交到 git

**优先级**：越具体的越优先。项目级 > 用户级。

**最小可用示例**：

```markdown
# Project Rules

- 用中文回复
- 代码注释用英文
- commit message 用英文
- 测试框架用 pytest
- 不要修改 tests/ 目录下的已有测试，除非我明确要求
```

**常见错误**：

- **写太长** — 超过 200 行效果就开始打折。Claude 是当 context 来读的，不是严格执行的规则引擎。精简、具体、可操作的指令效果最好。
- **写太泛** — "写好的代码"没用，"函数不超过 20 行、错误必须用自定义 Error 类型"才有用。
- **不知道 ********`@`******** 引用** — 你可以用 `@path/to/file` 在 CLAUDE.md 里引入其他文件，避免一个文件写太长。比如 `@.claude/code-standards.md`。

**一个技巧**：运行 `/init` 可以让 Claude 自动帮你生成第一个 CLAUDE.md。

## 2. settings.json — 权限和行为控制

这个文件控制 Claude 的"能力边界"——哪些工具能用、哪些命令允许执行、用什么模型等。

**放在哪里？**

- `~/.claude/settings.json` — 用户级，所有项目生效
- `.claude/settings.json` — 项目级，团队共享
- `.claude/settings.local.json` — 项目级但私有

**优先级**：CLI 参数 > 本地 > 项目 > 用户。数组类设置（如权限列表）会跨层级合并。

**最小可用示例**：

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm test)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(.env)"
    ]
  }
}
```

上面的意思是：允许 Claude 自动执行 lint 和 test，禁止它用 curl 或读 .env 文件。

**权限判断顺序**：deny → ask → allow。先检查禁止列表，再检查需要询问的，最后检查允许的。

**其他有用设置**：

```json
{
  "model": "claude-sonnet-4-6",
  "env": {
    "NODE_ENV": "development"
  },
  "autoMemoryEnabled": true
}
```

**常见错误**：

- **所有权限都用默认** — 每次 Claude 想跑个测试都要你手动点允许，来回几次你就烦了。把常用的安全命令加到 `allow` 里，体验好很多。
- **不知道有 ****`.local.json`** — 有些权限你不想提交到团队仓库（比如允许访问你个人的 API key 路径），放 `settings.local.json` 就行。

## 3. Skills — 现代斜杠命令

Skills 是 Claude Code 目前推荐的方式来创建可复用工作流。写一个 `SKILL.md`，就得到一个 `/skill-name` 命令。

**放在哪里？**

- `.claude/skills/<skill-name>/SKILL.md` — 项目级
- `~/.claude/skills/<skill-name>/SKILL.md` — 用户级，所有项目可用

**最小可用示例**：

创建 `.claude/skills/review/SKILL.md`：

```markdown
---
name: review
description: Review code changes for quality and security
allowed-tools:
  - Bash(git diff)
  - Read
  - Grep
---

Review the current git diff. Check for:
1. Security issues (injection, XSS, hardcoded secrets)
2. Logic errors
3. Missing error handling

Output a brief summary with severity ratings.
```

保存后，在对话里输入 `/review` 就能用了。

**进阶功能**：

- `context: fork` — 在独立子 Agent 中运行，不污染主对话
- `$ARGUMENTS` — 获取用户传入的参数，比如 `/review src/api.ts`
- `!`command`` — 动态注入 shell 命令输出
- `disable-model-invocation: true` — 只能手动调用，Claude 不会自动触发

**Skills vs Commands**：旧的 `.claude/commands/*.md` 还能用，但 Skills 功能更强（支持子 Agent、工具限制、自动发现）。如果是新项目，直接用 Skills。

## 4. Commands — 旧版斜杠命令

放在 `.claude/commands/` 目录下的 Markdown 文件，每个文件变成一个 `/command`。

比如 `.claude/commands/commit.md` → `/commit`。

**还能用，但新项目建议直接用 Skills。** 如果 Skill 和 Command 同名，Skill 优先。

## 5. Rules — 按路径加载的模块化指令

Rules 是 CLAUDE.md 的"模块化"版本。你可以写多个 `.md` 文件，按文件路径模式条件加载。

**放在哪里？**

- `.claude/rules/*.md` — 项目级
- `~/.claude/rules/*.md` — 用户级

**最小可用示例**：

创建 `.claude/rules/api-standards.md`：

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API 开发规范
- 所有接口必须做入参校验
- 使用统一错误响应格式
- 必须写单元测试
```

这个规则只在 Claude 读取 `src/api/` 下的 TypeScript 文件时才会生效。

**没有 ********`paths`******** 的 Rules** 会在每次会话启动时无条件加载，和写在 CLAUDE.md 里效果一样。

**适用场景**：monorepo 里不同子项目有不同规范，或者前后端代码规则不同。

## 6. Hooks — 生命周期自动化

Hooks 让你在 Claude 的生命周期节点上自动执行脚本。

**在 settings.json 里配置**：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx eslint --fix $CLAUDE_FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

上面的例子：每次 Claude 编辑或创建文件后，自动跑一次 ESLint 修复。

**常用生命周期事件**：

- `SessionStart` — 会话开始，适合注入上下文
- `PreToolUse` — 工具调用前，可以拦截危险操作
- `PostToolUse` — 工具调用后，适合做 lint、format
- `Stop` — Claude 回复结束，适合做收尾工作

**Handler 类型**：

- `command` — 跑 shell 命令
- `http` — 发 HTTP 请求
- `prompt` — 发一段 prompt 给 Claude 做决策
- `agent` — 启动一个子 Agent

**退出码约定**：0 = 通过，2 = 阻止（适用于 Pre 类事件）。

**常见错误**：

- **不知道有 Hooks 这个东西** — 大部分人压根没配过。但它是自动化最强的手段，比如自动跑测试、自动 lint、自动注入项目上下文。
- **Hook 配在了 project settings 但用了本机路径** — 脚本路径如果是绝对路径，其他人 clone 下来就跑不了。要么用相对路径，要么放 `settings.local.json`。

## 7. MCP Servers — 连接外部世界

MCP（Model Context Protocol）让 Claude 能调用外部工具——数据库、浏览器、API、文件系统等。

**添加方式**：

```bash
# 远程 HTTP（推荐）
claude mcp add --transport http my-server https://example.com/mcp

# 本地进程
claude mcp add --transport stdio my-server -- npx my-mcp-server

# 指定范围
claude mcp add --scope project --transport http my-server https://example.com/mcp
```

**配置存储**：

- `~/.claude.json` — 用户级 / 本地 MCP 配置（注意不是 `~/.claude/` 目录下）
- `.mcp.json` — 项目级，可提交到 git

**项目级 ********`.mcp.json`******** 示例**：

```json
{
  "mcpServers": {
    "my-db": {
      "command": "npx",
      "args": ["@anthropic/mcp-server-postgres", "postgresql://localhost/mydb"],
      "env": {}
    }
  }
}
```

**注意**：项目级 MCP 首次使用时 Claude 会弹出确认。环境变量可以用 `${VAR}` 语法引用。

## 8. Memory — 跨会话记忆

Claude 会自动在 `~/.claude/projects/<项目>/memory/MEMORY.md` 里记笔记——你纠正过它的偏好、项目的构建命令、调试经验等。

**特点**：

- 只有 `MEMORY.md` 的前 200 行会在每次对话加载
- 其他子文件（如 `debugging.md`）按需读取
- 按项目隔离，同一个 git 仓库的不同 worktree 共享

**管理**：在对话里说"记住 xxx"它就会存下来，或者运行 `/memory` 查看和管理。

**开关**：

```json
{ "autoMemoryEnabled": false }
```

## 新手优先级：先配什么？

如果你刚开始用 Claude Code，我建议按这个顺序来：

**1. CLAUDE.md（第一天就该有）**

跑一下 `/init`，Claude 会帮你生成一个基础版。然后根据自己的习惯加几条规则。不用写太长，5-10 条就够。

**2. settings.json 的权限（第一周内）**

把你常用的安全命令加到 `allow` 里，减少手动确认。把不该碰的文件加到 `deny`。

**3. 一两个 Skill（用熟了以后）**

从你最常做的重复性工作开始。比如 code review、commit message 生成、发布流程。

**4. 其余的（按需学习）**

Rules、Hooks、MCP、Memory——这些等你用了一段时间、有了具体需求再学不迟。

## 8 个新手典型误区

**1. CLAUDE.md 写了 500 行**

Claude 不是规则引擎，超长指令会稀释重点。保持在 200 行以内，用 `@` 引用拆分。

**2. 所有权限都用默认**

结果每次 Claude 想跑个测试都弹确认框。常用安全命令该 allow 就 allow。

**3. 不知道用户级配置的存在**

`~/.claude/CLAUDE.md`、`~/.claude/settings.json`、`~/.claude/skills/` 这三个位置的配置对你的所有项目生效。"用中文回复"这种偏好放用户级，别每个项目都写一遍。

**4. 把 ********`.env`******** 路径写进了 CLAUDE.md**

CLAUDE.md 如果提交到 git，等于把敏感信息路径告诉了所有人。私有信息放 `CLAUDE.local.md` 或 `settings.local.json`。

**5. 不知道 Skills 和 Commands 的区别**

都能创建斜杠命令，但 Skills 更强：支持子 Agent、工具限制、自动发现。新项目直接用 Skills。

**6. 只知道 CLAUDE.md，不知道 Rules**

如果你的项目有"前端代码用这套规范、后端代码用那套规范"的需求，Rules 的路径匹配比在 CLAUDE.md 里写一堆 `if` 条件优雅得多。

**7. Hook 脚本用了绝对路径然后提交了**

队友 clone 下来路径不对。放 `settings.local.json`，或者用相对路径。

**8. 不查看 /status**

不确定哪些配置生效了？运行 `/status`，一目了然。

## 配置不是一次性的

写完 CLAUDE.md 不代表完事了。随着你用 Claude Code 越来越深入，你会发现：

- 有些规则需要调整——Claude 老是误解某条指令，可能是你写得不够具体
- 有些重复操作可以变成 Skill——你第 5 次手动告诉 Claude "先跑测试再提交"的时候，就该写个 `/test-and-commit` 了
- 有些项目间的共同偏好该提到用户级——别在每个项目的 CLAUDE.md 里写同样的东西

我自己的做法是：用了一段时间后跑一次"配置体检"——看看哪些指令 Claude 经常忽略（可能写得不好），哪些操作我在重复（可能需要 Skill 或 Hook），哪些配置应该提到用户级。

工具会变，但思路不变：**让 AI 的工作环境越来越适配你的工作方式。**

你的 Claude Code，配好了吗？

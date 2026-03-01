# 如何在一个项目里同时使用 Claude Code、Codex等其他 AI，需要维护两套配置么？
> 简单来说，把你希望所有 AI 都遵守的规则写在 AGENT.md 里，在CLAUDE.md 里@Agent.md，然后加上 Claude 专属的东西 ，就不用维护两套了。


有的时候，我会在一个项目里同时跑多个 AI Coding Agent，比如 Claude Code、Codex 和 GitHub Copilot。但是我发现一个头疼的问题：Claude Code 读 CLAUDE.md，Codex 读 AGENTS.md —— 我每次在一个地方改完，还要同步到另一个地方，很麻烦。


一开始我采用的是软链接的方式，但是每次打开 AGENTS.md 看到首行是 CLAUDE.md，我就不太得劲。今天简单问了一下 AI ，找到了一个干净的方案。

**1. 先搞清楚：AI 默认读什么文件？**

- Claude Code — 读 `CLAUDE.md`
- OpenAI Codex — 读 `AGENTS.md`，找不到就按 fallback 列表找
- Cursor、Gemini CLI、Copilot coding agent、Aider、Zed、Devin、Warp 等 — 都读 `AGENTS.md`

好消息是，除了 Claude Code，其他工具基本都支持 `AGENTS.md` 了。

[`AGENTS.md`](https://agents.md/) 是 Linux 基金会下面 Agentic AI Foundation 维护的开放标准，60000+ 开源项目在用。Claude Code 暂时还没有原生支持（[GitHub Issue #6235](https://github.com/anthropics/claude-code/issues/6235) 几千人投票了），但有简单的 workaround。

**2. 核心思路：一份内容，多个入口**

把所有通用的项目规则写在 `AGENTS.md` 里，然后让各家的专属配置文件引用它。

项目结构长这样：

```
my-project/
├── AGENTS.md        ← 通用规则（Codex、Copilot agent、Cursor 等直接读这个）
├── CLAUDE.md        ← Claude 专属配置 + 引用 AGENTS.md
└── ...
```

**3. AGENTS.md 怎么写**

把所有 AI 工具都需要知道的东西放在这里：项目结构、构建命令、代码风格、测试规范。

```markdown
# Project: my-project

## Build & Test
- Install: `npm install`
- Dev: `npm run dev`
- Test: `npm test`
- Lint: `npm run lint`

## Architecture
- Frontend: React + TypeScript, components in `src/components/`
- Backend: Express API in `src/api/`
- Database: PostgreSQL, migrations in `db/migrations/`

## Code Style
- Use TypeScript strict mode
- Prefer named exports
- Error messages in English
- Components use PascalCase, utils use camelCase

## Testing
- Unit tests alongside source files: `foo.test.ts`
- E2E tests in `tests/e2e/`
- Run `npm test` before committing

## Git
- Commit messages: `type: description` (feat/fix/refactor/test/docs)
- No force push to main
```

没有固定格式，就是普通 Markdown。写清楚就行。

**4. CLAUDE.md 怎么写**

两行搞定引用，然后加 Claude 专属的东西：

```markdown
# CLAUDE.md 
@AGENTS.md

## Claude-Specific
- Add Claude-only guidance here if needed (keep rules in AGENTS.md).
```

`@AGENTS.md` 这个语法是 Claude Code 的文件引用功能，Claude 启动时会自动把 AGENTS.md 的内容加载进来。这样不用复制粘贴，AGENTS.md 改了，Claude 也能立刻读到最新内容。

**5. 让 Codex 也能读 CLAUDE.md（反向兼容）**

如果某个项目只有 CLAUDE.md 没有 AGENTS.md（比如你之前的老项目），可以配置 Codex 的 fallback：

编辑 `~/.codex/config.toml`：

```toml
project_doc_fallback_filenames = ["CLAUDE.md"]
```

这样 Codex 在找不到 AGENTS.md 时，会自动去读 CLAUDE.md。

**6. 符号链接：最简单粗暴的方案**

如果你不需要 Claude 专属配置，直接软链接也可以，这是我之前的做法：

```bash
ln -s AGENTS.md CLAUDE.md
```

两个文件指向同一份内容，改一处全生效。缺点是没法加 Claude 专属的指令了。

**7. 个人建议**

大多数情况，「AGENTS.md 为主 + 各工具专属文件引用它」是最好的选择：

- 通用规则一份，不用同步
- Claude 专属能力（@引用、slash commands、hooks）不丢
- Copilot coding agent 直接读 AGENTS.md，零配置
- 再加一个新 AI 工具，大概率也读 AGENTS.md，不用改任何东西

如果项目简单、不需要任何工具的专属配置，符号链接也够用。

**8. 多目录项目（monorepo）怎么办？**

AGENTS.md 和 CLAUDE.md 都支持嵌套——子目录放一份，优先级高于根目录。

```
monorepo/
├── AGENTS.md              ← 全局规则
├── CLAUDE.md              ← @AGENTS.md + Claude 全局配置
├── packages/
│   ├── frontend/
│   │   └── AGENTS.md      ← 前端专属规则（覆盖全局）
│   └── backend/
│       └── AGENTS.md      ← 后端专属规则（覆盖全局）
```

Codex 的加载顺序是：从根目录往当前目录走，每层最多加载一个文件。Claude Code 也类似，`.claude/` 目录和项目根的 CLAUDE.md 会一起加载。

---

等 Claude Code 哪天原生支持 AGENTS.md，连 CLAUDE.md 都可以不用了

不过，这是一个很有趣的问题：为什么其他家都统一用 AGENTS.md, 唯独 Claude Code 独树一帜用 CLAUDE.md，你怎么看？

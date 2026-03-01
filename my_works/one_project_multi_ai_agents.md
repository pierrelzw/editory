一个项目里同时用 Claude Code、Codex、GitHub Copilot，怎么不维护三套配置？


前几天在一个项目里同时跑 Claude Code、Codex 和 GitHub Copilot，发现一个头疼的问题：Claude Code 读 CLAUDE.md，Codex 读 AGENTS.md，Copilot 有自己的 `.github/copilot-instructions.md`——三边各写一份，改了这个忘了那个，很快就不同步了。

我折腾了一番，找到了一个干净的方案，分享出来。

**1. 先搞清楚：谁读什么文件？**

- Claude Code — 读 `CLAUDE.md`
- OpenAI Codex — 读 `AGENTS.md`，找不到就按 fallback 列表找
- GitHub Copilot — 读 `.github/copilot-instructions.md`，Copilot coding agent 也读 `AGENTS.md`
- Cursor、Gemini CLI、Aider、Zed、Devin、Warp 等 — 都读 `AGENTS.md`

好消息是，除了 Claude Code，其他工具基本都支持 `AGENTS.md` 了。

[`AGENTS.md`](https://agents.md/) 是 Linux 基金会下面 Agentic AI Foundation 维护的开放标准，60000+ 开源项目在用。Claude Code 暂时还没有原生支持（[GitHub Issue #6235](https://github.com/anthropics/claude-code/issues/6235) 几千人投票了），但有简单的 workaround。

**2. 核心思路：一份内容，多个入口**

把所有通用的项目规则写在 `AGENTS.md` 里，然后让各家的专属配置文件引用它。

项目结构长这样：

```
my-project/
├── AGENTS.md        ← 通用规则（Codex、Copilot agent、Cursor 等直接读这个）
├── CLAUDE.md        ← Claude 专属配置 + 引用 AGENTS.md
├── .github/
│   └── copilot-instructions.md  ← Copilot 专属配置（可选）
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
@AGENTS.md

## Claude-Specific

- Use Opus for architecture decisions, Haiku for simple fixes
- Prefer Edit tool over Bash sed for file modifications
- Run tests after every code change
- When unsure, ask before proceeding
```

`@AGENTS.md` 这个语法是 Claude Code 的文件引用功能，Claude 启动时会自动把 AGENTS.md 的内容加载进来。这样你不用复制粘贴，AGENTS.md 改了，Claude 也能立刻读到最新内容。

**5. GitHub Copilot 怎么办？**

Copilot 有两套机制：

- **Copilot coding agent**（就是帮你自动写 PR 那个）— 已经支持 `AGENTS.md`，不用额外配置
- **Copilot Chat / 编辑器内补全** — 读 `.github/copilot-instructions.md`

如果你主要用 Copilot coding agent，项目有 `AGENTS.md` 就够了，不需要单独写 `copilot-instructions.md`。

如果你也用 Copilot Chat，可以创建一个简短的 `.github/copilot-instructions.md`，引导它去看 AGENTS.md：

```markdown
See AGENTS.md in the repository root for project conventions,
build commands, and code style guidelines.
```

Copilot 没有 `@` 引用语法，但它能读到仓库里的文件。这行提示足够让它在回答时参考 AGENTS.md 的内容。

**6. 让 Codex 也能读 CLAUDE.md（反向兼容）**

如果某个项目只有 CLAUDE.md 没有 AGENTS.md（比如你之前的老项目），可以配置 Codex 的 fallback：

编辑 `~/.codex/config.toml`：

```toml
project_doc_fallback_filenames = ["CLAUDE.md"]
```

这样 Codex 在找不到 AGENTS.md 时，会自动去读 CLAUDE.md。

**7. 符号链接：最简单粗暴的方案**

如果你不需要 Claude 专属配置，直接软链接：

```bash
ln -s AGENTS.md CLAUDE.md
```

两个文件指向同一份内容，改一处全生效。缺点是没法加 Claude 专属的指令了。

**8. 我的建议**

大多数情况，「AGENTS.md 为主 + 各工具专属文件引用它」是最好的选择：

- 通用规则一份，不用同步
- Claude 专属能力（@引用、slash commands、hooks）不丢
- Copilot coding agent 直接读 AGENTS.md，零配置
- 再加一个新 AI 工具，大概率也读 AGENTS.md，不用改任何东西

如果项目简单、不需要任何工具的专属配置，符号链接也够用。

**9. 多目录项目（monorepo）怎么办？**

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

说到底，`AGENTS.md` 就是给 AI 看的 README。把你希望所有 AI 都遵守的规则写在那里，Claude 专属的东西写在 CLAUDE.md 里 `@` 一下，Copilot 专属的写在 `.github/copilot-instructions.md` 里提一句，就不用维护三套了。

等 Claude Code 哪天原生支持 AGENTS.md，连 CLAUDE.md 里的 `@AGENTS.md` 都可以删掉。

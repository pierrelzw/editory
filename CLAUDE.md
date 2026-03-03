# Editory — AI-Powered Content Distribution Skill for Claude Code

## What is this?

Editory is a Claude Code skill (not a standalone CLI tool). After writing a Markdown article in your editor, you can say in Claude Code: "publish this article to Mowen and Xiaohongshu". Claude reads the article, performs AI review & optimization (formatting/layout/content/cover image — user's choice), shows a preview for confirmation, then automatically publishes via MCP servers or Chrome DevTools MCP.

**Key insight:** Claude itself is the AI engine — no extra Python packages needed. The entire project is Markdown files that guide Claude's behavior.

## MCP Strategy

| Platform | Primary Method | Fallback |
|---|---|---|
| Mowen | `mowen-mcp-server` (direct MCP) | Chrome DevTools MCP (browser) |
| Xiaohongshu | `rednote-mcp` (planned, not yet configured) | Chrome DevTools MCP (browser) |
| WeChat Official Account | Chrome DevTools MCP (browser) | — |
| Twitter/X | Chrome DevTools MCP (browser) | — |

Mowen has a dedicated MCP Server for direct content publishing without browser automation. Xiaohongshu's `rednote-mcp` is planned but not yet configured. WeChat and Twitter use Chrome DevTools MCP for browser automation.

## Project Structure

```
editory/
├── CLAUDE.md                  # This file — project context for Claude
├── .claude/
│   ├── commands/
│   │   ├── publish.md         # /publish skill definition
│   │   └── iterate-style.md   # /iterate-style skill (update style from user edits)
│   ├── my-style.md            # Writing style skill (auto-loaded for all writing tasks)
│   └── my-style-log.md        # Style iteration log (not loaded during writing)
├── my_works/                   # User's articles and drafts
├── my-skills/                  # Custom user skills
├── baoyu-skills/               # Third-party skills (baoyu)
├── docs/                       # Project documentation files
├── platforms/                  # Per-platform publishing automation guides
│   ├── mowen.md               # Mowen: MCP tools + browser fallback
│   ├── xiaohongshu.md         # Xiaohongshu: MCP tools + browser fallback
│   ├── wechat.md              # WeChat Official Account: browser automation
│   └── twitter.md             # Twitter/X: browser automation
├── templates/
│   ├── review-checklist.md    # AI content review checklist template
│   └── platform-styles.md    # Per-platform content style guide
├── config.example.toml        # Example configuration
├── README.md                  # Project documentation
└── README.zh-CN.md            # Chinese documentation
```

## Writing Style

**When the user asks to write, polish, continue, rewrite, or translate article content, read `.claude/my-style.md` first and follow its rules throughout the task.** This file defines the user's voice, style principles, and forbidden patterns.

Claude auto-commits after writing or polishing content, using tags `[ai-draft]`, `[ai-polish]`, or `[user-draft]`. The user edits freely, then runs `/iterate-style <file>` to extract preferences from the diff and update the style skill. Iteration log is stored in `.claude/my-style-log.md` (not loaded during writing).

## Workflow Overview

```
User: /publish article.md --platforms mowen,xiaohongshu

Step 1: Read article — parse Markdown + frontmatter
Step 2: AI review & optimization (optional, skippable) — loads my-style.md
Step 3: Preview — show final versions per platform, await confirmation
Step 4: Auto-publish — MCP direct call or Chrome DevTools browser automation
Step 5: Result report — status, links, screenshots per platform
```

```
User: /iterate-style article.md

Step 1: Detect scenario (AI draft vs AI polish) from git history
Step 2: Generate diff between AI version and user's edits
Step 3: Analyze changes — extract style rules
Step 4: Update .claude/my-style.md — deduplicate, consolidate, check contradictions
Step 5: Show summary — new rules, reinforced rules, edit rate
```

## Chrome Session Persistence

Chrome uses a dedicated profile directory so login sessions persist:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=~/.editory/chrome-profile
```

On first use, navigate to each platform's login page and log in manually. Sessions are saved in `~/.editory/chrome-profile/`. On subsequent uses, all platforms are already logged in.

If a session expires, Claude detects the login page via `take_snapshot` and prompts the user to re-login.

## Configuration

Configuration template at `config.example.toml`. Currently not auto-loaded (this is a Markdown-only skill project — no code reads config files).

## Language Rules
When I write in Chinese:
1. Plan phase: Output the plan in BOTH Chinese and English. Chinese for my review, English for execution.
2. Execution phase: Follow the English plan. Use English for code, comments, and commit messages.
3. Response phase: Summarize results in Chinese.

When I write in English, respond in English. No special formatting rules apply.


# Editory — AI-Powered Content Distribution Skill for Claude Code

## What is this?

Editory is a Claude Code skill (not a standalone CLI tool). After writing a Markdown article in your editor, you can say in Claude Code: "publish this article to Mowen and Xiaohongshu". Claude reads the article, performs AI review & optimization (formatting/layout/content/cover image — user's choice), shows a preview for confirmation, then automatically publishes via MCP servers or Chrome DevTools MCP.

**Key insight:** Claude itself is the AI engine — no extra Python packages needed. The entire project is Markdown files that guide Claude's behavior.

## MCP Strategy

| Platform | Primary Method | Fallback |
|---|---|---|
| Mowen | `mowen-mcp-server` (direct MCP) | Chrome DevTools MCP (browser) |
| Xiaohongshu | `rednote-mcp` (direct MCP) | Chrome DevTools MCP (browser) |
| WeChat Official Account | Chrome DevTools MCP (browser) | — |
| Twitter/X | Chrome DevTools MCP (browser) | — |

Mowen and Xiaohongshu have dedicated MCP Servers for direct content publishing without browser automation. WeChat and Twitter use Chrome DevTools MCP for browser automation.

## Project Structure

```
editory/
├── CLAUDE.md                  # This file — project context for Claude
├── skills/
│   └── publish.md             # /publish skill definition
├── platforms/                  # Per-platform publishing automation guides
│   ├── mowen.md               # Mowen: MCP tools + browser fallback
│   ├── xiaohongshu.md         # Xiaohongshu: MCP tools + browser fallback
│   ├── wechat.md              # WeChat Official Account: browser automation
│   └── twitter.md             # Twitter/X: browser automation
├── templates/
│   ├── review-checklist.md    # AI content review checklist template
│   └── platform-styles.md    # Per-platform content style guide
├── config.example.toml        # Example configuration
└── README.md                  # Project documentation
```

## Workflow Overview

```
User: /publish article.md --platforms mowen,xiaohongshu

Step 1: Read article — parse Markdown + frontmatter
Step 2: AI review & optimization (optional, skippable)
Step 3: Preview — show final versions per platform, await confirmation
Step 4: Auto-publish — MCP direct call or Chrome DevTools browser automation
Step 5: Result report — status, links, screenshots per platform
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

See `config.example.toml` for all available options. Config can live at:
- `~/.config/editory/config.toml` (global)
- `./editory.toml` (project-level)

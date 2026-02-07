# Editory

AI-powered content distribution skill for Claude Code. Write once in Markdown, publish everywhere.

## What is Editory?

Editory is a Claude Code skill that lets you publish Markdown articles to multiple platforms directly from your terminal. After writing your article in any editor, just tell Claude:

```
/publish article.md --platforms mowen,xiaohongshu
```

Claude reads the article, performs AI review and optimization, shows a preview, and automatically publishes to your chosen platforms.

**This is not a standalone CLI tool.** It's a set of Markdown files that teach Claude Code how to publish content. Claude itself is the AI engine — no extra dependencies needed.

## Supported Platforms

| Platform | Method | Status |
|---|---|---|
| Mowen (mowen.cn) | Direct MCP via `mo-note-mcp-server` | Ready |
| Xiaohongshu | Direct MCP via `rednote-mcp` | Ready |
| WeChat Official Account | Browser automation via Chrome DevTools MCP | Ready |
| Twitter/X | Browser automation via Chrome DevTools MCP | Ready |

## How It Works

1. **Read** — Claude reads your Markdown file and parses frontmatter metadata
2. **Review** — AI reviews formatting, content quality, and suggests improvements (optional)
3. **Adapt** — Generates platform-specific versions (Xiaohongshu gets emojis, Twitter gets threads, etc.)
4. **Preview** — Shows you the final version for each platform
5. **Publish** — Automatically publishes via MCP servers or browser automation
6. **Report** — Shows status, links, and screenshots for each platform

## Setup

### 1. Install to your project

Copy the `skills/`, `platforms/`, and `templates/` directories to your project:

```bash
git clone https://github.com/user/editory.git
cp -r editory/skills editory/platforms editory/templates your-project/
cp editory/CLAUDE.md your-project/
```

Or add Editory directly as a skill directory in your Claude Code configuration.

### 2. Configure MCP Servers

For Mowen (direct MCP via Streamable HTTP):

墨问官方提供了基于 Streamable HTTP 协议的 MCP Server，无需本地环境依赖。

1. 在墨问微信小程序中开通会员
2. 前往 [墨问开发者中心](https://mowen.cn) 获取 API Key
3. 在 Claude Code 中添加 MCP 配置：

```bash
claude mcp add-json mowen '{"type":"streamable-http","url":"https://open.mowen.cn/api/open/mcp/v1/note?key=YOUR_API_KEY"}'
```

或手动编辑 MCP 配置文件，添加：

```json
{
  "mcpServers": {
    "mowen": {
      "type": "streamable-http",
      "url": "https://open.mowen.cn/api/open/mcp/v1/note?key=YOUR_API_KEY"
    }
  }
}
```

配置完成后可用的 MCP Tools：
- `CreateRichNote` — 创建富文本笔记（支持加粗、高亮、链接、图片、音频、PDF）
- `EditRichNote` — 编辑已有笔记
- `ChangeNoteSettings` — 设置笔记公开/私密
- `UploadViaURL` — 通过 URL 上传图片、音频、PDF 文件

> 详见官方仓库：https://github.com/we-mowen/mo-note-mcp-server

For Xiaohongshu (direct MCP):
```bash
# Add to Claude Code MCP settings
npx rednote-mcp --stdio
# First-time: obtain cookies via browser login
```

For WeChat and Twitter (browser automation):
```bash
# Ensure chrome-devtools MCP is configured in Claude Code
# Start Chrome with remote debugging:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=~/.editory/chrome-profile
```

### 3. Login to platforms

On first use, log in to each platform in the Chrome instance:
- Navigate to each platform's website
- Log in with your credentials
- Sessions persist in `~/.editory/chrome-profile/`

### 4. Configuration (optional)

Copy and customize the config file:

```bash
cp config.example.toml ~/.config/editory/config.toml
# Edit to set your defaults
```

## Usage

### Basic usage
```
/publish article.md
```
Uses platforms from article frontmatter or config defaults.

### Specify platforms
```
/publish article.md --platforms mowen,xiaohongshu,twitter
```

### Skip AI review
```
/publish article.md --skip-review
```

### Skip cover image generation
```
/publish article.md --skip-cover
```

### Article frontmatter

```yaml
---
title: "My Article Title"
tags: [python, programming, tips]
platforms: [mowen, xiaohongshu]
cover: ./cover.png
type: article  # or "short_post"
---

Your article content here...
```

## Project Structure

```
editory/
├── CLAUDE.md                  # Project context for Claude
├── skills/
│   └── publish.md             # /publish skill definition
├── platforms/
│   ├── mowen.md               # Mowen publishing guide
│   ├── xiaohongshu.md         # Xiaohongshu publishing guide
│   ├── wechat.md              # WeChat Official Account guide
│   └── twitter.md             # Twitter/X publishing guide
├── templates/
│   ├── review-checklist.md    # AI content review checklist
│   └── platform-styles.md    # Platform content style guide
├── config.example.toml        # Example configuration
└── README.md                  # This file
```

## How It Differs from Traditional Tools

| | Traditional CLI | Editory (Claude Code Skill) |
|---|---|---|
| Code | ~30+ Python files | ~8 Markdown files |
| Dependencies | 12+ Python packages | 0 (uses Claude Code's built-in capabilities) |
| AI Capabilities | None (pure automation) | Native (content review, optimization, adaptation) |
| Installation | pip install | Copy skill files |
| Maintenance | Code + tests | Update platform selector docs |
| Flexibility | Fixed workflow | Conversational — adjust on the fly |

## License

MIT

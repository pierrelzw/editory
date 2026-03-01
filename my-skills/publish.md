# /publish Skill

Publish a Markdown article to one or more content platforms.

## Trigger

```
/publish <file> [--platforms <platforms>] [--skip-review] [--skip-cover]
```

**Arguments:**
- `<file>` — Path to the Markdown file to publish
- `--platforms <platforms>` — Comma-separated list of target platforms (mowen, xiaohongshu, wechat, twitter). Falls back to frontmatter `platforms` field, then config defaults.
- `--skip-review` — Skip the AI content review & optimization step
- `--skip-cover` — Skip cover image generation

## Workflow

### 1. Parse Input

Read the Markdown file and parse frontmatter:

```yaml
---
title: "Article Title"
tags: [tag1, tag2]
platforms: [mowen, xiaohongshu]
cover: ./cover.png        # optional, path to cover image
type: article              # "article" (long-form) or "short_post" (short content)
---
```

- If `--platforms` not specified, use frontmatter `platforms` field
- If neither specified, use defaults from config file
- Detect content type: `article` (long-form) or `short_post` (short content)

### 2. AI Content Review & Optimization (unless --skip-review)

**Load `skills/my-style.md`** as the writing style baseline for all content generation and optimization. Follow its commit conventions: save `[user-draft]` before editing, save `[ai-polish]` after.

Read `templates/review-checklist.md` and check each item:
- [ ] Markdown formatting is correct (no broken links, proper heading hierarchy)
- [ ] Title is compelling and appropriate for each platform
- [ ] Article has a summary/abstract
- [ ] Tags are relevant and sufficient
- [ ] Images are present and accessible

Generate platform-adapted versions for each target platform:
- Read `templates/platform-styles.md` for each platform's style guidelines
- **Xiaohongshu:** Extract key points, add emojis, generate hashtags, keep 500-1000 chars
- **Twitter:** Generate a 280-char version or split into a thread
- **Mowen:** Keep original long-form, optimize formatting
- **WeChat:** Optimize layout, generate summary (<=120 chars)

Present optimization suggestions and adapted versions. Wait for user confirmation using `AskUserQuestion`:
- "Accept all suggestions"
- "Accept with modifications" (let user edit)
- "Skip optimization, use original"

### 3. Cover Image Generation (unless --skip-cover or cover already exists)

If the article has no cover image:
- Generate a cover image prompt based on article content
- Call image generation tool if available (DALL-E, etc.)
- Or suggest the user provide a cover image
- Platform-specific sizes: WeChat needs 900x383, Xiaohongshu prefers vertical

### 4. Preview

Display the final version for each platform in the terminal:
- Platform name + content preview + word/character count
- Image list
- Any platform-specific metadata (tags, summary, etc.)

Wait for final confirmation using `AskUserQuestion`:
- "Publish to all platforms"
- "Publish to selected platforms only"
- "Cancel"

### 5. Auto-Publish

For each target platform, read `platforms/<name>.md` to get the publishing method:

**A) Platforms with dedicated MCP Server (Mowen / Xiaohongshu):**
- Directly call the MCP tool (e.g., `create_note` / `add_note`)
- Requires the corresponding MCP Server to be installed and configured in Claude Code
- Faster, more stable, no browser dependency

**B) Platforms without dedicated MCP (WeChat / Twitter):**
- Use Chrome DevTools MCP to automate browser operations
- Follow step-by-step instructions from the platform guide
- Take a screenshot after each major step for verification
- On error: pause and report to user, ask how to proceed

**Publishing order:** Publish to platforms sequentially (not in parallel) to avoid conflicts.

**Error handling:**
- If a platform fails, continue with remaining platforms
- Report all failures at the end
- Offer to retry failed platforms

### 6. Result Report

Display a summary table:

```
Platform      | Status  | Link                    | Notes
------------- | ------- | ----------------------- | -----
Mowen         | Success | https://mowen.cn/...    |
Xiaohongshu   | Success | https://xiaohongshu.com/... |
WeChat        | Failed  | —                       | Session expired, please re-login
Twitter       | Success | https://x.com/...       |
```

For browser-automated platforms, include a screenshot of the published content.

After publishing, if the user made manual edits during the review step, remind them:
"You made edits to the article. Run `/iterate-style <file>` to update your writing style."

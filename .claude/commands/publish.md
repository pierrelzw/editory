Publish a Markdown article to one or more content platforms.

Parse the user's arguments: $ARGUMENTS

The arguments follow this format:
```
<file> [--platforms <platforms>] [--skip-review] [--skip-cover]
```

- `<file>` — Path to the Markdown file to publish
- `--platforms <platforms>` — Comma-separated list: mowen, xiaohongshu, wechat, twitter
- `--skip-review` — Skip the AI content review & optimization step
- `--skip-cover` — Skip cover image generation

## Execute the following workflow:

### Step 1: Parse Input
1. Read the Markdown file specified by `<file>`
2. Parse YAML frontmatter for: title, tags, platforms, cover, type
3. If `--platforms` not specified, use frontmatter `platforms` field
4. If neither, use defaults: mowen, xiaohongshu

### Step 2: AI Content Review & Optimization (unless --skip-review)
1. **Load `.claude/my-style.md`** as the writing style baseline. Follow its commit conventions: save `[user-draft]` before editing, save `[ai-polish]` after.
2. Read `templates/review-checklist.md` and check each item against the article
3. Read `templates/platform-styles.md` for style guidelines
3. Generate platform-adapted versions:
   - **Xiaohongshu:** Extract key points, add emojis, generate hashtags, 500-1000 chars
   - **Twitter:** 280-char version or thread split
   - **Mowen:** Keep long-form, optimize formatting
   - **WeChat:** Optimize layout, generate summary (<=120 chars)
4. Present suggestions and adapted versions to the user
5. Use AskUserQuestion to let user choose: "Accept all", "Accept with modifications", or "Skip, use original"

### Step 3: Cover Image (unless --skip-cover or cover exists in frontmatter)
If no cover image: suggest the user provide one, or generate a prompt for AI image generation.

### Step 4: Preview
Display the final version for each target platform:
- Platform name + content preview + word count
- Image list
- Tags and metadata
Use AskUserQuestion: "Publish to all platforms", "Publish to selected only", or "Cancel"

### Step 5: Auto-Publish
For each target platform, read `platforms/<name>.md` for the publishing guide, then:

**A) Mowen (delegate to post-to-mowen skill):**
Read and follow the `post-to-mowen` skill's SKILL.md workflow, passing `--skip-review` and `--skip-cover` flags as appropriate (review and cover are already handled in Steps 2-3 above).

**A2) Xiaohongshu (browser automation):**
- Use Chrome DevTools MCP following the step-by-step guide in platforms/xiaohongshu.md

**B) WeChat (delegate to post-to-wechat):**
- Read and follow `.claude/commands/post-to-wechat.md` with the article file and any relevant arguments (`--skip-review`, `--skip-cover`, `--theme`, `--color`)
- The post-to-wechat command handles AI review, cover image resolution, and delegates publishing to the baoyu-post-to-wechat skill

**C) Twitter (browser automation):**
- Use Chrome DevTools MCP following the step-by-step guide in platforms/twitter.md
- Take screenshot after each major step
- On error: pause and report to user

Publish sequentially. If one platform fails, continue with the rest. Offer to retry failed platforms.

### Step 6: Result Report
Display a summary table with: Platform | Status | Link | Notes
For browser-automated platforms, include a confirmation screenshot.

If the user made manual edits during the review step, remind them:
"Run `/iterate-style <file>` to update your writing style."

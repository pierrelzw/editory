---
name: post-to-mowen
description: Post a Markdown article to Mowen (墨问). Use when user mentions "发墨问", "post to mowen", or "墨问".
user-invocable: true
allowed-tools:
  - Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/*)
---

Post a Markdown article to Mowen (墨问).

Parse the user's arguments: $ARGUMENTS

```
<file> [--skip-review] [--skip-cover] [--public] [--tags "tag1,tag2"]
```

- `<file>` — Path to the Markdown file to publish
- `--skip-review` — Skip the AI content review & optimization step
- `--skip-cover` — Skip cover image handling
- `--public` — Set note as public after publishing (default: private)
- `--tags` — Comma-separated tags

## Workflow

### Step 1: Read Article

1. Read the Markdown file specified by `<file>`
2. Parse YAML frontmatter for: `title`, `tags`, `mowen_note_id`, `mowen_cover_uuid`

### Step 2: AI Content Review (unless --skip-review)

1. If `.claude/my-style.md` exists in the current project, load it as the writing style baseline
2. Review for long-form readability: formatting, structure, flow
3. Present suggestions to the user
4. Use AskUserQuestion: "Accept all", "Accept with modifications", or "Skip, use original"

### Step 3: Publish

Run the publish script — it handles MD→JSON conversion, image upload, cover insertion, and API call in one step:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/publish_to_mowen.py <file> \
  [--note-id <mowen_note_id>] \
  [--cover-uuid <mowen_cover_uuid>] \
  [--cover <cover_image_path>] \
  [--tags "tag1,tag2"] \
  [--public]
```

Pass `--note-id` and `--cover-uuid` from frontmatter if they exist.
Pass `--tags` from CLI args or frontmatter.
Pass `--public` only if the user explicitly requests public visibility.

The script outputs JSON to stdout: `{"note_id": "xxx", "cover_uuid": "yyy"}`
Progress and warnings go to stderr.

If `--skip-cover` is set, do NOT pass `--cover` or `--cover-uuid`.

### Step 4: Write Back Frontmatter

Parse the script's stdout JSON output. Write the following back into the article's YAML frontmatter (add frontmatter block if absent):

- `mowen_note_id` — the note ID (if newly created)
- `mowen_cover_uuid` — the cover image UUID (if newly uploaded)

### Step 5: Result Report

Display:
- Status (success/failure)
- Note ID
- Cover UUID (if applicable)
- Any warnings from stderr

## Prerequisites

- `MOWEN_API_KEY` env var, or Mowen MCP configured in `~/.claude.json` (key is auto-extracted)
- Python packages: `markdown-it-py`, `requests`

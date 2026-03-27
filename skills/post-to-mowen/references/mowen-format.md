# Mowen JSON Format Reference

## JSON Structure

Mowen uses ProseMirror/TipTap JSON format. Root node is a `doc` with a `content` array of blocks:

```json
{
  "type": "doc",
  "content": [
    {"type": "paragraph", "content": [
      {"type": "text", "text": "Normal text "},
      {"type": "text", "marks": [{"type": "bold"}], "text": "bold"},
      {"type": "text", "marks": [{"type": "highlight"}], "text": "highlighted"},
      {"type": "text", "marks": [{"type": "link", "attrs": {"href": "https://..."}}], "text": "link"}
    ]},
    {"type": "paragraph"},
    {"type": "codeblock", "attrs": {"language": "python"}, "content": [
      {"type": "text", "text": "print('hello')"}
    ]},
    {"type": "image", "attrs": {"uuid": "xxx", "align": "center", "alt": "description"}},
    {"type": "quote", "content": [{"type": "text", "text": "quote content"}]}
  ]
}
```

## Supported Types

**Block types:** `paragraph`, `codeblock`, `image`, `quote`, `audio`, `pdf`, `note` (internal link)

**Inline marks:** `bold`, `highlight`, `link` (with `attrs.href`)

**Not supported:** `code` mark (renders as plain text — the converter preserves backticks instead)

## Image Upload

### Method 1: Local Direct Upload (Recommended)

Two-step REST API via `upload_to_mowen.py`:

1. `POST /api/open/api/v1/upload/prepare` — get OSS upload fields
2. `POST {endpoint}/` — multipart upload to OSS, returns UUID

Limits: images <50MB (jpeg/png/gif/webp), 1 req/sec, 200 files/day.

Requires `MOWEN_API_KEY` environment variable.

### Method 2: URL Upload (Fallback)

MCP `UploadViaURL` tool — for images already at a public URL.

**Important:** Mowen server is in China and cannot access `raw.githubusercontent.com` directly. Use proxy:

```
https://ghfast.top/https://raw.githubusercontent.com/user/repo/branch/path/to/file.png
```

Backup proxies: `https://gh-proxy.com/`, `https://mirror.ghproxy.com/`

## Cover Image

Mowen uses **the first image in the body** as the note's cover. There is no separate cover API.

### Lifecycle (unified for Create and Edit)

- **First publish:** upload cover → get UUID → write `mowen_cover_uuid` to frontmatter → insert into body → publish
- **Subsequent updates:** read `mowen_cover_uuid` from frontmatter → insert into body → update

### Body Structure

Insert cover image directly after title (or after quote if present) — no empty paragraph between:

- With quote: `[title, quote, cover_image, first_body_p, ...]`
- Without quote: `[title, cover_image, first_body_p, ...]`

### Responsibilities

- `md2mowen.py` → article body JSON (headings as bold paragraphs, images with `local` flag)
- Publish workflow → insert cover image + upload images + replace UUIDs

## Note ID Persistence

Articles store `mowen_note_id` in YAML frontmatter:

- **Has `mowen_note_id`** → `EditRichNote(note_id, body)` updates existing note
- **No `mowen_note_id`** → `CreateRichNote(body, settings)` creates new note, write returned ID back to frontmatter

## MCP Tools

- `CreateRichNote` — create and publish rich text note (body JSON + settings with tags)
- `EditRichNote` — full replace (need note_id + complete body)
- `ChangeNoteSettings` — set public/private (section=1 for public)
- `UploadViaURL` — upload image/audio/pdf via public URL (returns UUID)
- `Echo` — connectivity test

# Mowen (mowen.cn) Publishing Guide

## Primary Method: mo-note-mcp-server (Direct MCP via Streamable HTTP)

### Installation

墨问官方 MCP Server 基于 Streamable HTTP 协议，无需本地环境依赖。

```bash
claude mcp add-json mowen '{"type":"streamable-http","url":"https://open.mowen.cn/api/open/mcp/v1/note?key=YOUR_API_KEY"}'
```

**API Key 获取方式：** 在墨问微信小程序中开通会员，然后前往开发者中心获取。

> 官方仓库：https://github.com/we-mowen/mo-note-mcp-server

### MCP Tools

#### `CreateRichNote`
创建并发布富文本笔记。

**支持的富文本格式：** 加粗、高亮、链接、文字引用、笔记内链、图片、音频、PDF。

#### `EditRichNote`
编辑已有笔记内容。

#### `ChangeNoteSettings`
设置笔记公开/私密权限。

#### `UploadViaURL`
通过 URL 上传图片、音频、PDF 文件。

**注意：** 墨问服务器在国内，无法直接访问 `raw.githubusercontent.com`。需要使用 GitHub 代理包装 URL：

```
https://ghfast.top/https://raw.githubusercontent.com/user/repo/branch/path/to/file.png
```

备选代理（如 ghfast.top 不可用）：
- `https://gh-proxy.com/`
- `https://mirror.ghproxy.com/`

### Content Format Conversion

Mowen uses a ProseMirror/TipTap JSON format. Use the converter script to transform Markdown:

```bash
python3 scripts/md2mowen.py article.md          # compact JSON to stdout
python3 scripts/md2mowen.py article.md --pretty  # formatted output
python3 scripts/md2mowen.py -                    # read from stdin
```

The script handles frontmatter stripping, inline formatting, images (with `local` flag for upload workflow), lists, tables, code blocks, and blockquotes.

#### JSON Structure

Root node is a `doc` with a `content` array of blocks:

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

**Supported block types:** `paragraph`, `codeblock`, `image`, `quote`, `audio`, `pdf`, `note` (internal link)

**Supported inline marks:** `bold`, `highlight`, `link` (with `attrs.href`)

**Not supported:** `code` mark (renders as plain text with no visual effect — the script preserves backticks instead)

#### Image Handling in Publish Workflow

The script outputs images in an intermediate format with `src` and `local` flag:
- Local: `{"type": "image", "attrs": {"src": "path/img.png", "local": true, "alt": "..."}}`
- URL: `{"type": "image", "attrs": {"src": "https://...", "local": false, "alt": "..."}}`

The publish workflow then uploads `local: true` images via `UploadViaURL` and replaces attrs with `{"uuid": "xxx", "align": "center", "alt": "..."}`.

#### Note ID Persistence (Create vs Update)

Articles can store `mowen_note_id` in YAML frontmatter to enable updates instead of duplicate creation:

```yaml
---
mowen_note_id: 3thRpsI8EcthpzhpcU5Km
---
```

- **Has `mowen_note_id`** → `EditRichNote(note_id, body)` updates the existing note
- **No `mowen_note_id`** → `CreateRichNote(body, settings)` creates a new note, then the returned ID is written back into the article's frontmatter

---

## Fallback: Chrome DevTools MCP (Browser Automation)

Use this if `mowen-mcp-server` is not available or not configured.

### Prerequisites
- Chrome is running with remote debugging enabled
- User is logged in to mowen.cn (check via `take_snapshot`)

### Steps

1. **Navigate to editor page**
   ```
   navigate_page → https://mowen.cn (find the "write" or compose button)
   ```

2. **Check login status**
   ```
   take_snapshot → check if login page is shown
   ```
   If not logged in: pause and ask user to log in manually.

3. **Fill in content**
   The editor is likely a rich text editor (contenteditable or similar).
   ```
   evaluate_script → interact with the editor's API or DOM to insert content
   ```
   May need to:
   - Focus the editor element
   - Use `document.execCommand` or the editor's internal API
   - Insert HTML converted from Markdown

4. **Upload images**
   If the article contains images:
   ```
   upload_file → select image files through the upload dialog
   ```

5. **Add tags**
   ```
   click → tag input field
   fill → enter tag text
   press_key → Enter (to confirm each tag)
   ```

6. **Publish**
   ```
   click → publish button
   take_screenshot → capture confirmation
   ```

7. **Verify**
   ```
   take_snapshot → confirm the note was published successfully
   ```
   Extract the published URL if visible.

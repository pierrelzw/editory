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

### Content Format Conversion

Markdown must be converted to Mowen's paragraph JSON format:

| Markdown | Mowen JSON |
|---|---|
| Plain paragraph | `{"type": "text", "texts": [{"text": "..."}]}` |
| **Bold text** | `{"text": "...", "bold": true}` |
| > Blockquote | `{"type": "quote", "texts": [...]}` |
| `![](url)` Image | `{"type": "file", "url": "..."}` |
| `[text](url)` Link | `{"type": "link", "url": "...", "text": "..."}` |

**Conversion rules:**
1. Split Markdown into blocks (paragraphs, headings, quotes, code blocks, images)
2. For each block, create the corresponding JSON structure
3. Within text blocks, parse inline formatting (bold, italic, links, code)
4. Headings become text paragraphs with bold formatting
5. Code blocks become text paragraphs with code formatting

### Example

```json
[
  {"type": "text", "texts": [{"text": "Introduction", "bold": true}]},
  {"type": "text", "texts": [{"text": "This is a paragraph with "}, {"text": "bold text", "bold": true}, {"text": " in it."}]},
  {"type": "quote", "texts": [{"text": "This is a blockquote."}]},
  {"type": "file", "url": "https://example.com/image.png"}
]
```

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

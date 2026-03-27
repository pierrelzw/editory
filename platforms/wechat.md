# WeChat Official Account Publishing Guide

> **Legacy Reference:** This document is kept for debugging and troubleshooting. For normal publishing, use `/post-to-wechat` which delegates to the `baoyu-post-to-wechat` skill with battle-tested browser automation.

## Method: Chrome DevTools MCP (Browser Automation)

No dedicated MCP Server available. The primary publishing method now uses the `baoyu-post-to-wechat` skill (via `/post-to-wechat`), which handles Markdown→WeChat HTML conversion, theme styling, and browser automation internally. The manual steps below are retained as reference for debugging.

### Prerequisites
- Chrome is running with remote debugging enabled
- User is logged in to mp.weixin.qq.com (may require QR code scan)

### Content Preparation

WeChat's editor uses rich HTML with inline styles. Markdown must be converted to styled HTML:

1. **Headings** — Convert to `<h2>`, `<h3>` with inline font-size and color styles
2. **Paragraphs** — Wrap in `<p>` with `line-height: 1.75; margin-bottom: 16px`
3. **Bold** — Use `<strong>` tags
4. **Code blocks** — Use `<pre>` with background color and padding
5. **Images** — Must be uploaded to WeChat's CDN first (external URLs not supported)
6. **Links** — WeChat restricts external links; only whitelisted domains work

**Cover image:** 900x383 pixels recommended
**Summary:** Maximum 120 characters

### Steps

1. **Navigate to platform**
   ```
   navigate_page → https://mp.weixin.qq.com
   ```

2. **Check login status**
   ```
   take_snapshot → check if QR login page is shown
   ```
   If not logged in: pause and ask user to scan QR code to log in.

3. **Navigate to article editor**
   ```
   click → "Content & Publishing" or equivalent menu item
   click → "Write new article" or "New draft"
   ```
   Wait for the editor to load.

4. **Fill in title**
   ```
   click → title input field
   fill → enter article title (14 characters or fewer is optimal)
   ```

5. **Fill in author** (optional)
   ```
   click → author field
   fill → enter author name
   ```

6. **Inject HTML body content**
   The content editor is a rich text editor. Inject formatted HTML:
   ```
   evaluate_script →
     // Find the editor element
     const editor = document.querySelector('#edui1_body')
       || document.querySelector('[contenteditable="true"]');
     editor.innerHTML = '<converted HTML content>';
     // Trigger input event so the editor registers the change
     editor.dispatchEvent(new Event('input', { bubbles: true }));
   ```

7. **Upload cover image**
   ```
   click → cover image upload area
   upload_file → select cover image (900x383)
   ```
   Wait for upload to complete.

8. **Fill in summary**
   ```
   click → summary/abstract text area
   fill → enter summary (max 120 characters)
   ```

9. **Preview or publish**
   Two options:
   - **Save as draft:** Click the "Save" button
   - **Preview:** Click "Preview" to send to your WeChat for review
   - **Publish:** Click "Publish" (sends immediately to subscribers)

   ```
   click → desired action button
   take_screenshot → capture confirmation
   ```

10. **Verify**
    ```
    take_snapshot → confirm the article was saved/published
    ```

### Known Selectors (may change)
- Title: `#title` or `input[placeholder*="title"]`
- Editor body: `#edui1_body` or `[contenteditable="true"]`
- Cover image: `.media-cover` or cover upload area
- Summary: `textarea[placeholder*="summary"]` or `.abstract-input`

### Limitations
- External image URLs are not supported; images must be uploaded to WeChat's CDN
- External links are restricted to whitelisted domains
- Rich formatting requires inline styles (WeChat strips `<style>` blocks)
- Session expires relatively quickly; may need frequent re-login via QR code

**Note:** Selectors may change when WeChat updates their platform. Use `take_snapshot` to inspect the current page structure if selectors don't work.

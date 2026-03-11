# Xiaohongshu (Little Red Book) Publishing Guide

## Method: Chrome DevTools MCP (Browser Automation)

### Prerequisites
- Chrome is running with remote debugging enabled
- User is logged in to creator.xiaohongshu.com

### Content Adaptation Rules

When publishing long-form articles to Xiaohongshu, adapt the content:

1. **Extract key points** — Distill the core message into 500-1000 characters
2. **Add emojis** — Use relevant emojis in title and body for engagement
3. **Generate hashtags** — Create relevant topic tags (e.g., #Python #Coding #TechTips)
4. **Image selection** — Choose up to 9 images; vertical format works best
5. **Title style** — Eye-catching with emojis, e.g., "5 Python Tips That 10x Your Productivity!"
6. **Short paragraphs** — Use frequent line breaks, keep paragraphs to 2-3 sentences
7. **Bold keywords** — Emphasize important terms

### Example Adaptation

**Original title:** "Advanced Python Decorator Patterns"
**Adapted title:** "Advanced Python Decorator Patterns You Must Know!"

**Original content (excerpt):**
> Decorators in Python are a powerful feature that allows you to modify the behavior of functions...

**Adapted content:**
> Have you ever wondered how to write cleaner Python code?
>
> Decorators are your secret weapon! Here are the key patterns:
>
> 1. **Basic decorator** — wrap any function with extra logic
> 2. **Parameterized decorators** — pass arguments to customize behavior
> 3. **Class decorators** — for more complex use cases
>
> Save this for later!
>
> #Python #Coding #Programming #TechTips #Developer

---

### Publishing Steps

1. **Navigate to publish page**
   ```
   navigate_page → https://creator.xiaohongshu.com/publish/publish
   ```

2. **Check login status**
   ```
   take_snapshot → check if redirected to login page
   ```
   If not logged in: pause and ask user to log in manually.

3. **Upload images**
   Images must be uploaded first (Xiaohongshu is image-first).
   ```
   upload_file → select image files
   ```
   Wait for upload to complete before proceeding.

4. **Fill in title**
   ```
   click → title input field
   fill → enter the adapted title
   ```

5. **Fill in body content**
   ```
   click → body text area / editor
   fill → enter the adapted content with hashtags
   ```

6. **Add topic tags**
   Look for a hashtag/topic input area:
   ```
   click → topic/tag input
   fill → enter tag text
   click → select from suggestions or press Enter
   ```

7. **Publish**
   ```
   click → publish button
   take_screenshot → capture confirmation
   ```

8. **Verify**
   ```
   take_snapshot → confirm the note was published
   ```
   Extract the published URL if visible.

### Known Selectors (may change)
- Title input: `input[placeholder*="title"]` or `.title-input`
- Content editor: `.ql-editor` or `[contenteditable="true"]`
- Publish button: `.publish-btn` or `button[class*="publish"]`

**Note:** Selectors may change when Xiaohongshu updates their site. Use `take_snapshot` to inspect the current page structure if selectors don't work.

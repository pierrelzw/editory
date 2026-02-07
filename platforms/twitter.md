# Twitter/X Publishing Guide

## Method: Chrome DevTools MCP (Browser Automation)

No dedicated MCP Server available. Publishing is done through browser automation of x.com.

### Prerequisites
- Chrome is running with remote debugging enabled
- User is logged in to x.com

### Content Adaptation Rules

**Single tweet (<=280 characters):**
- Distill the core message into a single concise tweet
- Include 1-2 relevant hashtags
- Add a call to action if appropriate

**Thread (for longer content):**
- First tweet is the "hook" — grab attention
- Each subsequent tweet covers one key point
- Last tweet is a summary or call to action
- Number format: configurable (e.g., "1/5", "[1]", or unnumbered)
- Each tweet in the thread should stand on its own
- Use `@` mentions and `#` hashtags sparingly (1-2 per thread)

**Images:**
- Maximum 4 images per tweet
- Recommended dimensions: 1200x675 (16:9) or 1080x1080 (1:1)

### Steps — Single Tweet

1. **Navigate to compose page**
   ```
   navigate_page → https://x.com/compose/post
   ```

2. **Check login status**
   ```
   take_snapshot → check if login page is shown
   ```
   If not logged in: pause and ask user to log in manually.

3. **Fill in tweet content**
   ```
   click → tweet text area (the main compose box)
   fill → enter tweet content (<=280 characters)
   ```

4. **Upload images** (if any)
   ```
   click → media upload button (camera/image icon)
   upload_file → select image files (max 4)
   ```
   Wait for upload to complete.

5. **Post**
   ```
   click → "Post" button
   take_screenshot → capture confirmation
   ```

6. **Verify**
   ```
   take_snapshot → confirm the tweet was posted
   ```
   Extract the tweet URL if visible.

### Steps — Thread

1. **Post first tweet** (follow single tweet steps above)

2. **For each subsequent tweet:**
   ```
   click → "Reply" on the just-posted tweet, or use the "Add another tweet" button in compose
   fill → enter next tweet content
   click → "Post" / "Reply"
   ```
   Repeat for all tweets in the thread.

3. **Verify thread**
   ```
   navigate_page → the first tweet's URL
   take_snapshot → verify the full thread is visible
   take_screenshot → capture the thread
   ```

### Known Selectors (may change)
- Compose text area: `[data-testid="tweetTextarea_0"]` or `[role="textbox"]`
- Post button: `[data-testid="tweetButton"]` or `[data-testid="tweetButtonInline"]`
- Media upload: `[data-testid="fileInput"]` or `input[type="file"]`
- Reply button: `[data-testid="reply"]`

### Limitations
- 280 character limit per tweet
- Maximum 4 images per tweet, 25 tweets per thread
- Video upload may require longer wait times
- Rate limiting may apply for rapid posting

**Note:** Selectors may change when X updates their site. Use `take_snapshot` to inspect the current page structure if selectors don't work.

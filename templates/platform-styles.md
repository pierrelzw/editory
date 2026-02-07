# Platform Content Style Guide

Guidelines for adapting content to each platform's style and audience expectations.

## Xiaohongshu Style

- **Title:** Eye-catching with emojis, e.g., "5 Python Tips That 10x Your Productivity!"
- **Body:** Short paragraphs, frequent line breaks, bold keywords for emphasis
- **Ending:** Add hashtags: #Python #Coding #TechTips
- **Images:** At least 1 image, recommended 3-9. Vertical format works best (3:4 ratio)
- **Length:** 500-1000 characters recommended
- **Tone:** Casual, friendly, enthusiastic. Use emojis throughout.
- **Structure:** Numbered lists and bullet points work well

### Adaptation Template
```
[Emoji] [Catchy Title]

[1-2 sentence hook]

[Key point 1 with emoji]
[Key point 2 with emoji]
[Key point 3 with emoji]
...

[Call to action: save/like/follow]

#tag1 #tag2 #tag3 #tag4 #tag5
```

## Twitter/X Style

### Single Tweet
- Maximum 280 characters
- One clear, punchy point
- 1-2 hashtags max (don't overdo it)
- End with a question or call to action for engagement
- Use line breaks for readability

### Thread
- **Tweet 1 (Hook):** Grab attention, make people want to read more. Often starts with a bold claim or question.
- **Tweets 2-N (Body):** One key point per tweet. Each should make sense on its own.
- **Final Tweet (Summary):** Recap, call to action, or link to the full article.
- Numbering: "1/" or "[1]" or just unnumbered — configurable
- Include relevant media in 1-2 tweets for visual engagement

### Tone
- Concise, direct
- Conversational but professional
- Use `@` mentions sparingly and only when relevant

## Mowen Style

- **Format:** Long-form is fine — Mowen supports rich text articles
- **Title:** Clear and descriptive, professional tone
- **Body:** Well-structured with headings, subheadings, and clear sections
- **Tags:** Use specific, relevant tags for discoverability
- **Images:** Include inline images where they add value
- **Tone:** Can range from casual to professional depending on content

### Notes
- Mowen supports rich text formatting (bold, italic, quotes, code blocks, images, links)
- Content is converted to Mowen's paragraph JSON format (see platforms/mowen.md)
- Minimal adaptation needed — keep the original article's structure and tone

## WeChat Official Account Style

- **Title:** 14 characters or fewer is optimal for display. Clear, informative, no clickbait.
- **Cover image:** Required. 900x383 pixels recommended.
- **Summary:** Maximum 120 characters. Concise abstract of the article.
- **Body:** Long-form OK. Focus on visual formatting:
  - Use section headers with clear styling
  - Add spacing between sections
  - Indent or highlight key quotes
  - Use images to break up long text
- **Tone:** Professional, authoritative. WeChat audiences expect polished content.
- **Links:** External links are restricted to whitelisted domains. Use sparingly.
- **Images:** Must be uploaded to WeChat CDN (external URLs not supported)

### Formatting Notes
- WeChat strips `<style>` blocks — all styles must be inline
- Use `<section>` tags for layout sections
- Color and font styling supported via inline CSS
- Code blocks need explicit background/padding styling

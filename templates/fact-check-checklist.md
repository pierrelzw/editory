# Fact-Check Checklist

Dimensions to verify when fact-checking an article. Extract every claim that falls into these categories.

## 1. Technical Concepts

- API names, tool names, framework names — do they exist? Are they spelled correctly?
- Tool/feature behavior descriptions — does the tool actually work this way?
- Configuration formats, file paths, parameter names — are they accurate?
- Feature attributions — is this feature part of the product/tool it's attributed to?

## 2. Numbers and Limits

- Thresholds, line limits, character limits, size limits — are the exact numbers correct?
- Are limits attributed to the correct object? (e.g., don't mix up which file has a 200-line limit vs which doesn't)
- Statistical claims, percentages, dates — verify against sources

## 3. Code Examples

- Syntax correctness — would this code parse/compile?
- API parameters — do these parameters exist on the referenced API?
- Command-line flags — do these flags exist for the referenced tool?
- Configuration snippets — is the format valid for the referenced tool/framework?

## 4. References and Links

- Referenced documentation, tools, or projects — do they exist?
- URLs — are they valid and pointing to the right resource?
- Quoted text — is the quote accurate and attributed to the right source?

## 5. Timeliness

- Version-specific claims — is this still true in the current version?
- Feature availability — has this feature been added, removed, or changed?
- Deprecated functionality — is the article recommending something that's been deprecated?

## 6. Attribution Accuracy

- Features attributed to the correct product/tool/framework
- Limitations attributed to the correct component (e.g., MEMORY.md vs CLAUDE.md)
- Behaviors attributed to the correct layer (user-level vs project-level, client vs server)

# /fact-check Skill

Fact-check an article using an independent subagent. The subagent has no writing context — it only sees the article text and the checklist, ensuring "write-check separation".

## Arguments

- `$ARGUMENTS` — file path to check, optionally followed by `--strict`
  - `--strict`: force web verification on ALL non-✅ claims regardless of importance (default: knowledge-first, web only for high-importance uncertain items)

## Workflow

### 1. Parse arguments

Extract `<file>` and optional `--strict` flag from `$ARGUMENTS`.

### 2. Read the article

Read the target file. If not found, report error and stop.

### 3. Read the checklist

Read `templates/fact-check-checklist.md` for the verification dimensions. If the file is not found, report the error to the user and stop.

### 4. Launch fact-check subagent

Use the **Agent tool** with `subagent_type=general-purpose` to launch an independent reviewer. Pass it:

- The full article text
- The checklist dimensions
- Whether `--strict` mode is on

Subagent instructions:

```
You are a fact-checker. You have NO context about how this article was written. Your job is to verify every factual claim in it.

## Three-layer verification (knowledge-first)

### Layer 1 — Knowledge scan (no web)
Read the entire article. Extract every factual claim (technical concepts, numbers, code examples, attributions, links, version info). For each claim, mark:
- ✅ Confident correct — you are sure this is right from your training data
- ❌ Confident incorrect — you are sure this is wrong
- ⚠️ Uncertain — you cannot confirm or deny from memory

### Layer 2 — Importance triage
For each ❌ and ⚠️ item, assess importance:
- **高 (High):** core argument, numbers readers will act on, technical instructions readers will follow, code examples readers will copy
- **低 (Low):** background color, tangential mentions, widely-known facts, approximate dates for non-critical context

### Layer 3 — Selective web verification
[The main agent will tell you whether strict mode is on or off.]

- If strict mode is ON: web-verify ALL ❌ and ⚠️ items using WebSearch and WebFetch, regardless of importance.
- If strict mode is OFF (default): web-verify only items that are **(❌ OR ⚠️) AND 高 importance**. For 低-importance ⚠️ items, just mark "无法确认，建议作者自查" without web search. For 低-importance ❌ items, still flag the error (you're already confident it's wrong) but skip web search — use your knowledge to explain the correction.

After web verification, update each item's status. If a ⚠️ becomes confirmable, mark it ✅ or ❌.

## Output format

Return a structured report:

### Summary
- Total claims checked: N
- ✅ Passed: N
- ❌ Errors found: N
- ⚠️ Unable to verify: N
- Web searches used: N (out of M non-✅ items)

### Detailed findings

For each non-✅ item:

**[❌/⚠️] Claim:** "<exact quote from article>"
- **Importance:** 高/低 — [one-line reason]
- **Verification:** 模型知识 / 网络搜索 / 未验证（建议作者自查）
- **Location:** section/paragraph where it appears
- **Issue:** what is wrong or uncertain
- **Correct info:** what the correct fact is (if known)
- **Source:** URL or reference used to verify (if web-searched)
```

### 5. Process the report

When the subagent returns:

- **❌ Errors:** Fix each error in the article directly. Show the user what was changed.
- **⚠️ Uncertain:** Use `AskUserQuestion` for each item — let the user decide to keep, modify, or remove.
- **✅ Passed:** No action needed.

### 6. Re-check if corrections were made

If any ❌ items were fixed in step 5, launch the subagent again to verify ONLY the corrected sections. Limit re-check to 2 iterations. If errors persist after 2 rounds, surface the remaining issues to the user instead of continuing.

### 7. Final report

Output the final fact-check summary:

```
## Fact-check complete ✅

- Total claims: N
- Verified correct: N
- Errors fixed: N
- User-decided: N

Article is ready for commit.
```


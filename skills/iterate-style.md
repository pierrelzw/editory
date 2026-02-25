# /iterate-style Skill

Analyze the diff between AI-generated content and user's manual edits, extract writing preferences, and update `skills/my-style.md`.

## Trigger

```
/iterate-style <file> [--commit <commit-hash>]
```

**Arguments:**
- `<file>` — Path to the article file (after user's manual edits)
- `--commit <hash>` — (Optional) Specific commit to diff against. If omitted, auto-detect.

## Supported Scenarios

### Scenario A: AI Draft (wrote from scratch)

Commit history looks like:
```
[ai-draft] article.md   ← AI wrote this
... user edits ...       ← user's changes in working tree
```

Two-way diff: `[ai-draft]` commit vs current working tree.

Signal extracted:
- What AI wrote that user deleted → potential forbidden patterns
- What user added that AI didn't write → missing style elements
- What user rephrased → preferred expressions

### Scenario B: AI Polish (optimized user's draft)

Commit history looks like:
```
[user-draft] article.md  ← user's original
[ai-polish] article.md   ← AI's polished version
... user edits ...        ← user's review in working tree
```

Three-way diff: `[user-draft]` → `[ai-polish]` → current working tree.

Signals extracted:
- AI changed A→B, user kept B → **good optimization**, reinforce in style guide
- AI changed A→B, user reverted to A → **unwanted change**, add to forbidden list
- AI changed A→B, user changed to C → **right direction, wrong execution**, record user's preferred expression
- AI left something unchanged, user changed it → **missed opportunity**, note for future

## Workflow

### 1. Detect Scenario

Find relevant commits for the given file:

```bash
# Find most recent [ai-draft] or [ai-polish] commit
git log --grep="\[ai-draft\]\|\[ai-polish\]\|\[user-draft\]" --format="%H %s" -- <file>
```

- If `[ai-polish]` found → Scenario B (three-way)
- If `[ai-draft]` found → Scenario A (two-way)
- If nothing found → fall back to `git diff HEAD -- <file>`, warn user

If `--commit` is provided, use that commit directly.

### 2. Generate Diff

```bash
# Scenario A
git diff <ai-draft-commit> -- <file>

# Scenario B
git diff <user-draft-commit> <ai-polish-commit> -- <file>   # what AI changed
git diff <ai-polish-commit> -- <file>                        # what user changed after AI
```

### 3. Analyze Changes

For each change, classify it:

- **Deletion**: User removed something AI wrote. Why? (filler, wrong tone, forbidden pattern?)
- **Addition**: User added something AI didn't write. Why? (missing context, personal touch, specific detail?)
- **Rephrasing**: User kept the meaning but changed the words. What's the pattern? (simpler words, shorter sentences, different structure?)
- **Reversion** (Scenario B only): User undid AI's change. What should AI not touch?
- **Acceptance** (Scenario B only): User kept AI's change. What did AI do right?

Summarize findings as concrete, actionable rules. Each rule should have:
- A clear description
- An example (before → after)
- Which section of `my-style.md` it belongs to

### 4. Update my-style.md

Read current `skills/my-style.md` and merge new rules:

**Deduplication:** Compare each new rule against existing rules. If a rule already exists (same meaning, different wording), skip it.

**Consolidation:** If the forbidden list exceeds 20 items, group similar items:
- Before: "禁用深耕", "禁用赋能", "禁用闭环", "禁用抓手"
- After: "禁用商业黑话：深耕、赋能、闭环、抓手等"

**Contradiction detection:** If a new rule conflicts with an existing rule, present both to the user and ask which to keep.

**Update the iteration log** in `skills/my-style-log.md` (separate file to avoid wasting tokens during normal writing):

| # | Date | Article | Scenario | Edit % | New Rules |
|---|------|---------|----------|--------|-----------|
| N | today | filename | draft/polish | X% | summary |

Edit % = lines changed by user / total lines in AI version.

### 5. Present Summary

Show the user:

```
## Style Iteration Summary

**Article:** <filename>
**Scenario:** AI Draft / AI Polish
**Edit rate:** X% (Y lines changed out of Z)

### New rules added:
- [Style] Added: prefer "做了十几年" over "深耕多年"
- [Forbidden] Added: "不可否认的是" — user deleted 2 instances

### Rules reinforced:
- [Style] Short paragraphs confirmed — user broke 3 long paragraphs into shorter ones

### No changes needed:
- Opening style matched — user kept the conversational opening
```

### 6. Commit the Update

```bash
git add skills/my-style.md skills/my-style-log.md
git commit -m "[style-update] iterate from <filename>: +N rules, edit rate X%"
```

## Edge Cases

- **No changes detected:** User accepted AI output as-is. Log it (edit rate 0%) but don't modify style. This is a positive signal — the style is working.
- **Massive rewrites (edit rate > 80%):** The style skill may be far off. Suggest the user review the entire style document, or provide more sample articles for re-analysis.
- **File not in git:** Cannot diff. Ask user to commit the file first, or provide the AI draft manually via `--commit`.

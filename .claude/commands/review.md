# Article Review Expert Panel

Review a Markdown article by launching multiple virtual expert reviewers in parallel. Each expert evaluates the article from a different perspective and provides specific, actionable feedback.

## Arguments

\$ARGUMENTS should contain: `<file_path> [--experts <list>] [--readers <profile>] [--iterate]`

- `file_path` (required): path to the article to review
- `--experts`: which experts to use (default: core 3)
  - "全部" / "all" → all 6 experts
  - Comma-separated names: "小白,逻辑,反方" or "novice,logic,devil"
  - Natural language: "帮我看看逻辑" → adds 逻辑审查员
  - Default (no flag): core 3 (小白试读员, 结构编辑, 增长顾问)
- `--readers`: reader profile description (e.g., "技术人员" or "大学生")
- `--iterate`: compare against previous review's 🔴 items

## Expert Roster

| File                                    | Expert | Group    |
| --------------------------------------- | ------ | -------- |
| `templates/experts/novice-reader.md`    | 小白试读员  | Core     |
| `templates/experts/structure-editor.md` | 结构编辑   | Core     |
| `templates/experts/growth-advisor.md`   | 增长顾问   | Core     |
| `templates/experts/logic-reviewer.md`   | 逻辑审查员  | Extended |
| `templates/experts/devil-advocate.md`   | 反方辩手   | Extended |
| `templates/experts/fact-checker.md`     | 事实审查员  | Extended |

## Workflow

### Step 1: Parse arguments

Extract file path from \$ARGUMENTS. Determine expert selection:

- No `--experts` flag → core 3 (小白试读员, 结构编辑, 增长顾问)
- `--experts 全部/所有/全面/complete/all` → all 6
- `--experts <names>` → fuzzy match names to expert files, then **union with core 3** (add matches to core, don't replace):
  - 小白/novice → novice-reader.md
  - 结构/structure → structure-editor.md
  - 增长/growth → growth-advisor.md
  - 逻辑/logic → logic-reviewer.md
  - 反方/devil → devil-advocate.md
  - 事实/fact → fact-checker.md
  - Mixed Chinese/English supported (e.g., "逻辑,devil")
- Natural language (e.g., "帮我看看逻辑") → extract recognizable keywords, add matched experts to core 3
- Unrecognizable input → default to core 3 and inform user: "无法识别专家名称，使用默认核心三人组"

If `--readers` is provided, note the reader profile for passing to experts.

### Step 2: Read article

Read the article file. If the file doesn't exist, tell the user and stop.

If `--iterate` is specified: first try to read the sidecar file `<article-path>.review.md` for the previous action list. If the sidecar file doesn't exist, fall back to searching conversation history for the most recent `<!-- review-action-list -->` block. Extract previous 🔴 items as iteration context. If no previous review found in either location, proceed with a fresh review and inform the user.

### Step 3: Read expert definitions

Read each selected expert's definition file from `templates/experts/`. These files contain the persona, mission, focus areas, and output format for each expert.

### Step 4: Launch expert subagents in parallel

For each selected expert, launch a subagent (using the Agent tool with subagent\_type "general-purpose") with this prompt template:

```
You are a professional article reviewer. Read the expert definition below and stay fully in character.

## Your Expert Role
[contents of the expert's .md file]

## Reader Profile
[if --readers provided: the reader profile; otherwise: "一般读者 — 对该话题有基本兴趣但无专业背景"]

## Article to Review
[full article text]

[If --iterate: "## Previous Issues (mark each as ✅已解决 / ⚠️部分解决 / ❌未解决)\n" + previous 🔴 items]

Review the article strictly according to your role's Output Format (including its word cap). Be specific — quote the article text when flagging issues. Output in Chinese.

Do not suggest changes that contradict the author's style guide (if provided below).

[If style file ~/.claude/my-style.md exists and expert is 结构编辑 or 增长顾问: "## Author Style Constraints\n" + key style rules summary]
```

Launch subagents in two batches:

- **Batch 1 (Core):** 小白试读员, 结构编辑, 增长顾问 — launch concurrently
- **Batch 2 (Extended):** 逻辑审查员, 反方辩手, 事实审查员 — launch after Batch 1 completes

If only core experts are selected, launch all in a single batch.

### Step 5: Display results

For each expert's response, display with clear separators:

```
═══════════════════════════════════════
📋 [Expert Chinese Name] 审稿意见
═══════════════════════════════════════

[expert's review output]

```

### Step 6: Synthesize action list

After all experts have reported, synthesize a unified, deduplicated action list. Prioritize by severity:

```
## 📝 综合行动清单

🔴 必须修改（阻塞发布）
1. [action item — source: expert name]
2. ...

🟡 建议修改（显著提升质量）
1. [action item — source: expert name]
2. ...

🟢 锦上添花
1. [action item — source: expert name]
2. ...
```

Rules for synthesizing:

- Merge similar feedback from different experts into one item
- Signal mapping from expert output to priority:
  - Expert ❌ → 🔴
  - Expert ⚠️ on core argument/structure → 🔴
  - Expert ⚠️ on peripheral point → 🟡
  - Expert 💡 suggestion with high impact → 🟡
  - Expert 💡 suggestion with low impact → 🟢
  - Multiple experts flagging same issue → escalate one level
- 🔴: factual errors, logical fallacies, major confusion points, broken structure
- 🟡: weak opening/ending, missing transitions, unclear analogies, poor title
- 🟢: minor wording, optional enhancements, nice-to-have additions

After displaying, persist the action list in two places:

1. Output in conversation (hidden from display):

```
<!-- review-action-list -->
🔴 items listed here for --iterate to pick up
<!-- /review-action-list -->
```

2. Write to sidecar file `<article-path>.review.md` with the full action list (🔴🟡🟢) so `--iterate` can read it in future sessions.

> **Note:** `templates/review-checklist.md` is used by `/publish` for pre-flight formatting/metadata checks. `/review` focuses on content quality via expert panel — this is a deliberate scope separation.

### Step 7: Suggest next steps

Based on the review results:

- If 🔴 items exist: "建议先处理 🔴 项，然后运行 `/review <file> --iterate` 复查"
- If 事实审查员 flagged ⚠️/❌: "建议运行 `/fact-check <file>` 做深度事实核查"
- If all clean: "文章质量不错！可以运行 `/publish <file>` 发布了"


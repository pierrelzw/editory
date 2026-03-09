---
type: mixed
density: balanced
style: blueprint
image_count: 3
---

## Illustration 1
**Position**: After "Git 是什么？" section (after the time machine + parallel universe explanation)
**Purpose**: Visualize the core Git metaphor — time machine (commits) + parallel universe (branches)
**Type**: framework
**Visual Content**: A blueprint-style diagram showing two concepts side by side: Left side shows a vertical timeline of commit snapshots (labeled "时光机"), with arrows pointing back showing "checkout" ability. Right side shows branching paths diverging from a main line (labeled "平行宇宙"), with one branch merging back and another being discarded. Clean engineering lines, blueprint grid background.
**Filename**: 01-framework-git-concepts.png

## Illustration 2
**Position**: After "从 6 个基础命令开始" heading (before the individual command sections)
**Purpose**: Overview of the 6 essential commands and their relationships
**Type**: flowchart
**Visual Content**: A blueprint-style flowchart showing the 6 commands in a logical workflow: init → add → commit → log/diff (branch off for viewing) → checkout (for reverting) → branch (for experimenting). Each command shown as a blueprint node with a one-word Chinese description. Arrows show the typical workflow order. Color-coded: blue for basic flow, amber for "safety" commands (checkout, diff).
**Filename**: 02-flowchart-six-commands.png

## Illustration 3
**Position**: After "让 Claude Code 帮你自动存档" section
**Purpose**: Show the recommended workflow — commit before and after Claude edits
**Type**: infographic
**Visual Content**: A blueprint-style infographic showing the ideal workflow: [Commit checkpoint] → [Claude edits] → [Review diff] → [Commit checkpoint]. Shown as a horizontal pipeline with engineering-style connectors. Key labels: "存档" before Claude, "git diff 检查" after Claude, "再次存档" at the end. A safety net icon at the bottom labeled "你的安全网".
**Filename**: 03-infographic-workflow.png

---
illustration_id: 02
type: flowchart
style: blueprint
---

6 Essential Git Commands - Process Flow

Layout: top-down with branching

STEPS:
1. "git init" - 开启存档 (Start tracking) — top of flow, single entry point
2. "git add + commit" - 存档 (Save checkpoint) — main flow, largest node
3. "git log" - 查看历史 (View history) — branches right from commit
4. "git diff" - 对比变化 (Compare changes) — branches right from commit, next to log
5. "git checkout" - 回退版本 (Revert) — branches left from commit, with arrow looping back up
6. "git branch" - 平行宇宙 (Parallel universe) — branches left from main flow, showing diverge and merge back

CONNECTIONS:
- Main flow: init → add+commit (thick blue arrow, primary path)
- From commit, branch right to log and diff (thin lines, "查看类" viewing commands)
- From commit, branch left to checkout and branch (thin lines, "操作类" action commands)
- checkout has a dashed arrow looping back to previous commit state
- branch has arrow showing merge back to main flow

LABELS:
- Each command in monospace font: `git init`, `git add`, etc.
- Chinese one-word description next to each
- Color coding: Blue for basic flow (init, add, commit), Amber for safety/viewing (log, diff, checkout), Light blue for advanced (branch)

COLORS:
- Background: Blueprint Off-White (#FAF8F5) with subtle grid
- Primary flow: Engineering Blue (#2563EB) thick arrows
- View commands: Navy Blue (#1E3A5F)
- Safety commands: Amber (#F59E0B)
- Node fills: Light Blue (#BFDBFE)
- Text: Deep Slate (#334155)

STYLE: Precise technical blueprint style. Clean geometric nodes (rounded rectangles). Straight arrows with 90-degree bends only. Consistent stroke weights. Grid-aligned layout. Engineering precision. No hand-drawn elements.

Clean composition with generous white space. Simple blueprint grid background.

Text should be large and prominent. Keep minimal, focus on command names and one-word descriptions.

ASPECT: 16:9

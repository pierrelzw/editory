---
strategy: b
name: Information-Dense
style: notion
style_reason: "Minimalist hand-drawn line art matches the intellectual, knowledge-sharing nature of a config guide"
elements:
  background: grid
  decorations: [arrows, brackets]
  emphasis: underline
  typography: monospace-mix
layout: dense
image_count: 6
---

## P1 Cover
**Type**: cover
**Hook**: "Claude Code 配置全景图 | 8 种配置一篇讲清"
**Visual**: Clean title card with config type icons arranged in a grid
**Layout**: sparse

## P2 Config Overview
**Type**: info-card
**Message**: 8 config types with one-line descriptions, newcomer priority marked
**Visual**: Table/list with icons, top 3 highlighted
**Layout**: dense

## P3 CLAUDE.md Deep Dive
**Type**: detail-card
**Message**: Where to put it (3 locations + priority), minimal example, common mistakes
**Visual**: File tree diagram + code block
**Layout**: dense

## P4 settings.json + Skills
**Type**: detail-card
**Message**: Permission control example + Skill creation in 3 steps
**Visual**: Two-column layout, code examples
**Layout**: comparison

## P5 Advanced: Rules + Hooks + MCP
**Type**: info-card
**Message**: Quick overview of rules (path-based), hooks (lifecycle), MCP (external tools)
**Visual**: Three mini-sections with key examples
**Layout**: dense

## P6 Ending
**Type**: ending
**Message**: "Config is iterative" + /status tip + save CTA
**Visual**: Checklist with checkmarks
**Layout**: balanced

---
strategy: c
name: Visual-First (视觉优先型)
style: chalkboard
style_reason: "黑板教学风格，粉笔字 + 黑色背景，教程感最强，适合'课堂'氛围"
elements:
  background: chalkboard-dark
  decorations: [chalk-lines, chalk-arrows]
  emphasis: chalk-underline
  typography: chalk-handwritten
layout: balanced
image_count: 4
---

## P1 Cover
**Type**: cover
**Hook**: "Claude Code 新手必修课：Git 存档术"
**Visual**: 黑板上大字标题，粉笔画的 Git 分支图，教室氛围
**Layout**: sparse
**Slug**: git-class

## P2 Problem + Solution
**Type**: content
**Message**: 改坏了回不去？因为你没有"存档"→ Git 就是你的存档键
**Visual**: 黑板上画 Before（混乱）→ After（有序的 Git 时间线）
**Layout**: comparison
**Slug**: before-after

## P3 Cheat Sheet
**Type**: content
**Message**: 6 个命令速查表
**Visual**: 黑板上整齐排列 6 个命令，粉笔手写风格，配彩色粉笔高亮关键词
**Layout**: dense
**Slug**: cheat-sheet

## P4 Ending
**Type**: ending
**Message**: 下课！记得先 git init
**Visual**: 黑板右下角写 "git init" 大字，左边写 CTA 互动文字
**Layout**: sparse
**Slug**: class-dismissed

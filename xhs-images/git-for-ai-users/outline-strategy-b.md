---
strategy: b
name: Information-Dense (信息密集型)
style: notion
style_reason: "极简手绘线条 + 知识卡片风格，最适合 Git 教程干货，专业而不枯燥"
elements:
  background: solid-white
  decorations: [hand-drawn-lines, arrows-curvy]
  emphasis: circle-mark
  typography: handwritten
layout: dense
image_count: 6
---

## P1 Cover
**Type**: cover
**Hook**: "用 Claude Code 不学 Git？6 个命令就能避免改坏回不去"
**Visual**: 大标题 + Claude Code logo + Git logo，极简线条装饰，干净有力
**Layout**: sparse
**Slug**: git-for-claude

## P2 Pain Points
**Type**: content
**Message**: 没有"存档"的 6 个代价
**Visual**: 6 个痛点用编号列表展示，每个配简笔画图标（❌ 文件丢失、🔀 版本混乱、💥 协作灾难...）
**Layout**: list
**Slug**: six-costs

## P3 Concept
**Type**: content
**Message**: Git = 时光机 + 平行宇宙
**Visual**: 手绘示意图：左边时间线（commit 节点），右边分支图（branch 分叉）
**Layout**: balanced
**Slug**: git-concept

## P4 Commands Part 1
**Type**: content
**Message**: 基础三件套：init + add/commit + log
**Visual**: 3 个命令卡片，每个包含命令、一句话说明、使用场景
**Layout**: dense
**Slug**: commands-basics

## P5 Commands Part 2
**Type**: content
**Message**: 进阶三件套：diff + checkout + branch
**Visual**: 3 个命令卡片，每个包含命令、一句话说明、对应痛点
**Layout**: dense
**Slug**: commands-advanced

## P6 Ending
**Type**: ending
**Message**: 让 Claude 自动存档 + 行动号召
**Visual**: CLAUDE.md 配置示例 + "下次打开 Claude Code 之前先 git init" + 互动引导
**Layout**: balanced
**Slug**: auto-save-cta

# baoyu-skills：用 Claude Code 给文章配图，我跑了三个 Demo

> 从封面图到小红书系列到文章插图，一套 Markdown 技能包就能搞定。

---

前几天我在折腾 editory 项目的时候，发现仓库里有个 `baoyu-skills/` 目录，打开一看 —— 二十多个 skill，从生成封面图到做小红书图文到画漫画，全都有。

但光看文档看不出什么感觉。于是我挑了三个视觉类的 skill，拿自己的文章跑了一遍。

这篇文章就是把跑的过程记下来，帮你理解 baoyu-skills 到底是什么、怎么工作的。

## baoyu-skills 是什么

一句话：**给 Claude Code 用的第三方技能包，专注 AI 内容生成。**

作者是宝玉（JimLiu），把图片生成、内容发布、格式转换这些常用操作，封装成了 Claude Code 的 skill。每个 skill 就是一个 `SKILL.md` 文件，加上一些 TypeScript 脚本。

不需要装 npm 包，用 `npx -y bun` 就能跑。

技能分三大类：

- **内容生成类** —— 封面图、小红书图文、文章插图、幻灯片、漫画
- **AI 后端类** —— 图像生成引擎（调用 Google Gemini / OpenAI 的 API）
- **工具类** —— URL 转 Markdown、图片压缩、翻译

我这次跑的三个 demo 都是内容生成类，它们底层都调用 `baoyu-image-gen` 这个 AI 后端 skill 来生成图片。

## 前置准备

跑之前需要两样东西：

**1. 图像生成 API key**

baoyu-skills 支持 Google Gemini、OpenAI、阿里通义万象、Replicate 四个 provider。我用的是 Google Gemini。

注意：Google 免费层的图片生成配额是 0 —— 我一开始就被这个坑了，换了付费 key 才跑通。

API key 放在 `~/.baoyu-skills/.env` 里：

```
GOOGLE_API_KEY=your-key-here
```

**2. 首次设置（EXTEND.md）**

每个 skill 第一次运行时会问你一堆偏好问题 —— 要不要水印、默认风格、默认宽高比、输出目录放哪。回答完后保存为 `EXTEND.md`，下次就不用再设了。

这个设计挺聪明的：偏好跟着项目走（`.baoyu-skills/skill-name/EXTEND.md`），也可以放用户级（`~/.baoyu-skills/skill-name/EXTEND.md`），跨项目通用。

## Demo 1：封面图（baoyu-cover-image）

**文章**：《让 AI 先计划再写代码》

这是最简单的一个 skill —— 给一篇文章生成一张封面图。

### 它的工作流

整个过程分 5 步：

**Step 0：加载偏好** —— 读 EXTEND.md，没有就触发首次设置。这一步是阻塞的，必须完成才能继续。

**Step 1：分析内容** —— 读文章，提取主题、语气、关键词、视觉隐喻。我那篇文章讲的是从混乱的 vibe coding 到有序的 plan 模式，所以分析出来的核心隐喻是"从混乱到清晰的路径"。

**Step 2：确认选项** —— 这一步最有意思。baoyu-cover-image 用 **五个维度** 来定义一张封面图：

- **Type** —— hero / conceptual / typography / metaphor / scene / minimal
- **Palette** —— warm / elegant / cool / dark / earth / vivid / pastel / mono / retro
- **Rendering** —— flat-vector / hand-drawn / painterly / digital / pixel / chalk
- **Text** —— none / title-only / title-subtitle / text-rich
- **Mood** —— subtle / balanced / bold

每个维度都有自动选择规则。比如文章里有"个人故事、经验分享"这些信号，palette 就自动匹配 warm；有"哲学、反思、成长"信号，type 就匹配 metaphor。

我那篇文章最终选的是：metaphor + warm + hand-drawn + title-only + balanced。

**Step 3：生成 prompt** —— 把分析结果和维度选择组装成一个详细的图片生成 prompt，保存为 `prompts/cover.md`。这个 prompt 里有配色的具体 hex 值、构图描述、文字内容、渲染风格说明。

**Step 4：调用图片生成** —— 把 prompt 文件传给 `baoyu-image-gen`，指定 provider、宽高比、画质。底层是调 Google Gemini 的图片生成 API。

**Step 5：输出报告** —— 告诉你生成了什么、放在哪。

### 实际效果

生成了一张 3:4 竖版封面：手绘风格，一个小人从左下角的混乱代码（Chaos）沿着蜿蜒路径走向右侧的有序步骤（PLAN → DEFINE → STRUCTURE → IMPLEMENT → Clarity）。标题"让 AI 先计划再写代码"。

从输入文章到拿到图片，整个过程大概 2 分钟。

### 输出的文件结构

```
cover-image/plan-before-coding/
├── prompts/cover.md    # 图片生成 prompt
└── cover.png           # 生成的封面图
```

## Demo 2：小红书图文系列（baoyu-xhs-images）

**文章**：《Claude Code 配置，我一开始全做错了》

这个 skill 复杂得多 —— 把一篇长文拆成 N 张小红书风格的信息图卡片。

### 它的工作流

**Step 0：加载偏好** —— 同上。

**Step 1：内容分析** —— 分析文章，判断内容类型（干货教程）、目标受众（Claude Code 新手）、爆款潜力（高收藏、中分享）、视觉机会。保存为 `analysis.md`。

**Step 2：确认理解** —— 问你核心卖点是什么、受众风格偏好。我选了"经验教训 + 全景配置指南"和"自动匹配"。

**Step 3：生成 3 个大纲变体** —— 这一步是亮点。skill 会生成三个完全不同的策略：

- **Strategy A：故事驱动** —— 从"我做错了"开始，个人经历线索，warm 风格，5 张
- **Strategy B：信息密集** —— 全景图 + 深入讲解，notion 风格，6 张
- **Strategy C：视觉优先** —— 极简设计，图表为主，minimal 风格，4 张

每个策略不光是大纲不同，连推荐的视觉风格都不同。

**Step 4：确认选择** —— 我选了 Strategy C（视觉优先，4 张），但风格换成了 chalkboard（黑板粉笔风）。

这里体现了 baoyu-xhs-images 的 **Style × Layout 二维设计**：

- **Style** 控制视觉美学 —— cute / fresh / warm / bold / minimal / retro / pop / notion / chalkboard / study-notes
- **Layout** 控制信息结构 —— sparse / balanced / dense / list / comparison / flow / mindmap / quadrant

两个维度自由组合。比如 chalkboard + dense 就是"黑板上写满知识点"的感觉，chalkboard + sparse 就是"黑板上只写一句话"的感觉。

**Step 5：逐张生成** —— 这里有个关键细节：**reference image chain**。

第一张图（封面）不带 `--ref` 参数，作为"视觉锚点"。后面所有图片都带上 `--ref 01-cover.png`，让 AI 参考第一张图的风格。这样整个系列的配色、线条、质感才能保持一致。

```bash
# 第 1 张：不带 --ref，建立视觉锚点
bun image-gen --promptfiles prompts/01-cover.md --image 01-cover.png --ar 3:4

# 第 2-4 张：带 --ref 保持一致
bun image-gen --promptfiles prompts/02-content.md --image 02-content.png --ar 3:4 --ref 01-cover.png
```

**Step 6：输出报告。**

### 实际效果

4 张黑板风格的图，风格高度一致：

- P1 封面 —— "你的 Claude Code 配好了吗？" 终端图标 + 齿轮 + 粉笔涂鸦
- P2 全景图 —— 8 种配置类型的层级关系，Top 3 高亮
- P3 Quick Start —— 3 个文件的代码示例卡片，黄/蓝/绿三色
- P4 结尾 —— 种子到大树的成长隐喻，"收藏备用"

### 输出的文件结构

```
xhs-images/claude-code-config/
├── analysis.md                      # 内容分析
├── outline-strategy-a.md            # 策略 A 大纲
├── outline-strategy-b.md            # 策略 B 大纲
├── outline-strategy-c.md            # 策略 C 大纲
├── outline.md                       # 最终选定的大纲
├── prompts/
│   ├── 01-cover-config-guide.md
│   ├── 02-content-config-map.md
│   ├── 03-content-quick-start.md
│   └── 04-ending-iterate.md
├── 01-cover-config-guide.png
├── 02-content-config-map.png
├── 03-content-quick-start.png
└── 04-ending-iterate.png
```

## Demo 3：文章插图（baoyu-article-illustrator）

**文章**：《用 Claude Code 做项目，为什么要学 Git》

这个 skill 做的事不一样 —— 不是把文章变成独立的图片系列，而是分析文章结构，**在合适的位置插入配图**。

### 它的工作流

**Step 1：分析内容** —— 读完文章，判断内容类型（Tutorial/Methodology），找出核心论点，然后 **定位哪些地方需要插图**。

我的文章有三个明显的视觉机会：
- "时光机 + 平行宇宙"这个核心比喻 —— 需要一张概念框架图
- "6 个基础命令"这个章节 —— 需要一张命令流程图
- "让 Claude 自动存档"这个工作流 —— 需要一张流程信息图

**Step 2-3：确认设置** —— 问两个核心问题：

- **Type** —— 插图类型。我选了 mixed（混合），因为文章既有概念比喻又有流程描述
- **Density** —— 插图密度。我选了 balanced（3-5 张）

这个 skill 也有 **Type × Style 二维设计**：

Type 控制信息结构：
- infographic —— 数据可视化
- scene —— 叙事场景
- flowchart —— 流程图
- comparison —— 对比图
- framework —— 概念框架
- timeline —— 时间线

Style 控制视觉美学（和封面图的维度不同）：
- notion / warm / minimal / blueprint / watercolor / elegant……

我用的是 blueprint 风格 —— 工程蓝图，精确线条，网格背景，90 度连接线。

**Step 4：生成大纲** —— 为每张插图写明位置、目的、视觉内容、文件名。

**Step 5：生成图片** —— 每张图单独一个 prompt 文件，按照 type 对应的模板写。比如 framework 类型有 STRUCTURE / NODES / RELATIONSHIPS 这些区块，flowchart 类型有 STEPS / CONNECTIONS 这些区块。

**Step 6：插入文章** —— 在对应位置插入 `![description](path)` 标记。

### Prompt 的结构差异

这是我觉得 baoyu-article-illustrator 最巧妙的地方 —— 不同类型的插图有不同的 prompt 模板。

**framework 类型的 prompt**：
```
STRUCTURE: dual-panel side-by-side

NODES:
- Left Panel: "时光机" — vertical timeline of commits
- Right Panel: "平行宇宙" — branching paths

RELATIONSHIPS: Left shows linear history, Right shows branching
```

**flowchart 类型的 prompt**：
```
STEPS:
1. "git init" - 开启存档
2. "git add + commit" - 存档
3. "git log" - 查看历史
...

CONNECTIONS: Main flow with branching to viewing and action commands
```

**infographic 类型的 prompt**：
```
ZONES:
- Zone 1: "存档" — commit checkpoint
- Zone 2: "Claude 修改" — AI edits
- Zone 3: "检查变化" — git diff
- Zone 4: "再次存档" — commit again

LABELS: 推荐工作流：每次 AI 修改前后都存档
```

这些模板确保了 prompt 有足够的结构信息，而不是模糊的"画一张好看的图"。

### 实际效果

3 张 blueprint 风格插图，工程感十足：

- 图 1 —— Git 核心概念：左边"时光机"（commit 时间线 + checkout 回退），右边"平行宇宙"（branch 分叉 + merge 合并）
- 图 2 —— 6 个命令流程图：init → add+commit 为主线，log/diff 分支右侧，checkout/branch 分支左侧
- 图 3 —— 推荐工作流：存档 → Claude 修改 → git diff 检查 → 再次存档，底部绿色"你的安全网"

### 输出的文件结构

```
illustrations/git-for-ai-users/
├── outline.md
├── prompts/
│   ├── 01-framework-git-concepts.md
│   ├── 02-flowchart-six-commands.md
│   └── 03-infographic-workflow.md
├── 01-framework-git-concepts.png
├── 02-flowchart-six-commands.png
└── 03-infographic-workflow.png
```

## 三个 Skill 的共同模式

跑完三个 demo，我发现 baoyu-skills 的设计有几个一致的模式：

**1. 偏好系统（EXTEND.md）**

每个 skill 都有 EXTEND.md，首次使用时通过问答生成，之后自动加载。项目级优先于用户级。这意味着你可以给不同项目设不同的默认风格 —— 技术博客用 blueprint，生活分享用 warm。

**2. 多维度组合**

不是给你一个"风格"下拉框选一下就完事。封面图有 5 个维度（type/palette/rendering/text/mood），小红书有 2 个维度（style × layout），文章插图也有 2 个维度（type × style）。维度之间自由组合，排列组合出来的可能性远超预设模板。

**3. Prompt 保存为文件**

每张图的 prompt 都保存在 `prompts/` 目录下。这样做的好处是：如果生成效果不满意，你可以直接编辑 prompt 文件重新生成，而不用从头走一遍流程。

**4. 输出目录独立**

每次运行都创建一个独立目录（`cover-image/plan-before-coding/`、`xhs-images/claude-code-config/`），不会互相覆盖。slug 冲突时自动加时间戳。

**5. 底层共享 baoyu-image-gen**

所有视觉 skill 的图片生成都委托给 `baoyu-image-gen`。这个 skill 封装了 Google / OpenAI / DashScope / Replicate 四个 provider 的调用逻辑，支持 prompt 文件、宽高比、画质、reference image 等参数。上层 skill 只需要写好 prompt，调用时传几个参数就行。

## 一些坑

- Google 免费层的图片生成配额是 0，必须付费
- `.env` 文件的路径要放对 —— 脚本从 `<cwd>/.baoyu-skills/.env` 或 `~/.baoyu-skills/.env` 读，放其他地方读不到
- 生成偶尔会失败（尤其是复杂 prompt），skill 内置了一次自动重试
- 中文文字在生成图片里的准确度取决于模型 —— Gemini 对中文的表现还不错，但偶尔会有错字

---

跑完三个 demo，我对 baoyu-skills 的理解从"一堆 Markdown 文件"变成了"一套设计得挺讲究的 AI 内容生产工具链"。

最让我意外的是小红书那个 skill —— 3 个策略变体、reference image chain 保持一致性、Style × Layout 二维组合 —— 复杂度远超我的预期，但交互流程跟着走就行，不用自己操心细节。

如果你也在用 Claude Code 写文章，想给内容配图但不想开 Figma，可以试试。

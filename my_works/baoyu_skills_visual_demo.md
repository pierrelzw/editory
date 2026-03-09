# baoyu-skills：用 Claude Code 给文章配图，从零开始

> 一套 Markdown 技能包，让 Claude Code 帮你生成封面图、小红书图文、文章插图。

---

前几天我在折腾 editory 项目的时候，发现仓库里有个 `baoyu-skills/` 目录，打开一看 —— 二十多个 skill，从生成封面图到做小红书图文到画漫画，全都有。

但光看文档看不出什么感觉。于是我挑了三个视觉类的 skill，拿自己的文章跑了一遍。

这篇文章把跑的过程记下来。如果你也想试，照着做就行。

## baoyu-skills 是什么

一句话：**给 Claude Code 用的第三方技能包，专注 AI 内容生成。**

作者是宝玉（JimLiu），把图片生成、内容发布、格式转换这些操作，封装成了 Claude Code 的 skill。

它不是一个独立的程序。**它是一堆 Markdown 文件 + 一些 TypeScript 脚本**，安装到你的项目或者 Claude Code 环境里以后，Claude 就会读这些文件，按照里面写好的步骤一步步执行。

换个方式理解：你在 CLAUDE.md 里写"每次改完代码跑一遍测试"，Claude 就会照做。baoyu-skills 做的事情本质一样 —— 只不过它写的指令远比你手写的复杂，覆盖了从"分析文章内容"到"组装图片生成 prompt"到"调用 API 生成图片"的完整流程。

技能分三大类：

- **内容生成类** —— 封面图、小红书图文、文章插图、幻灯片、漫画
- **AI 后端类** —— 图像生成引擎（调用 Google Gemini / OpenAI 的 API）
- **工具类** —— URL 转 Markdown、图片压缩、翻译

我这次跑的三个 demo 都是内容生成类，它们底层都调用 `baoyu-image-gen` 这个 AI 后端 skill 来生成图片。

## 从零开始：环境准备

假设你已经装好了 Claude Code，现在想跑第一个 baoyu-skills 的 demo。需要三步。

### 第一步：把 baoyu-skills 放进项目

baoyu-skills 是一个 Git 仓库。最简单的方式是 clone 到你的项目目录下：

```bash
cd your-project
git clone https://github.com/baoyu-io/baoyu-skills.git
```

Claude Code 启动后会扫描项目目录，发现 `baoyu-skills/skills/` 下面的 SKILL.md 文件，自动把它们注册为可用的 skill。

你也可以把它安装为 Claude Code 的 plugin —— 但直接放项目里是最简单的入门方式。

### 第二步：准备图像生成 API key

baoyu-skills 支持四个图像生成 provider：Google Gemini、OpenAI、阿里通义万象（DashScope）、Replicate。选一个就行，我用的是 Google Gemini。

去 [Google AI Studio](https://aistudio.google.com/) 申请 API key。**注意：免费层的图片生成配额是 0** —— 我一开始就被这个坑了，必须开通付费才能用。价格很低，一张图几分钱。

拿到 key 后，创建配置文件：

```bash
mkdir -p ~/.baoyu-skills
echo 'GOOGLE_API_KEY=your-key-here' > ~/.baoyu-skills/.env
```

脚本会从两个位置读 `.env`：`~/.baoyu-skills/.env`（用户级）和 `<项目目录>/.baoyu-skills/.env`（项目级）。放哪个都行。

### 第三步：确认 bun 可用

baoyu-skills 的脚本用 TypeScript 写，需要 bun 来运行。如果你没装 bun，用 `npx -y bun` 也行 —— 脚本会自动检测。

```bash
# 测试一下
npx -y bun baoyu-skills/skills/baoyu-image-gen/scripts/main.ts --help
```

看到 Usage 输出就说明环境 OK 了。

## 原理：skill 是怎么工作的

在进入 demo 之前，先说清一个概念 —— baoyu-skills 的"运行"跟你想的可能不一样。

**不是你敲一个命令，它就自己跑完了。** 整个过程是 Claude Code 在读 SKILL.md 里的指令，然后一步步执行。

拿 `baoyu-cover-image` 举例，它的 SKILL.md 里写了这些步骤：

1. 检查有没有 EXTEND.md（偏好配置文件），没有就问用户一堆问题然后创建一个
2. 读文章，分析内容
3. 根据分析结果自动选择风格维度，问用户确认
4. 把所有信息组装成一个图片生成 prompt，保存为文件
5. 调用 `baoyu-image-gen` 的脚本生成图片

Claude 读到"检查有没有 EXTEND.md"，就真的去跑 `test -f .baoyu-skills/baoyu-cover-image/EXTEND.md`。读到"问用户确认"，就真的弹出选择框问你。读到"调用脚本生成图片"，就真的执行 `npx -y bun image-gen/scripts/main.ts --promptfiles ... --image ...`。

**SKILL.md 就是一份详细的操作手册，Claude 是执行者。**

这也解释了为什么每个 skill 第一次使用时会问你偏好问题 —— 不是 skill 自己弹出来的，是 Claude 读到 SKILL.md 里"如果没有 EXTEND.md，必须先运行首次设置"这条指令后，执行了问答流程。

理解了这一点，后面看 demo 就清楚多了。

## 项目设计：一套用 Markdown 编程的技能包

跑 demo 之前，值得花点时间看看 baoyu-skills 这个项目本身是怎么设计的。理解了设计，后面看 demo 的时候会清楚得多 —— 每一步为什么这么做，不是随便写的。

### 两层架构：Markdown 指令层 + TypeScript 脚本层

baoyu-skills 里有 16 个 skill。但打开目录一看，你会发现它们分成两种：

**一种只有 Markdown，没有代码。** 比如 `baoyu-cover-image`、`baoyu-xhs-images`、`baoyu-article-illustrator`。它们的目录里只有 `SKILL.md` 和一堆 `references/` 文件。所有的"逻辑"都写在 Markdown 里 —— Claude 读了以后按步骤执行。

**另一种有 TypeScript 脚本。** 比如 `baoyu-image-gen`（图像生成引擎）、`baoyu-compress-image`（图片压缩）、`baoyu-url-to-markdown`（网页转 Markdown）。这些 skill 需要调外部 API 或者做文件处理，光靠 Markdown 指令搞不定，所以用 TypeScript 写了实际的脚本。

两层之间的关系：**上层的内容 skill 负责"想"（分析文章、选风格、组装 prompt），下层的工具 skill 负责"做"（调 API、处理文件）。**

拿封面图举例：`baoyu-cover-image`（纯 Markdown）负责读文章、分析内容、选择 metaphor + warm + hand-drawn 这些维度、把所有信息写成一个 prompt 文件。然后它调用 `baoyu-image-gen`（有脚本），由后者读 prompt 文件、调 Google Gemini API、拿到图片二进制数据、写入 PNG。

这个分工挺聪明的 —— Claude 擅长理解文章内容和组装 prompt，这些事不需要写代码；调 API 和处理二进制数据需要写代码，但这些逻辑是通用的，写一次所有 skill 都能复用。

### SKILL.md 的 500 行约束和 references/ 渐进式展开

CLAUDE.md 里有一条硬规则：**SKILL.md 必须控制在 500 行以内。**

这听起来像个小事，但它决定了整个项目的信息架构。

`baoyu-cover-image` 的 SKILL.md 是 240 行，`baoyu-article-illustrator` 是 162 行，`baoyu-xhs-images` 最复杂也只有 498 行。主文件只写核心流程 —— "第几步做什么、什么条件走什么分支"。

具体的细节全部放在 `references/` 目录下。Claude 不会一次性把所有 reference 文件都读进来，而是走到哪一步、需要什么信息、才去读对应的文件。

`baoyu-cover-image` 的 references/ 有 30 个文件，组织方式是这样的：

- `config/` —— 首次设置流程（`first-time-setup.md`）、偏好字段定义（`preferences-schema.md`）、水印配置（`watermark-guide.md`）
- `dimensions/` —— 字体、mood、text 这些维度的定义
- `palettes/` —— 9 种配色方案，每种一个文件（`warm.md`、`cool.md`、`dark.md`……），里面写了具体的 hex 色值和适用场景
- `renderings/` —— 6 种渲染风格的定义（`hand-drawn.md`、`flat-vector.md`……）
- `workflow/` —— 确认选项的交互流程、prompt 模板、reference image 使用规则

当 Claude 走到"选配色"这一步，它读 `auto-selection.md` 匹配到 warm，然后读 `palettes/warm.md` 拿到具体的色值（Orange #E8742A、Golden Yellow #F5C040……）。走到"生成 prompt"这一步，它读 `workflow/prompt-template.md` 拿到模板格式。

**SKILL.md 是目录，references/ 是正文。** Claude 按需翻页，不用一次性加载全部上下文。

`baoyu-xhs-images` 和 `baoyu-article-illustrator` 的 references/ 结构类似，但按各自的需要组织：

- xhs-images（20 个文件）—— `presets/` 下 10 种视觉风格（chalkboard、notion、cute……）、`elements/` 下排版和装饰规则、`workflows/` 下分析框架和 prompt 组装模板
- article-illustrator（27 个文件）—— `styles/` 下 20 种插图风格（blueprint、watercolor、sketch……）、prompt 构造规则、工作流定义

### 自动选择：内容信号 → 风格维度

每个视觉 skill 都有一套自动选择规则（`auto-selection.md`）。不是随机选，不是让用户从一长串列表里挑 —— 是根据文章内容的信号来匹配。

比如 baoyu-cover-image 的规则：

- 文章里有"个人故事、经验分享、成长"信号 → palette 匹配 warm
- 文章里有"哲学、反思、隐喻"信号 → type 匹配 metaphor
- 文章里有"数据、分析、对比"信号 → type 匹配 conceptual，palette 匹配 cool

Claude 先读文章，提取出信号，然后按规则匹配每个维度的值。匹配结果列出来让用户确认 —— 你可以接受自动选择，也可以手动覆盖任何一个维度。

这个设计在三个 skill 里是一致的：**先自动推荐，再人工确认。** 既不需要用户从零开始选（太累），也不完全交给 AI 决定（怕跑偏）。

### 没有代码的 skill 怎么"运行"

说到底，baoyu-skills 最有意思的设计决策是：**内容生成类 skill 没有一行代码。**

`baoyu-cover-image` 的目录里没有 `scripts/`。`baoyu-xhs-images` 也没有。`baoyu-article-illustrator` 也没有。

它们的全部"逻辑"就是 SKILL.md 里的自然语言指令 + references/ 里的参数定义。Claude 读了这些 Markdown 文件，用自己的语言理解能力来执行每一步：分析文章内容、提取信号、匹配维度、组装 prompt。

这也意味着 —— 如果你想改某个 skill 的行为，不用写代码，改 Markdown 就行。想加一种新的配色方案？在 `palettes/` 下加一个 `.md` 文件，在 `auto-selection.md` 里加一条匹配规则。想改 prompt 模板的格式？直接编辑 `prompt-template.md`。

**Markdown as code** —— 这不是比喻，是字面意思。

## Demo 1：封面图（baoyu-cover-image）

**文章**：《让 AI 先计划再写代码》

**怎么触发**：在 Claude Code 里说"用 baoyu-cover-image 给 my_works/plan_before_coding.md 生成封面图"就行。或者如果已经注册为 skill，直接 `/baoyu-cover-image my_works/plan_before_coding.md`。

这是最简单的一个 skill —— 给一篇文章生成一张封面图。

### 它执行了什么

**Step 0：加载偏好（EXTEND.md）**

Claude 先检查 `.baoyu-skills/baoyu-cover-image/EXTEND.md` 存不存在。第一次跑肯定没有，于是它按 SKILL.md 的指示，问了我 8 个问题：要不要水印？默认封面类型？默认配色？默认渲染风格？宽高比？输出目录？快速模式？保存到哪？

我大部分选了"自动选择"，宽高比选了 3:4（竖版，适合手机端），保存到项目级。Claude 把我的回答写成一个 YAML 配置文件，存为 `.baoyu-skills/baoyu-cover-image/EXTEND.md`。下次再用这个 skill 就不用再回答了。

**Step 1：分析内容**

Claude 读完文章，提取出：主题是"从混乱的 vibe coding 到有序的 plan 模式"，语气是"个人经验分享"，视觉隐喻是"从混乱到清晰的路径"。

**Step 2：确认选项**

这一步是 baoyu-cover-image 的核心设计 —— 用 **五个维度** 来定义一张封面图：

- **Type** —— hero / conceptual / typography / metaphor / scene / minimal
- **Palette** —— warm / elegant / cool / dark / earth / vivid / pastel / mono / retro
- **Rendering** —— flat-vector / hand-drawn / painterly / digital / pixel / chalk
- **Text** —— none / title-only / title-subtitle / text-rich
- **Mood** —— subtle / balanced / bold

每个维度都有自动选择规则，写在 `references/auto-selection.md` 里。比如文章里有"个人故事、经验分享"信号，palette 就自动匹配 warm；有"哲学、反思、成长"信号，type 就匹配 metaphor。

我的文章最终选的是：metaphor + warm + hand-drawn + title-only + balanced。Claude 列出来让我确认，我点了确认。

**Step 3：生成 prompt**

Claude 把分析结果和维度选择组装成一个 prompt 文件，保存为 `prompts/cover.md`。这个文件里有具体的配色 hex 值（Orange #E8742A、Golden Yellow #F5C040……）、构图描述（小人从 Chaos 走向 Clarity）、标题文字、渲染风格说明。

这也是 baoyu-skills 的一个设计原则 —— **prompt 不是临时传给 API 的字符串，而是保存下来的文件**。不满意可以直接改文件重跑，不用从头走一遍流程。

**Step 4：调用 baoyu-image-gen**

Claude 执行了这条命令：

```bash
npx -y bun baoyu-skills/skills/baoyu-image-gen/scripts/main.ts \
  --promptfiles my_works/plan_before_coding.assets/prompt-cover.md \
  --image my_works/plan_before_coding.assets/cover.png \
  --provider google --ar 3:4 --quality 2k
```

这就是实际调 API 的地方。`baoyu-image-gen` 是底层的图像生成 skill，它读 prompt 文件内容，调 Google Gemini API，拿到图片二进制数据，写入 PNG 文件。

**Step 5：输出报告**

告诉我生成了什么、放在哪、用了什么参数。

### 输出的文件结构

```
my_works/plan_before_coding.assets/
├── prompt-cover.md    # 图片生成 prompt（可编辑重跑）
└── cover.png          # 生成的封面图
```

### 实际效果

一张 3:4 竖版封面：手绘风格，一个小人从左下角的混乱代码（Chaos）沿着蜿蜒路径走向右侧的有序步骤（PLAN → DEFINE → STRUCTURE → IMPLEMENT → Clarity）。标题"让 AI 先计划再写代码"。

从开始到拿到图片，大概 2 分钟。

## Demo 2：小红书图文系列（baoyu-xhs-images）

**文章**：《Claude Code 配置，我一开始全做错了》

**怎么触发**："用 baoyu-xhs-images 给 my_works/claude_code_config_guide.md 生成小红书图文，风格用 chalkboard"。

这个 skill 复杂得多 —— 把一篇长文拆成 N 张小红书风格的信息图卡片。

### 它执行了什么

**Step 0：首次设置** —— 和封面图一样，先问偏好。这个 skill 的问题少一些：水印、默认风格、保存位置。

**Step 1：内容分析** —— Claude 读完文章，写了一份分析报告（保存为 `analysis.md`）：内容类型是"干货教程"，目标受众是"Claude Code 新手"，收藏潜力高，视觉机会在"配置类型概览图"和"代码示例卡片"。

**Step 2：确认理解** —— Claude 问我核心卖点是什么、受众风格偏好。这不是偏好设置，是针对这篇文章的具体确认 —— 确保它理解对了文章的重点。

**Step 3：生成 3 个大纲变体** —— 这一步是亮点。Claude 生成了三个完全不同的策略：

- **Strategy A：故事驱动** —— 从"我做错了"开始，个人经历线索，warm 风格，5 张
- **Strategy B：信息密集** —— 全景图 + 深入讲解，notion 风格，6 张
- **Strategy C：视觉优先** —— 极简设计，图表为主，minimal 风格，4 张

每个策略不光是大纲不同，连推荐的视觉风格都不同。三个策略分别保存为 `outline-strategy-a/b/c.md`。

这三个变体不是 Claude 自己发挥的 —— 是 SKILL.md 里要求的："Based on analysis + user context, create three distinct strategy variants"，并且规定了 A 是故事型、B 是信息密集型、C 是视觉优先型。

**Step 4：确认选择** —— 我选了 Strategy C（4 张），但风格从 minimal 换成了 chalkboard（黑板粉笔风）。

这里体现了 baoyu-xhs-images 的 **Style × Layout 二维设计**：

- **Style** 控制视觉美学 —— cute / fresh / warm / bold / minimal / retro / pop / notion / chalkboard / study-notes
- **Layout** 控制信息结构 —— sparse / balanced / dense / list / comparison / flow / mindmap / quadrant

两个维度自由组合。chalkboard + dense 就是"黑板上写满知识点"，chalkboard + sparse 就是"黑板上只写一句大字"。每张图可以用不同的 layout。

确认后 Claude 把最终大纲保存为 `outline.md`。

**Step 5：逐张生成** —— Claude 为每张图写一个 prompt 文件（`prompts/01-cover-config-guide.md` 等），然后调用 `baoyu-image-gen` 逐张生成。

这里有个关键细节：**reference image chain**。

第一张图（封面）不带 `--ref` 参数，作为"视觉锚点"。后面所有图片都带上 `--ref 01-cover.png`，让 Gemini 参考第一张图的风格。这样整个系列的配色、线条、质感才能保持一致。

```bash
# 第 1 张：不带 --ref，建立视觉锚点
bun image-gen --promptfiles prompts/01-cover.md --image 01-cover.png --ar 3:4

# 第 2-4 张：带 --ref 保持一致
bun image-gen --promptfiles prompts/02-content.md --image 02-content.png --ar 3:4 --ref 01-cover.png
```

这个设计也写在 SKILL.md 里，不是 Claude 自己想出来的。

**Step 6：输出报告。**

### 实际效果

4 张黑板风格的图，风格高度一致：

- P1 封面 —— "你的 Claude Code 配好了吗？" 终端图标 + 齿轮 + 粉笔涂鸦
- P2 全景图 —— 8 种配置类型的层级关系，Top 3 黄色高亮
- P3 Quick Start —— 3 个文件的代码示例卡片，黄/蓝/绿三色边框
- P4 结尾 —— 种子到大树的成长隐喻，"收藏备用"

### 输出的文件结构

```
my_works/claude_code_config_guide.assets/
├── xhs-analysis.md                          # 内容分析报告
├── xhs-outline-strategy-a.md                # 策略 A 大纲
├── xhs-outline-strategy-b.md                # 策略 B 大纲
├── xhs-outline-strategy-c.md                # 策略 C 大纲
├── xhs-outline.md                           # 最终选定的大纲
├── prompt-xhs-01-cover-config-guide.md      # 每张图的 prompt（可编辑重跑）
├── prompt-xhs-02-content-config-map.md
├── prompt-xhs-03-content-quick-start.md
├── prompt-xhs-04-ending-iterate.md
├── xhs-01-cover-config-guide.png
├── xhs-02-content-config-map.png
├── xhs-03-content-quick-start.png
└── xhs-04-ending-iterate.png
```

## Demo 3：文章插图（baoyu-article-illustrator）

**文章**：《用 Claude Code 做项目，为什么要学 Git》

**怎么触发**："用 baoyu-article-illustrator 给 my_works/git_for_ai_agent_users.md 配插图，风格用 blueprint"。

这个 skill 做的事不一样 —— 不是把文章变成独立的图片系列，而是分析文章结构，**在合适的位置插入配图**。

### 它执行了什么

**Step 1：分析内容** —— Claude 读完文章，判断内容类型（Tutorial），找出核心论点，然后 **定位哪些地方需要插图**。

我的文章有三个明显的视觉机会：

- "时光机 + 平行宇宙"这个核心比喻 —— 需要一张概念框架图
- "6 个基础命令"这个章节 —— 需要一张命令流程图
- "让 Claude 自动存档"这个工作流 —— 需要一张流程信息图

**Step 2-3：确认设置** —— 问两个核心问题：

- **Type** —— 插图类型。我选了 mixed（混合），让 Claude 根据每张图的位置自动选 framework / flowchart / infographic
- **Density** —— 插图密度。我选了 balanced（3-5 张）

这个 skill 也有 **Type × Style 二维设计**：

Type 控制信息结构：infographic / scene / flowchart / comparison / framework / timeline

Style 控制视觉美学：notion / warm / minimal / blueprint / watercolor / elegant……

我用的是 blueprint —— 工程蓝图风，精确线条，网格背景，90 度连接线。

**Step 4：生成大纲** —— 为每张插图写明：插在文章什么位置、为什么要插、画什么内容、文件名。保存为 `outline.md`。

**Step 5：生成图片** —— 每张图单独一个 prompt 文件，按照 type 对应的模板写。

这是 baoyu-article-illustrator 最巧妙的地方 —— **不同类型的插图有不同的 prompt 模板**。SKILL.md 引用的 `references/prompt-construction.md` 里定义了每种 type 的模板结构。

framework 类型用 STRUCTURE / NODES / RELATIONSHIPS：

```
STRUCTURE: dual-panel side-by-side

NODES:
- Left Panel: "时光机" — vertical timeline of commits
- Right Panel: "平行宇宙" — branching paths

RELATIONSHIPS: Left shows linear history, Right shows branching
```

flowchart 类型用 STEPS / CONNECTIONS：

```
STEPS:
1. "git init" - 开启存档
2. "git add + commit" - 存档
3. "git log" - 查看历史
...

CONNECTIONS: Main flow with branching to viewing and action commands
```

infographic 类型用 ZONES / LABELS：

```
ZONES:
- Zone 1: "存档" — commit checkpoint
- Zone 2: "Claude 修改" — AI edits
- Zone 3: "检查变化" — git diff
- Zone 4: "再次存档" — commit again

LABELS: 推荐工作流：每次 AI 修改前后都存档
```

这些模板确保了 prompt 有足够的结构信息，而不是模糊的"画一张好看的图"。Claude 按模板填入文章里的具体内容，生成出来的图就带有实际的标签、数据和关系。

**Step 6：插入文章** —— 在对应位置插入 `![description](path)` 标记。

### 实际效果

3 张 blueprint 风格插图，工程感十足：

- 图 1 —— Git 核心概念：左边"时光机"（commit 时间线 + checkout 回退），右边"平行宇宙"（branch 分叉 + merge 合并）
- 图 2 —— 6 个命令流程图：init → add+commit 为主线，log/diff 分支右侧，checkout/branch 分支左侧
- 图 3 —— 推荐工作流：存档 → Claude 修改 → git diff 检查 → 再次存档，底部绿色"你的安全网"

### 输出的文件结构

```
my_works/git_for_ai_agent_users.assets/
├── illustration-outline.md
├── prompt-illustration-01-framework-git-concepts.md
├── prompt-illustration-02-flowchart-six-commands.md
├── prompt-illustration-03-infographic-workflow.md
├── illustration-01-framework-git-concepts.png
├── illustration-02-flowchart-six-commands.png
└── illustration-03-infographic-workflow.png
```

## 跑完三个 demo 的体感

前面"项目设计"那节是我扒完源码以后总结的。跑 demo 的时候体感是另一回事 —— 有几个地方跟我预期不同。

**"智能"来自两层，缺一不可。** SKILL.md 定义的流程逻辑是死的（先分析再确认再生成），但每一步的具体内容 —— 分析出什么结论、prompt 怎么写 —— 完全依赖 Claude 的判断。同一篇文章换个 AI 来读这些 SKILL.md，大概率出来的东西很不一样。

**偏好系统比我想的实用。** 我在 editory 项目里把技术文章的默认风格设成了 blueprint，另一个项目可以设成 warm。项目级优先于用户级，不用每次都重新选。

**prompt 保存为文件这个设计很关键。** 小红书 4 张图里有一张我不满意，直接改了 prompt 文件让 Claude 重跑那一张，不用从头走整个流程。如果 prompt 是临时传给 API 的字符串，这种微调就做不到。

## 踩过的坑

- Google 免费层的图片生成配额是 0，必须开通付费
- `.env` 文件的路径要放对 —— 脚本从 `<cwd>/.baoyu-skills/.env` 或 `~/.baoyu-skills/.env` 读，放其他位置读不到
- 生成偶尔会失败（尤其是复杂 prompt），skill 内置了一次自动重试
- 中文文字在生成图片里偶尔会有错字，取决于模型 —— Gemini 对中文的表现还不错

## 想试的话，从哪开始

建议从 **baoyu-cover-image** 开始。原因：流程最短，一张图就能看到效果，没有大纲选择那些中间步骤。

```
1. 准备一篇你的 Markdown 文章
2. 在 Claude Code 里说：
   "用 baoyu-cover-image 给 path/to/article.md 生成封面图"
3. 回答几个偏好问题（只有第一次）
4. 确认风格维度
5. 等生成完成
```

跑通以后，再试 baoyu-xhs-images（多图系列）和 baoyu-article-illustrator（文章插图）。每个 skill 的 SKILL.md 里都有详细的使用说明和参数列表。

---

跑完三个 demo，我对 baoyu-skills 的理解从"一堆 Markdown 文件"变成了"一套设计得挺讲究的 AI 内容生产工具链"。

最让我意外的是 —— 这些 skill 本身不包含任何 AI 逻辑。它们只是写得很详细的操作手册，所有的"智能"都来自 Claude 读完手册后的执行。Markdown as code，字面意义上的。

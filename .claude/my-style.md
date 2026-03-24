# My Writing Style

This is a passive skill. It is automatically loaded whenever the user asks to write, polish, continue, rewrite, translate, or otherwise create/modify article content.

## Role & Reader

- I'm an indie developer building AI products. I write about tech, investing, parenting, and personal growth.
- My readers are peers — tech people, friends, people who share similar interests. Not academic audiences.
- My tone is like chatting with a friend, not writing a report.

## Style Principles

### 1. Open with a story or conversation

Almost every article starts with a personal anecdote, a conversation, or a concrete scene. Never open with a thesis statement.

Good:
> 前段时间，和一个小伙伴瞎聊天，聊到了买房。他问我：你买房了么？

> Vibe coding 听起来很美好："不用自己写代码，用语言编程，动动嘴（键盘）就行。"

Bad:
> 本文将探讨通货膨胀与房产投资的关系。

### 2. Short paragraphs, one idea each

A paragraph is typically 1-3 sentences. Use blank lines between paragraphs. Long blocks of text are forbidden.

### 3. First person, experience-driven

Write from "I" perspective. Personal experience drives the argument. Don't hide behind "we" or passive voice. When presenting a solution, share the journey — mention what you tried before and why it didn't work, not just the final answer.

包括教程类文章也优先用"我"叙事 —— 分享自己的经历和做法，让读者自然代入，而不是用"你"指导读者。"你"适合用在结尾反问、对话引用等互动场景。

Good:
> 我一直没想着要买房，也因此错过了北京的房价高峰。

> 一开始我采用的是软链接的方式，但是每次打开 AGENTS.md 看到首行是 CLAUDE.md，我就不太得劲。今天简单问了一下 AI，找到了一个干净的方案。

> 每个没关的 Tab，本质上是一个我对自己的微小承诺："我会回来处理的。"

Bad:
> 许多年轻人在面对高房价时选择了观望。

> 每个没关的 Tab，本质上是一个你对自己的微小承诺。

### 4. Strong opinions, clear stance

Don't hedge everything. Take a position. It's okay to be direct.

Good:
> 先别管 AI 有没有幻觉，我们自己先不要有幻觉。

> 我斗胆劝一劝：可以暂停一下想想。

Bad:
> 关于这个问题，不同的人可能有不同的看法，需要综合考虑各种因素。

### 5. Cite and quote to support, don't preach

Frequently cite books, podcasts, people, and data to back up points. Include the source naturally.

Good:
> 我想起了脱不花说的：只要相信孩子，她们其实能做得相当好。

> 根据 JP 摩根的统计，从 1980 年以来，市场上超过 40% 的股票都曾经遭遇毁灭性打击。

Bad:
> 众所周知，股市是有风险的。

### 6. Use analogies to make abstract ideas concrete

When introducing a concept, lead with concrete examples or scenarios first, then add an analogy. Never open with an abstract definition.

Good:
> 如果是代码，一般会写项目用什么语言、什么框架、测试怎么跑……可以理解为：你给一个新同事写的「入职须知」，只不过这个同事每天早上都会失忆。

Bad:
> 这是你给 Claude 的持久化指令。

Good:
> 就像一个厨子，做菜不咸不淡不辣不酸，每道菜都能吃，但你吃不出任何个人特色。

> 进去的是垃圾，出来的也是垃圾。

### 7. Reflective endings, not summaries

End with a question, a thought, or a scene. Never summarize with "in conclusion".

Good:
> 你有哪些抗通胀的方法？

> 和外甥们斗智斗勇的一天，终于结束。

Bad:
> 综上所述，写作风格的培养是一个长期的过程。

### 8. Tutorials: three principles

1. **Reader perspective first** — organize by the reader's mental path, not the author's knowledge structure. "How do I get it running" comes before "how does it work internally."
2. **Every step is verifiable** — after each step, the reader must be able to confirm success or failure. No command without expected output; no instruction without specifying where to run it.
3. **One place, one thing** — dependencies listed upfront, troubleshooting separated from instructions, background knowledge in its own section. Don't interleave explanations into action steps.

Specific: provide exact links, screenshots, and step-by-step details. Never say "search for X" when you can give the URL directly.

Good:
> 安装和使用参考[教程](https://portal.shadowsocks.au/...)

Bad:
> 搜索 "US address generator" 生成一个地址即可

### 9. Cut to the conclusion, skip the preamble

Don't write "guiding" sentences that add no information. Lead with the actionable takeaway. In tutorials, keep code examples minimal and generic — use universal commands readers already know (e.g. `ls`, `cat`) over framework-specific ones (e.g. `npm run lint`) unless the article is about that framework. Let the reader fill in their own details.

For tutorial/how-to articles, add a short TL;DR as a blockquote (`>`) right after the title. Keep it to one punchy sentence — no commas chaining multiple clauses, no enumerating sub-topics.

Good:
> \> 一份清单帮你搞清 Claude Code 到底有哪些配置

Bad:
> \> 一份清单，帮你搞清 Claude Code 到底有哪些配置、放在哪、怎么用、先配什么。

Good:
> \> 简单来说，把你希望所有 AI 都遵守的规则写在 AGENT.md 里，在 CLAUDE.md 里 @Agent.md，然后加上 Claude 专属的东西，就不用维护两套了。

Bad:
> 以下分 iPhone 和 macOS 两条路线，选择你手边的设备操作即可。

### 10. Remove unnecessary intensifiers

Don't use "千万", "非常", "极其" when the sentence works without them.

Good:
> 不要贪便宜买低价礼品卡！

Bad:
> 千万不要贪便宜买低价礼品卡！

### 11. Tutorials: verify facts from primary sources

When writing tutorials about tools/plugins/frameworks:
- Verify counts, defaults, commands, and API signatures from primary sources
  (priority: local source code → official docs → product UI → release notes)
- Never write specific counts from memory — count from source
- Flag known bugs/gotchas with workarounds
- Distinguish where commands run (terminal vs in-tool) when it matters

## Formatting Habits

- Use `**bold**` for key takeaways, not headings
- Use ` —— ` (em dash with spaces) for parenthetical remarks
- Use `……` for trailing off / lingering tone
- Use numbered sections (`1.` `2.` `3.`) with bold titles for structure, not heading levels
- Lists are short and punchy, not verbose
- Section headings: simple noun phrases preferred. Avoid "先看 X：Y 个 Z 一览" style — just "X 概览" or "X"
- **Prefer lists over tables.** Use `- item — description` format instead of markdown tables. Tables are harder to read on mobile and feel overly formal.

## Forbidden List

Expressions and patterns to never use:

**Formulaic openings:**
- "本文将介绍/探讨/分析……"
- "在当今社会/在这个时代……"
- "随着 XX 技术的快速发展……"

**Formulaic transitions:**
- "首先……其次……最后……" (three-part formula)
- "接下来让我们看看……"
- "值得注意的是……"
- "不可否认的是……"

**Formulaic endings:**
- "综上所述/总而言之/总之/说到底" as summary openers
- "让我们拭目以待"
- "希望本文对你有所帮助"

**Business jargon:**
- 深耕、赋能、闭环、抓手、落地、打通、对齐、拉通
- 底层逻辑、顶层设计、第一性原理（unless genuinely discussing physics）

**AI-smell expressions:**
- "作为一名 XX 领域的从业者/老兵"
- "不得不说/说实话/有一说一/事实上" as openers
- "非常重要的、极其关键的、至关重要的" (empty emphasis stacking)
- "然而，需要指出的是……"

**Structural crutches:**
- "一方面……另一方面……" followed by "因此"
- Excessive use of "不是……而是……" patterns
- Parallel sentence structures repeated 3+ times

**Filler and fluff:**
- "有，但风险不同：" — don't editorialize before a list, just give the list
- "本教程只给一条最简单的操作路线，从头到尾跟着做就行" — skip meta-descriptions of the article itself
- "分享出来" / "分享给大家" — the act of publishing already implies sharing
- Unnecessary context the reader doesn't need (e.g. "一个手机号最多绑定 2 个 Apple ID" when user only needs one)
- Don't over-explain peripheral topics that are already covered in a list — if you listed it, the reader got it
- "不讲太多道理，直接给你能用的" — meta-descriptions of the article's own approach; just do it, don't announce it

## Behavior Rules

When generating or editing article content for the user:

1. **Fact-check before commit:** If `/fact-check` is available in the current project, run `/fact-check <file>` after finishing writing/editing.
   This launches an independent subagent to verify all factual claims.
   Fix any errors found, re-check until passed. Only then proceed to auto-commit.
   If `/fact-check` is not available, skip this step and proceed directly to auto-commit.
2. **Auto-commit after writing:** After writing or editing an article, immediately run:
   - For new content (draft/translate): `git add <file> && git commit -m "[ai-draft] <filename>"`
   - For polishing existing content: First `git add <file> && git commit -m "[user-draft] <filename>"` to save the user's original, then after polishing `git add <file> && git commit -m "[ai-polish] <filename>"`
3. **Always inform the user** that the version has been saved and they can freely edit.
4. **After the user finishes editing**, remind them: "Run `/iterate-style <file>` to update the writing style based on your edits."

## Reference Samples

- `my_works/samples/defend_inflation_without_buying_house.md` — long-form argumentative, data-driven
- `my_works/samples/kids_have_it_tough.md` — parenting essay, quote-heavy, storytelling
- `my_works/samples/try_take_care_my_nephews.md` — personal narrative, detailed scenes
- `my_works/samples/illusion_of_AI_or_us.md` — short opinion piece, direct and punchy
- `my_works/samples/language_bind_thinking.md` — reflective essay, multi-source citations
- `my_works/samples/autohighlight_online.md` — product announcement, casual tone

<!-- Iteration log is stored separately in .claude/my-style-log.md to save tokens -->

# 一个人开发，怎么模拟团队 Code Review

> 用 Claude Code 的 Agent Teams，让多个 AI 从不同角度审查你的代码，弥补独立开发者没有 reviewer 的缺憾。

---

独立开发最大的问题之一：没有人帮你 review 代码。

不是说 AI 不能 review —— Claude Code 的 subagent 做 code review 已经很好用了。但你有没有发现一个问题：**单个 reviewer，不管多强，看问题的角度是固定的**。

在团队里做过 code review 的人应该有感觉：同一个 PR，安全工程师看到的问题和前端工程师看到的完全不一样。有时候最有价值的 comment 来自一个"外行"角度 —— 比如产品经理问一句"这个错误提示用户能看懂吗？"

Agent Teams 能做的，就是帮你模拟这个过程。

## 和普通 AI Review 的区别

**普通做法**：你让 Claude review 一段代码，它给你一份清单 —— 安全问题 3 个、性能问题 2 个、风格问题 5 个。像一份体检报告，面面俱到但平铺直叙。

**Agent Teams 做法**：三个 reviewer 各自从自己的角度看完代码，然后开始互相质疑。安全 reviewer 说"这里必须加输入校验"，性能 reviewer 说"加校验会拖慢热路径，能不能放到别的层做？"，测试 reviewer 说"与其在这里吵，不如写个 benchmark 测一下。"

区别在于：单 agent 给你的是**一个人的意见**，Agent Teams 给你的是**一场讨论的结论**。讨论的过程会暴露出单一视角看不到的 tradeoff。

## 实操：三人 Review 团队

我最近在一个项目里加了身份验证模块，用 Agent Teams 做了一次 review。以下是 prompt：

```
我刚完成了身份验证模块的开发（src/auth/ 目录）。
创建一个 Agent Team 来 review，spawn 3 个 teammate：

1. 安全 reviewer：专注认证逻辑、token 处理、输入校验、
   常见漏洞（OWASP Top 10）

2. 工程质量 reviewer：专注代码结构、错误处理、可读性、
   是否符合项目既有风格

3. 测试 reviewer：专注测试覆盖率、edge cases、是否有不可测试的代码、
   mock 策略是否合理

要求：
- 先各自独立 review
- 然后互相质疑对方的发现——哪些是真问题，哪些是过度设计
- 对有分歧的点辩论出结论
- 最终给我一份合并后的 review 报告，标注优先级
```

### 辩论过程

安全 reviewer 首先发现 JWT token 没有设置过期时间。工程质量 reviewer 认同这是问题，但补充说"同时 refresh token 的轮换逻辑也没有实现，光加过期时间只解决一半问题。"

测试 reviewer 提了一个不同角度："auth 模块对数据库有硬依赖，没有做接口抽象，导致单元测试必须连真实数据库。建议抽一个 repository 接口出来。"

工程质量 reviewer 反对："为了测试好写而多加一层抽象，是过度设计。现在只有一种数据库实现，加接口只增加复杂度。"

测试 reviewer 坚持："不是为了换数据库，是为了能用 mock 跑测试。现在的写法，CI 每次跑测试都要启动数据库，慢且不稳定。"

安全 reviewer 加入讨论，支持测试 reviewer："而且抽出接口后，安全审计也更容易 —— 所有数据访问都经过一个明确的入口。"

最终结论：2:1 同意抽出 repository 接口，但限定只做 auth 相关的，不过度推广到整个项目。

**这种结论，单个 agent 给不出来。** 因为它不会自己跟自己辩论。

## Prompt 模板

针对不同类型的代码，reviewer 组合可以不一样：

**后端 API**
```
Spawn 3 teammates：安全 reviewer、性能 reviewer、API 设计 reviewer。
重点关注：认证授权、N+1 查询、接口一致性。
```

**前端组件**
```
Spawn 3 teammates：可访问性(a11y) reviewer、性能 reviewer、UX reviewer。
重点关注：键盘导航、渲染性能、用户体验一致性。
```

**基础设施/DevOps**
```
Spawn 3 teammates：安全 reviewer、可靠性 reviewer、成本 reviewer。
重点关注：权限最小化、故障恢复、资源浪费。
```

你也可以根据自己的项目调整角色。核心原则是：**让不同角色之间有天然的 tension**（安全 vs 效率、抽象 vs 简单、覆盖率 vs 开发速度），这样辩论才有价值。

## 使用建议

**不是每个 PR 都需要 Agent Teams。**

我的做法是：日常小改动用普通 subagent review（快、便宜、够用）。遇到以下情况才拉 Agent Teams：

- **新模块/新功能** — 架构决策多，容易有盲区
- **涉及安全的改动** — 认证、支付、权限，值得多一双眼睛
- **重构** — 改动范围大，需要从多个角度评估影响
- **自己拿不准的代码** — 写完了总觉得哪里不对，但说不出来

**控制团队大小在 3 个。** 我试过 5 个 reviewer，协调开销太大，讨论容易跑偏。3 个刚好 —— 有分歧时 2:1 能出结论，视角足够多元但不至于混乱。

**注意成本。** Agent Teams 目前需要 Opus 模型，token 消耗不低。所以更要把它用在刀刃上 —— 日常小改动用普通 subagent review（可以用 sonnet），关键改动才拉 Agent Teams。

## 回到那个问题

独立开发最大的缺憾是没有人帮你 review。但仔细想想，review 的本质是什么？不是找 bug —— linter 和测试能找到大部分 bug。review 的真正价值是**多个视角的碰撞** —— 安全的人看到安全问题，性能的人看到性能问题，然后他们争论出一个平衡方案。

Agent Teams 不能完全替代真人 reviewer。但对独立开发者来说，能在关键节点召集一个"AI 评审会"，总比一个人闷头写好。

---

下一步可以试试：跑完 review 之后，把高优先级的改进项直接让 Claude 帮你改。Agent Teams 负责"讨论该怎么做"，普通 Claude 负责"动手做"。分工明确，效率最高。

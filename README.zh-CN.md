# Editory

基于 AI 的内容分发技能，适用于 Claude Code。Markdown 一次编写，多平台发布。

## Editory 是什么？

Editory 是一个 Claude Code 技能，让你可以直接在终端中将 Markdown 文章发布到多个平台。写完文章后，只需告诉 Claude：

```
/publish article.md --platforms mowen,xiaohongshu
```

Claude 会读取文章、进行 AI 审阅与优化、展示预览，然后自动发布到你选择的平台。

**这不是一个独立的命令行工具。** 它是一组 Markdown 文件，用来教会 Claude Code 如何发布内容。Claude 本身就是 AI 引擎——无需额外依赖。

## 支持的平台

| 平台 | 发布方式 | 状态 |
|---|---|---|
| 墨问 (mowen.cn) | 通过 `mowen-mcp-server` 直接 MCP 调用 | 可用 |
| 小红书 | 通过 Chrome DevTools MCP 浏览器自动化 | 可用 |
| 微信公众号 | 通过 Chrome DevTools MCP 浏览器自动化 | 可用 |
| Twitter/X | 通过 Chrome DevTools MCP 浏览器自动化 | 可用 |

## 工作流程

1. **读取** — Claude 读取你的 Markdown 文件并解析 frontmatter 元数据
2. **审阅** — AI 审阅格式、内容质量，并提出改进建议（可选）
3. **适配** — 生成各平台专属版本（小红书加表情、Twitter 拆分为推文串等）
4. **预览** — 展示每个平台的最终版本供你确认
5. **发布** — 通过 MCP 服务器或浏览器自动化自动发布
6. **报告** — 展示每个平台的发布状态、链接和截图

## 安装与配置

### 1. 安装到你的项目

将 `skills/`、`platforms/` 和 `templates/` 目录复制到你的项目中：

```bash
git clone https://github.com/user/editory.git
cp -r editory/skills editory/platforms editory/templates your-project/
cp editory/CLAUDE.md your-project/
```

或者直接在 Claude Code 配置中将 Editory 添加为技能目录。

### 2. 配置 MCP 服务器

墨问（直接 MCP，基于 Streamable HTTP 协议，无需本地环境依赖）：

```bash
claude mcp add-json mowen '{"type":"streamable-http","url":"https://open.mowen.cn/api/open/mcp/v1/note?key=YOUR_API_KEY"}'
```

API Key 获取方式：在墨问微信小程序中开通会员，然后前往开发者中心获取。

小红书、微信公众号和 Twitter（浏览器自动化）：
```bash
# 确保 Claude Code 中已配置 chrome-devtools MCP
# 启动 Chrome 并开启远程调试：
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=~/.editory/chrome-profile
```

### 3. 登录各平台

首次使用时，在 Chrome 实例中登录各平台：
- 打开各平台网站
- 使用你的账号登录
- 登录状态保存在 `~/.editory/chrome-profile/` 中

### 4. 配置文件（可选）

复制并自定义配置文件：

```bash
cp config.example.toml ~/.config/editory/config.toml
# 编辑设置你的默认选项
```

## 使用方法

### 基本用法
```
/publish article.md
```
使用文章 frontmatter 或配置文件中的默认平台。

### 指定平台
```
/publish article.md --platforms mowen,xiaohongshu,twitter
```

### 跳过 AI 审阅
```
/publish article.md --skip-review
```

### 跳过封面图生成
```
/publish article.md --skip-cover
```

### 文章 frontmatter

```yaml
---
title: "我的文章标题"
tags: [python, 编程, 技巧]
platforms: [mowen, xiaohongshu]
cover: ./cover.png
type: article  # 或 "short_post"（短文/笔记）
mowen_note_id: abc123        # 首次发布后自动填入（后续更新而非重复创建）
mowen_cover_uuid: xyz-TMP    # 封面上传后自动填入（更新时复用）
---

在这里写你的文章内容...
```

## 项目结构

```
editory/
├── CLAUDE.md                  # Claude 项目上下文
├── .claude/commands/
│   ├── publish.md             # /publish 技能定义
│   ├── post-to-wechat.md     # /post-to-wechat 技能
│   └── iterate-style.md      # /iterate-style 技能
├── scripts/
│   ├── md2mowen.py            # Markdown → 墨问 JSON 转换器
│   └── test_md2mowen.py       # 转换器测试
├── platforms/
│   ├── mowen.md               # 墨问：MCP 工具 + 浏览器备选
│   ├── xiaohongshu.md         # 小红书：浏览器自动化
│   ├── wechat.md              # 微信公众号发布指南
│   └── twitter.md             # Twitter/X 发布指南
├── templates/
│   ├── review-checklist.md    # AI 内容审阅清单
│   └── platform-styles.md    # 各平台内容风格指南
├── my_works/                   # 用户文章和草稿
├── config.example.toml        # 示例配置文件
└── README.md                  # 英文文档
```

## 与传统工具的区别

| | 传统 CLI 工具 | Editory（Claude Code 技能） |
|---|---|---|
| 代码量 | ~30+ Python 文件 | ~8 个 Markdown 文件 |
| 依赖项 | 12+ Python 包 | 0（使用 Claude Code 内置能力） |
| AI 能力 | 无（纯自动化） | 原生支持（内容审阅、优化、适配） |
| 安装方式 | pip install | 复制技能文件 |
| 维护成本 | 代码 + 测试 | 更新平台文档 |
| 灵活性 | 固定流程 | 对话式——随时调整 |

## 许可证

MIT

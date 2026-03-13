# 用 1Password CLI 管好你的 API Key

> 一个命令搞定 key 存哪、用在哪、去哪续。

---

前几天 GitHub 给我发了封邮件：你的 Personal Access Token 过期了。

我点进去一看，token 名字叫 `my-token`。

用在哪个项目？不记得了。配在哪个配置文件里？不知道。改了之后还要去哪里同步？完全没有头绪。

更痛苦的是另一种情况：我知道某个 key 需要更新，但忘了当初是在哪个网站的哪个页面创建的。Azure？OpenAI？Anthropic？每个平台的 key 管理页面都藏在不同的角落里，每次都要重新翻一遍。

这个问题的本质是：**key 本身存了，但元数据丢了** —— 在哪创建的、用在哪里、什么时候过期，这些信息散落在你的记忆里，而记忆是不可靠的。

我现在的方案是用 1Password CLI。

## 为什么是 1Password CLI

你可能已经在用 1Password 存密码了。它的 CLI 工具 `op` 能做三件事：

- **存 key + 元数据** —— 每个 key 不只是一个值，还能带上管理页面 URL、用在哪个项目、过期时间
- **环境变量不落盘** —— `.env` 文件里只写引用（`op://...`），真实值运行时注入
- **Shell 插件免配置** —— `gh`、`aws` 这些 CLI 直接用 Touch ID 认证，不用再设环境变量

## 安装和连接

```bash
brew install --cask 1password-cli
op --version
```

然后打开 1Password 桌面 App：**Settings → Developer → 勾选 "Integrate with 1Password CLI"**。

开了这个之后，所有 `op` 命令都走 Touch ID 认证，不用每次手动 `eval $(op signin)`。

## 1. 存 Key：带上你未来需要的信息

核心思路：**创建 key 的时候，多花 30 秒把元数据一起存进去**。未来过期、轮换、排查的时候，这 30 秒能省你 30 分钟。

```bash
op item create \
  --category "API Credential" \
  --title "github-editory-mcp" \
  --vault "Development" \
  --url "https://github.com/settings/tokens" \
  --tags "claude-code,editory" \
  credential="ghp_xxxx..." \
  "Metadata.used_in[text]=~/.claude.json MCP config" \
  "Metadata.project[text]=editory" \
  "Metadata.expires[text]=2026-06-01"
```

几个要点：

- `--url` 存管理页面地址 —— 过期了直接点过去续
- `Metadata.used_in` 记录这个 key 配在哪个文件里 —— 更新后知道去哪里同步
- `--tags` 按项目打标签 —— 方便按项目筛选
- `credential` 是 API Credential 类别的内置字段，存 key 本身的值

**命名规范也很重要。** token 名字要能自解释：

- `github-editory-mcp` —— 平台-项目-用途
- `azure-speech-mandarin-app` —— 平台-服务-项目
- `anthropic-claude-code-sub` —— 平台-产品-用途

GitHub 那边创建 token 的时候就用这个名字，1Password 里也用同一个名字。这样不管从哪边看到这个名字，都能对上。

## 2. 查 Key：过期了不慌

```bash
# 列出所有 API 凭证
op item list --categories "API Credential" --vault Development

# 查某个 key 的详情
op item get "github-editory-mcp"

# 按项目找：editory 用了哪些 key？
op item list --tags editory

# 只看某个字段
op item get "github-editory-mcp" --fields "label=used_in"
```

以后收到 "token 过期" 的邮件，一条命令就能看到：管理页面在哪、配在哪个文件里、属于哪个项目。

## 3. 用 Key：不落盘

传统做法是把 key 写在 `.env` 文件里。问题是：明文存在磁盘上，容易泄露，多个项目还要复制粘贴。

1Password CLI 的方案是**引用替代明文**。

**方式一：`op run` + `.env` 文件**

`.env` 文件里只存引用：

```bash
# .env —— 没有任何真实 key
GITHUB_TOKEN="op://Development/github-editory-mcp/credential"
ANTHROPIC_API_KEY="op://Development/anthropic-claude-code/credential"
OPENAI_API_KEY="op://Development/openai-api/credential"
```

运行时用 `op run` 注入：

```bash
op run --env-file=.env -- node server.js
op run --env-file=.env -- python main.py
```

`op run` 会把所有 `op://` 引用替换成真实值，而且默认会在 stdout 里遮蔽这些值，防止日志泄露。

**方式二：`op read` 读单个值**

```bash
# 读一个 key
op read "op://Development/openai-api/credential"

# 赋给变量
API_KEY=$(op read "op://Development/openai-api/credential")
```

**方式三：`op inject` 注入配置文件模板**

如果你的配置文件不是 `.env` 格式：

```yaml
# config.template.yml
database:
  password: {{ op://Development/postgres-prod/password }}
api:
  key: {{ op://Development/openai-api/credential }}
```

```bash
op inject -i config.template.yml -o config.yml
```

注意语法区别：`.env` 里用 `op://...`，模板文件里用 `{{ op://... }}`。

## 4. Shell 插件：最省心的方案

如果你常用 `gh`（GitHub CLI）、`aws` 这些工具，Shell 插件能让你完全不用管 token。

```bash
op plugin init gh
```

按提示选择 1Password 里哪个 item 存着你的 GitHub token，设置完成后，以后直接用 `gh` 命令就行 —— 触发 Touch ID，自动认证，不需要 `GH_TOKEN` 环境变量。

支持的插件很多：`aws`、`gh`、`stripe`、`openai`、`flyctl`、`vercel` 等等。

## 5. 和 Claude Code 配合

Claude Code 的 MCP 配置经常需要各种 token。可以这样：

在 `~/.claude.json` 的 MCP 配置里，环境变量用 `op://` 引用：

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "op://Development/github-mcp/credential"
      }
    }
  }
}
```

启动 Claude Code 时套一层 `op run`：

```bash
op run -- claude
```

所有 `op://` 引用自动替换。key 轮换了只需要在 1Password 里更新，不用改任何配置文件。

## 我的工作流

现在每次创建新 key，我会做这几件事：

1. 在平台上创建 key，**命名用 `平台-项目-用途` 格式**
2. 立刻在 1Password 里存一条 API Credential，**带上管理页面 URL 和 `used_in`**
3. 配置文件里只写 `op://` 引用，**不存明文**
4. 能用 Shell 插件的就用插件，**连引用都不用写**

收到过期通知的时候：

1. `op item get <name>` —— 看管理页面在哪、用在哪
2. 点 URL 去续或重新生成
3. 在 1Password App 里更新 key 值（命令行 `op item edit` 也行，但 key 会留在 shell history 里，不推荐）
4. 不用改任何配置文件，`op://` 引用自动生效

---

其实方案本身不复杂，关键是**养成习惯**：创建 key 的时候多花 30 秒存元数据。

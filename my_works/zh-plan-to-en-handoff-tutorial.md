# 用中文指挥 Claude Code 写代码？先让本地模型翻译一道

> 配一个 hook 脚本，你用中文说，Claude 自动收到英文版——不用改习惯，效果更好。

---

我平时用 Claude Code 写代码，指令习惯用中文。但我发现一个问题：**同样的意思，用英文下指令，Claude 的执行质量明显更高。**

这不难理解——Claude 的训练数据以英文为主，英文指令的语义更精确，歧义更少。

但让我每次都手动翻译成英文？太累了。

于是我搞了一个自动化方案：**在你按下回车的那一刻，hook 脚本检测到中文，自动调用本地 Ollama 翻译成英文，注入给 Claude。** 你继续用中文说话，Claude 看到的是英文版本。

## 架构一句话

```
你输入中文 → UserPromptSubmit hook → 本地 Ollama 翻译 → 英文作为 additionalContext 注入
```

Claude 同时看到你的中文原文和英文翻译，用英文版本作为主要指令来执行。

## 前置条件

**1. 安装 Ollama**

```bash
brew install ollama
ollama serve
```

**2. 拉一个翻译模型**

我测过三个模型：

- `gemma3:4b` — 14.5s，速度最快
- `qwen2.5:7b-instruct` — 17.7s，中英翻译质量最好，推荐
- `qwen2.5:14b-instruct` — 25.3s，质量和 7b 差不多，慢 43%

```bash
ollama pull qwen2.5:7b-instruct
```

**3. 确认 jq 可用**

```bash
brew install jq  # macOS
```

## Step 1：创建 hook 脚本

脚本放在项目里方便版本管理。以我的 editory 项目为例：

```bash
mkdir -p templates/claude-code-hooks
```

创建 `templates/claude-code-hooks/translate-prompt.sh`：

```bash
#!/usr/bin/env bash
# translate-prompt.sh — UserPromptSubmit hook for Claude Code
# Detects Chinese in user prompts and auto-translates to English via local Ollama.

set -euo pipefail

# --- Config ---
OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"
OLLAMA_MODEL="${TRANSLATE_MODEL:-qwen2.5:7b-instruct}"
OLLAMA_TIMEOUT="${OLLAMA_TIMEOUT:-30}"

# Skip translation for projects matching these patterns (comma-separated)
SKIP_PROJECTS="${TRANSLATE_SKIP_PROJECTS:-}"

# --- Read stdin ---
INPUT=$(cat)
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty')
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')

if [[ -z "$PROMPT" ]]; then
  exit 0
fi

# --- Skip list check ---
if [[ -n "$SKIP_PROJECTS" ]]; then
  IFS=',' read -ra SKIP_LIST <<< "$SKIP_PROJECTS"
  for pattern in "${SKIP_LIST[@]}"; do
    pattern=$(echo "$pattern" | xargs)
    if [[ "$CWD" == *"$pattern"* ]]; then
      exit 0
    fi
  done
fi

# --- Chinese detection (macOS compatible, requires UTF-8 binmode) ---
if ! echo "$PROMPT" | perl -e 'binmode STDIN,":utf8"; local $/; $t=<STDIN>; exit($t=~/[\x{4e00}-\x{9fff}]/?0:1)'; then
  exit 0
fi

# --- Clear proxy env vars (Ollama is local) ---
unset http_proxy https_proxy all_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY 2>/dev/null || true

# --- Call Ollama ---
SYSTEM_PROMPT="You are a translator. Translate the following Chinese text to English. The text is a programming instruction for an AI coding assistant. Preserve all code identifiers, file paths, command names, and technical terms exactly as-is. Output ONLY the English translation, nothing else."

PAYLOAD=$(jq -n \
  --arg model "$OLLAMA_MODEL" \
  --arg prompt "$PROMPT" \
  --arg system "$SYSTEM_PROMPT" \
  '{model: $model, prompt: $prompt, system: $system, stream: false}')

RESPONSE=$(curl -s --max-time "$OLLAMA_TIMEOUT" \
  "${OLLAMA_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" 2>/dev/null) || {
  exit 0  # Ollama unreachable → graceful degradation
}

TRANSLATION=$(echo "$RESPONSE" | jq -r '.response // empty' 2>/dev/null)

if [[ -z "$TRANSLATION" ]]; then
  exit 0
fi

# --- Output ---
jq -n --arg translation "$TRANSLATION" '{
  "additionalContext": ("[Auto-translated from Chinese]\n" + $translation + "\n\n[Original Chinese prompt is shown above. Use the English translation as your primary instruction.]")
}'
```

给脚本加执行权限：

```bash
chmod +x templates/claude-code-hooks/translate-prompt.sh
```

## Step 2：配置 hook

在项目根目录创建 `.claude/settings.json`：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash templates/claude-code-hooks/translate-prompt.sh"
          }
        ]
      }
    ]
  }
}
```

重启 Claude Code，hook 就生效了。

## Step 3：测试

**测试 1：中文指令触发翻译**

在 Claude Code 里输入：

```
帮我看看 CLAUDE.md 有什么问题
```

按 `Ctrl+R` 开启 verbose 模式，你会看到 hook 输出了 `additionalContext`，里面是英文翻译。

**测试 2：英文指令不触发**

输入：

```
show me the file structure
```

hook 检测到没有中文字符，直接跳过，不调用 Ollama。

**测试 3：短文本也翻译**

输入：

```
好的
```

不设最小长度阈值。短文本翻译很快（<2s），不值得加复杂度。

**测试 4：Ollama 不可用时优雅降级**

关掉 Ollama（`killall ollama`），输入中文，确认 Claude 正常工作，不报错，不阻塞。

## Step 4：推广到全局

测试通过后，把 hook 配到用户级别，所有项目都能用。

**1. 复制脚本**

```bash
cp templates/claude-code-hooks/translate-prompt.sh ~/.claude/hooks/translate-prompt.sh
```

**2. 编辑 `~/.claude/settings.json`**

在 `hooks` 字段里加：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/translate-prompt.sh"
          }
        ]
      }
    ]
  }
}
```

**3. 设置排除列表**

中文写作项目不应该被翻译。在 `~/.claude/settings.json` 的环境变量里加：

```json
{
  "env": {
    "TRANSLATE_SKIP_PROJECTS": "editory,my-blog,writing"
  }
}
```

或者直接 export：

```bash
export TRANSLATE_SKIP_PROJECTS="editory,my-blog,writing"
```

**4. 删除项目级测试配置**

```bash
rm .claude/settings.json
```

## 配合 CLAUDE.md 使用

在你的编程项目的 `CLAUDE.md` 里加上这段，告诉 Claude 如何处理翻译后的指令：

```markdown
## Language Rules
When my prompt includes an `[Auto-translated from Chinese]` section:
1. Use the English translation as the primary instruction for reasoning and execution.
2. Use English for code, comments, and commit messages.
3. Respond to me in Chinese with a brief summary of what was done.
```

这样 Claude 用英文理解和执行，用中文回复你——两全其美。

## 调试技巧

- **看 hook 输出** — `Ctrl+R` 开 verbose 模式，hook 的 stdout 会显示在日志里
- **单独测试脚本** — `echo '{"prompt":"帮我看看代码","cwd":"/tmp"}' | bash translate-prompt.sh`
- **切换模型** — 设置环境变量 `export TRANSLATE_MODEL=gemma3:4b`（要速度）或 `qwen2.5:7b-instruct`（要质量）
- **调超时** — `export OLLAMA_TIMEOUT=60`（网络慢或模型大时）

## 为什么不直接用 MCP Server？

我之前也搭了一个 [translate-ollama MCP server](https://github.com/pierrelzw/editory)，Claude 可以主动调用它翻译。但那是"出口翻译"——Claude 收到中文指令，决定要不要调翻译工具。

hook 方案是"入口翻译"——**在 Claude 看到你的指令之前，翻译已经完成了。** Claude 从一开始就在英文语境里思考，效果更好。

两个方案不冲突，可以并存。hook 处理日常指令的自动翻译，MCP server 处理你主动要求翻译文件或文本的场景。

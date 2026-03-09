# Claude Code 调用本地模型翻译 — 完成报告

## 方案架构

```
Claude Code ──MCP协议──> translate-ollama.py ──HTTP──> Ollama (localhost:11434)
                              │
                         两个工具：
                         ├─ translate      (翻译文字)
                         └─ translate_file (翻译文件)
```

## 模型对比结果

| 模型 | 大小 | 耗时 | 翻译质量 | 备注 |
|------|------|------|---------|------|
| `gemma3:4b` | 3.3GB | **14.5s** | 良好 | 当前默认模型，速度最快 |
| `qwen2.5:7b-instruct` | 4.7GB | 17.7s | 优秀 | 中英双语最佳，推荐 |
| `qwen2.5:14b-instruct` | 9GB | 25.3s | 优秀 | 质量与 7b 相近，慢 43% |

## 文件清单

| 文件 | 作用 |
|------|------|
| `~/.claude/mcp-servers/translate-ollama.py` | MCP Server 主程序 |
| `~/.claude/mcp-servers/.venv/` | Python 虚拟环境（含 mcp、httpx） |
| `~/.claude.json` → `mcpServers.translate-ollama` | MCP 注册配置 |

## 验证结果

| 测试 | 状态 | 说明 |
|------|------|------|
| 中→英文字翻译 | 通过 | "编程不再是少数人的专利" → 准确 |
| 英→中文字翻译 | 通过 | Alan Kay 名言翻译流畅 |
| 指定模型翻译 | 通过 | `model: qwen2.5:7b-instruct` 可切换 |
| 文件翻译 | 通过 | plan_before_coding.md 完整翻译，按段落分块处理 |

## 使用方式

在 Claude Code 中直接说：
- **翻译文字**: "帮我翻译：今天天气不错"
- **翻译文件**: "翻译 my_works/xxx.md 为英文"
- **指定模型**: "用 qwen2.5:7b-instruct 翻译这段话"
- **切换语言**: "翻译成日语/法语/..."

## 配置调整

如果想切换默认模型，编辑 `~/.claude/mcp-servers/translate-ollama.py` 第 13 行：
```python
DEFAULT_MODEL = os.environ.get("TRANSLATE_MODEL", "gemma3:4b")  # 改成你想要的模型
```

或通过环境变量：在 `~/.claude.json` 的 MCP 配置中加 `"env": {"TRANSLATE_MODEL": "qwen2.5:7b-instruct"}`。

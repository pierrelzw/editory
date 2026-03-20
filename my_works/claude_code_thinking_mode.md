# 如何打开 Claude Code 的 Thinking Mode

> 一个快捷键的事，但 iTerm2 用户可能会卡住。

前两天有人问我：Claude Code 的 thinking mode 怎么打开？我说按 `Option+T` 就行了。

结果他说："我按了，没反应。"

一问，果然是 iTerm2。

## 什么是 Thinking Mode

Claude Code 有一个 "extended thinking" 模式。打开后，Claude 在回答之前会先进行一轮内部推理 —— 你可以理解为它在心里打了个草稿，想清楚了再说。

对于简单问题，thinking mode 不会有明显区别。但遇到复杂的 debug、架构设计、多文件重构这类任务，打开 thinking mode 后回答质量会有肉眼可见的提升。

## 怎么打开

**快捷键：`Option+T`**（macOS）或 `Alt+T`（Windows/Linux）

按一下，底部状态栏会显示当前状态。再按一下就关闭。

如果你想让它默认开启，在 `~/.claude/settings.json` 里加一行：

```json
{
  "alwaysThinkingEnabled": true
}
```

想看 Claude 具体在"想"什么，按 `Ctrl+O` 可以切换显示 thinking 的输出内容。

## iTerm2 用户注意

如果你用的是 macOS 默认的 Terminal.app，`Option+T` 直接就能用，不用做任何配置。

但如果你用 iTerm2，按 `Option+T` 大概率会看到这行提示：

> To enable alt+t, set Option as Meta in iTerm2 preferences (⌘,)

这是因为 iTerm2 默认把 Option 键保留给了 macOS 的**特殊字符输入**功能（比如 `Option+e` 输入重音符 `´`，`Option+u` 输入分音符 `¨`）。在这个模式下，Option 键按下去不会发送终端程序能识别的信号，所以 Claude Code 收不到你的快捷键。

**修复方法：**

1. 打开 iTerm2 偏好设置（`⌘,`）
2. 进入 **Profiles → Keys → General**
3. 把 **Left Option key** 从 `Normal` 改为 **`Esc+`**
4. 右侧的 Option 键同理，按需修改

改完之后，`Option+T` 就能正常触发 thinking mode 了。

**一个 trade-off：** 改成 `Esc+` 之后，Option 键就不能用来输入特殊字符了。如果你偶尔需要输入 `ñ`、`ß`、`°` 这类字符，可以只改左侧 Option，右侧保持 `Normal`。

## 为什么会有这个差异

简单说一下背景。

终端程序识别 `Alt+某键` 的方式，是监听 `Esc` + `字符` 这个序列。比如 `Alt+T` 实际上是先发一个 `Esc`，紧接着发一个 `t`。这是从早期 Unix 终端继承下来的约定 —— 那时候键盘上有一个专门的 Meta 键，现代键盘没了，就用 Option/Alt 替代。

macOS 默认的 Terminal.app 自动把 Option 映射成了这个行为，所以开箱即用。

iTerm2 选择了不同的默认值：它把 Option 留给了 macOS 原生的字符输入系统。这对写法语、德语的用户很友好，但对终端快捷键来说就需要手动切一下。

两个 app 只是默认值不同，都可以改。Terminal.app 替你做了选择，iTerm2 让你自己选。

## 其他相关快捷键

既然聊到快捷键，顺便列几个 Claude Code 里常用的：

- `Option+T` — 切换 thinking mode
- `Ctrl+O` — 显示/隐藏 thinking 输出
- `Escape` — 取消当前操作
- `Option+Enter` — 在输入框中换行（不发送）

如果你想自定义快捷键，可以编辑 `~/.claude/keybindings.json`。

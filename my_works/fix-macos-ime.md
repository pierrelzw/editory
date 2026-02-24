---
title: "macOS 中文输入法候选框飘了？一条命令搞定"
tags: [macOS, 输入法, 技巧]
platforms: [mowen]
type: short_post
---

macOS 自带中文输入法用着用着，候选词窗口突然飘到屏幕左下角或右上角，打字完全看不到选词…

所有 App 都会受影响，重启输入法就能修复。

打开终端，执行：

```bash
killall SCIM_Extension TextInputMenuAgent imklaunchagent
```

不用担心，系统会自动重新拉起这三个进程，候选框位置立刻恢复正常。

这三个进程分别是：
- SCIM_Extension — 系统中文输入法核心
- TextInputMenuAgent — 菜单栏输入法图标
- imklaunchagent — 输入法框架启动代理

如果重启进程还不行，去系统设置 > 键盘 > 输入法，把中文输入法删掉再重新添加即可。

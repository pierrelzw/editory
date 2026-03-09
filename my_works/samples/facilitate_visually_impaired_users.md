**2025.10.30 如何设计能让视障人士也能看你的网站？**

这里视障人士指的是色盲色弱人士

最近在 vibe 一个新的应用（以后详细说），在和 AI 聊天过程中，学会了一个浏览器的隐藏功能 —— 色盲模拟器。

这一次用的是 Codex，提了需求以后，它咔咔闷头干了十多分钟，给我生成了几百行代码（现在看还挺少的，有点意外），然后还写了一很不错的总结。

![](https://priv-sdn-001.mowen.cn/mo/file/meta/54/19/96/1983804600669970433.png?Expires=1772099223&OSSAccessKeyId=LTAI5tE16jzdfWCPVBmyB5Nn&Signature=fzeqCAHPlJBSg3P40WPm51BVFZ4%3D&response-expires=Thu%2C%2026%20Feb%202026%2009%3A47%3A03%20GMT)  

我一看，它应该是把网站的架子搭好了。但只是 build 成功了啊，基本功能还没验证呢。

我没有前端开发、UI 设计的经验，每次 AI 搞出来个这种没有真实数据的假前端，我就只能看个大概（ok，反正我不懂，你随便忽悠）。

这一次，我索性让它自己出 “验收标准”。

![](https://priv-sdn-001.mowen.cn/mo/file/meta/60/76/54/1983798982550958082.png?Expires=1772102878&OSSAccessKeyId=LTAI5tE16jzdfWCPVBmyB5Nn&Signature=UbrqVdVF5XdALPkTGLi%2Bimi2ccc%3D&response-expires=Thu%2C%2026%20Feb%202026%2010%3A47%3A58%20GMT)  

然后我就问它，哪些是可以自动化验证的？

\- 如果可以自动化，就直接让它自己做了。

\- 如果需要我人工看的，再一步步指导完成验收。

![](https://priv-sdn-001.mowen.cn/mo/file/meta/93/25/43/1983798982550958081.png?Expires=1772102878&OSSAccessKeyId=LTAI5tE16jzdfWCPVBmyB5Nn&Signature=1kK4l2Iqr2lIUphDClC9IqGK2FU%3D&response-expires=Thu%2C%2026%20Feb%202026%2010%3A47%3A58%20GMT)![](https://priv-sdn-001.mowen.cn/mo/file/meta/71/09/74/1983798982550958083.png?Expires=1772102878&OSSAccessKeyId=LTAI5tE16jzdfWCPVBmyB5Nn&Signature=a4Kq0z0PFNeBMLXmmImJzRm9u5w%3D&response-expires=Thu%2C%2026%20Feb%202026%2010%3A47%3A58%20GMT)  

这里，它提到的 “色盲模拟” 引起了我的注意。一开始我还没找到 Rendering 选项，后来找到以后就按照指导完成了验收。

有种自己的产品 “多了一些温度” 的感觉，也很感谢设计这个功能的人。

虽然我这个产品还是很初级的阶段，都还没上线。

当我为学会了这个功能开心的时候，脑子里也冒出了另一个想法：关注这种功能是不是太早了？

的确有点早。不过我这是独立开发，也没有人给我 deadline，就这样吧。有 AI 的帮助，其实也没有花什么时间。

而且，我还学会了一个新的前端或者 UI 设计的“验收标准” —— 视觉一致性。

我发现，这一次让 AI 重新开发的版本，过滤各种颜色以后，关键信息都能清晰显示。

从网页前端效果看，相比之前我自己提了很多详细需求以后让它开发的版本，好很多。

因为我实在没有经验，真的需要描述需求的时候，发现自己的词语都是匮乏的。

所以，这一次，我决定放手让 AI 来设计前端：

1\. 和 chatgpt 聊开发开发需求

2\. 把需求发给 Google Stich，让它生成前端页面。在这里，我特地删除了一些前端页面的需求，让 AI 自由发挥。

3. 最后让 Codex 开发的时候，我就让它参考 Google Stich 生成的前段页面

因为 AI 在前端/UI 设计领域显然比我专业，所以我给了它更多空间，它反而能做得更好。

我之前开发的虚拟试衣间应用，就遇到过用户和我反馈过关键信息不不够明信的情况 —— 在她的浏览器下， 某个按钮的文字和背景颜色太相近以致于很难找到。

不过，因为这个问题只发生在她的电脑上，她也说自己的电脑有问题，我就没有太关注。

现在想来，还是有设计上的问题。如果加上视觉一致性的验收标准，也许就能避免。

附录：

**如何使用浏览器的色盲模拟器？**

**打开浏览器 Devtools（F12 或者在网页右键选择 inspect） -> 点击右上角三点菜单 -> Rendering -> Emulate vision deficiencies，就可以切换色盲模拟。**

![](https://priv-sdn-001.mowen.cn/mo/file/meta/86/57/91/1983846487258648577.png?Expires=1772099223&OSSAccessKeyId=LTAI5tE16jzdfWCPVBmyB5Nn&Signature=yiUhNOuOHiCD0pL7zThMMU1PNxY%3D&response-expires=Thu%2C%2026%20Feb%202026%2009%3A47%3A03%20GMT)  

你可以选择过滤红色、绿色、蓝色以后的网页效果，甚至切换成灰度模式（no color）。

如果在这些模式下，网页关键信息都清晰可见，那这个网站的 “视觉一致性” 就算是过关了。

理论上，如果灰度模式下可以，那过滤任何一种颜色应该就没问题了。所以，也可以直接测试灰度模式。

如果你觉得打开浏览器 Devtools  太麻烦，用的还是 Macbook，可以尝试用 Mac 的 Color Filter 功能。

打开 spotlight(快捷键Command+空格) -> 输入 color filter -> 点击右侧的开关按钮即可）。

![](https://priv-sdn-001.mowen.cn/mo/file/meta/10/13/86/1983807311821697024.png?Expires=1772102878&OSSAccessKeyId=LTAI5tE16jzdfWCPVBmyB5Nn&Signature=FVv%2FhR0O%2B%2BoHOa4F2l6mCHIK7Zs%3D&response-expires=Thu%2C%2026%20Feb%202026%2010%3A47%3A58%20GMT)
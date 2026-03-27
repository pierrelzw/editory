**没有海外信用卡和电话卡，我是如何订阅 Claude 的？**

本文主要讲如何通过**「美区 Apple ID + App Store礼品卡 + iOS 内购」**订阅 Claude，还介绍了我用的科学上网终端。这个方案也适用于 ChatGPT/Gemini 的订阅。但是，**安卓用户就不太适合这个教程了**。

**如果你是苹果用户，跟着这篇教程操作，过程中有疑问或者改进建议，欢迎在评论区留言或者私信我。**

⚠️ **特别提醒：**

这个教程上线后，很多朋友尝试，我也收到了很多反馈。因为：

1. 步骤多（购买科学上网工具并安装在手机和电脑上、设置美区 AppleID、注册和订阅 Claude）
2. 依赖多（科学上网工具🪜、手机号或者邮箱）

因为不同的原因，每一步都可能遇到阻碍甚至失败。这可能需要你做好心理准备。

遇到问题后，可以去 Q\&A 看看，没有答案的话可以在评论区反馈，也可以私聊我。

如果你特别着急使用，最快捷的方式，可能是去 TaoBao 付费买一个账号，有时间再慢慢跟着这个教程折腾**。**

**具体步骤（太长不看版）**

1. 准备苹果手机端和电脑端的科学上网工具，支持美区 IP 地址
2. 注册一个美区 Apple ID
3. 登录 App Store，确认国家/地区为美国
4. 购买美区 Apple 礼品卡（见下文）,兑换礼品卡
5. 在 App Store 下载 Claude App，注册登录后，使用 Apple ID 余额订阅升级目标套餐（Pro/Max）

第 4 和 第 5 步都需要科学上网（建议美国 IP），且需要移动端和电脑端都配置好。如果你之前没有这方面的经验，这可能是你最耗时的部分。如果卡住了，建议尽快找人帮忙解决。

**需要准备什么**

**- 注册 Apple ID 的邮箱：** 一个**没有注册过 Apple ID** 的邮箱（Gmail、Outlook、QQ 邮箱均可）

**- 注册 Claude 的邮箱：** **一个没注册过 Claude 的邮箱**，建议 Gmail （实测 163，qq 都不行，如果没有，建议在手机端 gmail App 注册，网页注册很容易要求「二维码验证+短信验证」导致无法注册）

如果尝试注册过 Claude，可能已经被标记了，即便用美国 IP 还是会要求海外手机号（如果有这个问题，可能买个手机号是最快的解决方案了）

**- 手机号**：中国大陆手机号即可（+86），用于接收验证码

**- 支付宝：** 已实名认证，用于购买 Apple 美区礼品卡

**- iPhone 或 iPad** — 用于通过 Apple ID 余额完成订阅（**必须**，Mac 上无法使用 Apple ID 余额订阅）

**- 科学上网工具** — **必须**，推荐机场+Clash Verge Rev 客户端使用（下文详述）

**第一步：准备科学上网环境（建议美国 IP）**

**设置美区 Apple ID 支付方式、注册 Claude 账号、使用 Claude** 都需要🪜（推荐**美国 IP**）。注册 Apple ID 和买礼品卡不需要，用正常网络即可。

⚠️重要提醒： 使用 Claude 全程建议保持同一个节点，频繁切换 IP 可能触发风控

主要需要两个东西：

1）🪜订阅：因为大家都知道的原因没法直接在文章里推荐，可以私聊我，或者问问经常用 AI 的人，记得用 ping0.cc 检查 ip 纯净度。

2）**🪜**客户端：[https\://secure.shadowsocks.au/knowledgebase/151/](https://secure.shadowsocks.au/knowledgebase/151/) （如果未登录需要先登录，然后输入这个网址刷新）。

- Android：**[Clash for Android 设置方法](https://secure.shadowsocks.au/knowledgebase/186/)**
- IOS：推&#x8350;**[Spectre VPN 设置方法](https://secure.shadowsocks.au/knowledgebase/189/)** (免费 APP) 或者 [Shadowrocket 设置方法](https://secure.shadowsocks.au/knowledgebase/176/) (第三方付费 APP)
- 桌面端：**[[通用]Clash Verge Rev设置方法](https://secure.shadowsocks.au/knowledgebase/202/)** (**支持 Windows /macOS / Linux**)

推荐配置：Proxies 选择**美国节点**，同时开启**系统代理 + TUN（虚拟网卡）模式**

1. 安装 Clash Verge Rev 后打开，点击左侧 Profiles，在顶部输入框粘贴 🪜 订阅链接，点击 Import(导入）
2. 点击左侧 Proxies，在节点列表中选择一个美国节点（带有 US / 美国 标识）
3. 点击左侧 Settings，同时开启系统代理（ System Proxy）和 TUN（虚拟网卡）模式 —— 首次安装需要点击 “扳手按钮” 安装虚拟网卡
4. 访问 [https\://ip.sb/](https://ip.sb/) 确认 IP 地址为美国
5. 点击 Home》Proxy Mode 建议选择规则模式（Rule） —— 国内网站走直连、海外走代理，日常使用更顺畅。最后的效果如下图所示

**第二步：注册美区 Apple ID**

如果已经有美区 Apple ID（之前验证下载过美区 App）

1. 在手机或者电脑浏览器打开 Apple ID 注册页面（[https\://appleid.apple.com/account](https://appleid.apple.com/account)）
2. 填写注册信息：

- Country/Region：选择 United States（实测这一步选了不一定生效，App Store 登录后可能还要调整）
- Name：填英文名（随意，如 Li Wei）
- Birthday：生日设为 25 岁以上（部分内容有年龄限制）
- Email：填写你准备好的邮箱（这就是你的 Apple ID）
- Password：至少 8 位，包含大小写字母和数字，不要包含姓名或生日
- Phone Number：选 +86，填你的手机号

3. 完成邮箱验证码 + 手机验证码验证
4. 注册成功

**第三步：登录 App Store，确认国家/地区为美国**

1. 在 Iphone 手机上打开 App Store → 点击右上角头像 → 滑到最底部退出当前 Apple ID → 登录美区 AppleID → 点击账户名 → 确认国家/地区为美国。

如下图所示，如果地区没问题了，直接跳到第四步（有人有之前注册的美区 AppleID，有人直接淘宝购买的，所以都可以）

如果国家/地区显示为中国大陆（China Mainland），需要修改成美国（这一步需要科学上网）

系统会让你选择付款方式，并要求填写账单地址（可在[https\://www\.fakexy.com/us-fake-address-generator-or](https://www.fakexy.com/us-fake-address-generator-or) 生成），**选免税州可以避免额外税费**，比如 Oregon（俄勒冈州）

**第四步：在 Pockyt Shop 购买美区 Apple 礼品卡**

1. 打开**Pockyt Shop 官网** [https\://shop.pockyt.io](https://shop.pockyt.io/)，注册并登录（微信、邮箱都可以）
2. 选择 "App Store & iTunes US" 礼品卡
3. 输入充值金额付款
4. 支付完成后， 1 分钟左右看到兑换码（16 位字母数字），同时邮箱也会收到

**充值多少？按照你想要订阅的套餐价格充值即可**

**可先充值一个月试试，没问题后可以一次充值更多，避免自动订阅中断**

- Claude Pro — $20/月
- Claude Max 5x — $125/月
- Claude Max 20x — $250/月

⚠️ 重要提醒：

- 不要贪便宜买低价礼品卡！ 淘宝/闲鱼也可以，但低于面值的卡很可能是"黑卡"（盗刷信用卡购买），使用后会导致你的 Apple ID 被封禁，甚至设备被锁
- 正规渠道价格 = 面值 × 实时汇率（可能有小幅折扣，但不会打很大的折）
- 确认买的是美区（US） 的 Apple Gift Card

**- 保存好兑换码，每个码只能用一次**

**第四步：登录 App Store 兑换礼品卡 （需要 Iphone 手机或 IPAD）**

只有 iPhone / iPad 才能通过 Apple ID 余额订阅。 macOS 桌面版 Claude 的升级按钮会跳转到网页支付，网页端只接受信用卡/借记卡，无法使用 Apple ID 余额。请使用 iPhone 或 iPad 完成以下操作。

1. 退出 App Store 后重新进入，点击右上角头像，确认账户正确
2. 点击兑换充值卡或代码（ Redeem Gift Card or Code） → 手动输入兑换码（Enter Code Manually）
3. 粘贴上一步得到的兑换码，点击 Redeem，成功后余额显示在账户页面顶部

**第五步：下载 Claude 并订阅**

1. 在 App Store 搜索 Claude by Anthropic，下载安装
2. 打开 Claude App，保持科学上网，注册或登录 Claude 账号
3. 点击左上角进入 Settings → Subscription，选择订阅方案：

- Claude Pro：$20/月 — 适合日常对话 + 轻度 Claude Code
- Claude Max 5x：$125/月 — 5 倍用量，Claude Code 日常使用推荐
- Claude Max 20x：$250/月 — 20 倍用量，Claude Code 重度用户推荐

4. 点击订阅，系统自动从 Apple ID 余额扣款
5. 点击左下角头像，显示 Pro/Max Plan 则表示订阅完成！

**大功告成！**

到这里你已经成功订阅了 Claude Pro/Max。你可以：

- 移动端 ：下载并打开 Claude App 直接使用
- 桌面版：下载并打开 Claude Desktop App 直接使用。如果付费订阅，桌面端顶部会有 Chat/Cowork/Code 三个功能选项
- 网页版：访问 [https\://claude.ai](https://claude.ai/) 登录使用

\**- Claude Code：这是最推荐的 Claude AI 的使用方案。因为 Claude 的最大优势就是 “编程” 能力。**而且，经过一年的发展，Claude Code 几乎是公认的最佳 AI 编程工具了。

最强编程 AI 模型+最佳 AI 编程工具的结合，让 Claude Code 在编程领域一骑绝尘。

不仅如此，新的用法层出不穷，用 Claude Code 写文章、做文章配图、搭建自媒体工作流、甚至用 Claude Code 剪视频……

我也是 Claude Code 重度使用者，就在一个月前，[我决定全面转向 Claude Code](https://note.mowen.cn/detail/r0S_-wxVVPLqjrajojGqg)。

**Claude Code安装和配置在网上有很多，我也会在下一篇教程中详细介绍，欢迎持续关注。**

**常见问题**

**Q：我付费订阅了，公司报销要发票，在哪里找？**

A：去你的美区 Apple ID 注册邮箱里找。通过 IOS 内购订阅的， Apple 会给你的 Apple 邮箱发 Invoice。

**Q：Claude 的注册邮箱，需要和美区 Apple ID 的注册邮箱一致么？**

**A： 不需要。** Claude 的注册邮箱与美区 Apple ID 的注册邮箱可以不一致。

这两个账号在系统层面是相互独立的，苹果只负责支付环节，并不会强制要求应用内账号与 Apple ID 邮箱相同。当你在 iPhone 上订阅 Claude Pro 时，底层扣款是通过你当前登录的 **美区 Apple ID** 余额或支付方式完成的，这与你登录 Claude 客户端所用的邮箱地址**没有关联**。

推荐用 Gmail 邮箱注册，目前 Claude 主要通过 “魔法链接” 注册和**登录** —— 每次注册/登录，都会给你的邮箱发一封带验证码的邮件。如果你在 App 登录界面直接选择了 **"Continue with Apple"**，系统会默认使用你当前设备的 Apple ID 邮箱（或其生成的私有邮箱）来创建 Claude 账号。

Q：为什么 App store 订阅比官网贵？

因为苹果公司会对 App Store 付费应用抽成，所以通过 IOS 内购订阅 Claude Code，比在网页上用信用卡订阅更贵（比如 Claude Pro 订阅 ios 内购价格为 $20 vs 信用卡 $17 ）。但后者有比较高的门槛，需要美国/英国/新加坡等支持 Claude 使用国家的信用卡。

**Q：一定要美国 IP 地址么？**

A：不一定。如果你想订阅 Claude

理论上像日本、新加坡、荷兰、德国、英国这些 Claude/chatGPT/Gemini 等 AI 都支持的国家都可以。

只是因为 OpenAI Google 等几家一线 AI 公司 都在美国，所以我推荐使用美国 IP + 美国 AppleID，更大概率没问题。我就会推荐新手使用。我个人实测，偶尔用一个荷兰、德国的节点也没问题，但要注意不要频繁切换。否则你上一秒还在荷兰、下一秒就去了美国，然后又去了日本。这明显就会被判断你在用 VPN，如果你更不谨慎，甚至切换到了香港、中国大陆等不被 Claude 支持的国家/地区，就更容易被封了。

大家都说 IP 纯净度比较重要，也好理解。因为如果有一些 IP 很便宜，被一些人滥用用来注册这些 AI 了，自然容易被标记为高风险的 IP，进而会把用这些 IP 的账户也标记为高风险。你可以通过访问 [https\://ping0.cc/](https://ping0.cc/) 来测试自己的 IP 是否干净。

**Q：首次登录 App Store ，改了地区为美国，但看不到 "None" 付款选项？**

A：大概率是因为 IP 不是美国。首次在 App Store 登录美区 ID 时必须使用美国 IP，付款方式才会出现 "None" 选项。

如果你使用 Clash Verge，请确认已开启**系统代理 + TUN（虚拟网卡）模式**，并在 Proxies 里选择了Proxy》美国节点。浏览器访问 [https\://ip.sb](https://ip.sb/) 确认国家是 US 后再操作。

**Q：注册时选了美国，但登录 App Store 后发现还是中国大陆怎么办？**

A：这说明你的 Apple ID 地区没有成功切换到美国，或者被自动重置了。解决方法：开启科学上网并使用美国节点，然后在 App Store 中点击右上角头像 → 点击你的 Apple ID → Country/Region（国家/地区） → 选择 United States → 按提示填写美国地址信息（参考上文免税州地址）。修改完成后退出 App Store 重新进入即可。

**Q：为什么 Clash Verge Rev 要同时开系统代理和 TUN（虚拟网卡）模式？**

A：

- 系统代理：让浏览器等常规应用走代理
- TUN 模式：接管所有网络流量（包括终端、命令行工具）
- 如果只开 TUN 不开系统代理，部分 UDP 转发会失效(看 Logs 页面就可以发现）走 Direct，可能导致 Claude 检测到你不在它支持的区域或者 ip 跳变，轻则导致暂时无法使用，重则封号
- 两者同时开启可以更确保 Claude 相关的网络走代理

**Q：机场订阅有什么要求？**

A：Clash Verge Rev 基于 Clash Meta 内核，支持主流协议（Shadowsocks、VMess、Trojan、VLESS、Hysteria2 等）。绝大多数机场都提供 Clash 订阅链接，直接导入即可。选机场时只要注意：

- 必须有美国节点
- 推荐稳定的中大型机场，不建议用免费节点（不稳定且有安全风险）

**Q：用了美国 IP 节点，也按照上面的网络配置了，注册/登录 Claude 还是要求输入手机号怎么办？**

原因：可能是尝试用这个邮箱注册失败过，被标记了

- 买个海外手机号（需要咨询买过的同学）
- 换个邮箱（推荐 Gmail，其他我还没验证过）
-

**Q：支付宝里找不到 Pockyt Shop / 礼品卡入口？有其他购买礼品卡的渠道吗？**

A：

- 支付宝的入口经常调整。如果找不到，可以直接通过 Pockyt Shop 官网购买：[https\://shop.pockyt.io](https://shop.pockyt.io/) ，支持支付宝扫码付款，效果一样。
- Apple 官网：[https\://www\.apple.com/shop/gift-cards](https://www.apple.com/shop/gift-cards)，Applepay 绑定国内银行visa信用卡也可以直接在Apple 美区官网购买礼品卡充值
- 淘宝/闲鱼：注意风险，低价卡大概率是黑卡，会导致 Apple ID 被封

**Q：美区 Apple ID 会影响我现有的国区 ID 吗？**

A：不会。建议：

- iCloud 保持国区 ID（保留通讯录、照片、iMessage 等）
- App Store 单独切换到美区 ID（仅用于下载和订阅）

**Q：可以在 iPhone 上直接注册美区 Apple ID 吗？**

A：可以。设置 → 顶部头像 → 退出登录 → 登录 iPhone → 没有或忘记 Apple ID → 创建 Apple ID → 国家选 United States。注册本身不需要科学上网，但首次在 App Store 登录时需要美国 IP，付款方式才会出现 "None" 选项。整体来说官网注册更简单直观，推荐优先用官网。

**Q：订阅后可以取消吗？**

A：可以。iPhone「设置」→ Apple ID → 订阅 → Claude → 取消订阅。取消后当前周期内仍可使用，到期后不再续费。

如果支付方式选择 None，IOS内购就只能通过 Apple ID 余额订阅，类似预充值电话卡的方式，不充值的话也就没法继续订阅了。

**Q：还有其他免税州地址可以用吗？**

A：可以。除了 Oregon，以下免税州也可以：

- Delaware — Wilmington, 302, 19801
- Montana — Billings, 406, 59101
- New Hampshire — Manchester, 603, 03101
- Alaska — Anchorage, 907, 99501

**费用总结**

- 美区 Apple ID — 免费
- 科学上网工具（机场） — 约 ¥15-50/月（视机场而定）
- Apple 礼品卡 — 面值 × 实时汇率（如 $20 ≈ ¥145）
- Claude Pro — $20/月（≈ ¥145/月）
- Claude Max 5x — $125/月（≈ ¥910/月）
- Claude Max 20x — $250/月（≈ ¥1820/月）

汇率仅供参考，以实际支付时为准。

**参考资料**

- [美区 Apple ID 注册教程 - 小木研习社](https://www.xmpick.com/apple-id/)

- [2025 最全美区 Apple ID 注册教程 - Extrabux](https://www.extrabux.com/chs/guide/5532699)

- [美区 Apple ID 礼品卡购买充值教程 - 知乎](https://zhuanlan.zhihu.com/p/636121931)

- [Clash Verge 使用教程](https://clashverge.la/tutorial/)

- [Claude Code 官方设置文档](https://code.claude.com/docs/zh-CN/setup)

没有海外信用卡，如何订阅 Claude / ChatGPT / Gemini？

> 美区 Apple ID + 礼品卡 + iOS 内购，三步搞定。

前段时间，一个朋友问我："我想用 Claude，但注册完发现要订阅才好用，又没有海外信用卡，怎么办？"

我给他发了一套操作流程，他跟着做，半小时搞定了。后来陆续又有几个人问同样的问题，干脆写出来。

这个方法我自己用了一年多，订阅 Claude、ChatGPT 都没出过问题。也适用于 Gemini 和其他需要美区付费的 App。

**核心思路：注册一个美区 Apple ID → 充值礼品卡 → 在 iPhone 上用余额内购订阅。**

⚠️ 因为苹果对 App 内购抽成，iOS 内购价格会比信用卡订阅贵一点（比如 Claude Pro 内购 $20 vs 信用卡 $17）。但对于没有海外信用卡的人来说，这是最简单稳定的方案。


**需要准备什么**

- **邮箱** — 一个没注册过 Apple ID 的邮箱（Gmail、Outlook、QQ 邮箱都行）
- **手机号** — 中国大陆 +86 手机号，接收验证码
- **iPhone 或 iPad** — 必须，Mac 上无法用 Apple ID 余额订阅
- **科学上网** — 必须，建议美国 IP 节点


**1. 科学上网**

注册 Apple ID 本身不需要科学上网。但后面设置付款方式、注册 AI 账号、日常使用都需要美国 IP。

你需要一个机场（代理服务商）+ 一个代理客户端。推荐 [Clash Verge Rev](https://clashverge.net/)，支持 macOS / Windows / Linux / 移动端。

配置好后，选一个美国节点，**同时开启系统代理 + TUN（虚拟网卡）模式**。

验证方法：浏览器打开 [https://ip.sb](https://ip.sb)，确认显示的国家是 US。


**2. 注册美区 Apple ID**

打开 [Apple ID 注册页面](https://appleid.apple.com/account)，填写：

- **Country/Region** — 选 United States
- **Name** — 英文名（随意）
- **Birthday** — 设为 25 岁以上（部分内容有年龄限制）
- **Email** — 你准备好的邮箱，这就是你的 Apple ID
- **Password** — 至少 8 位，包含大小写字母和数字
- **Phone Number** — +86，填你的手机号

完成邮箱 + 手机验证码验证，注册就搞定了。


**3. 登录 App Store，设置付款方式为 None**

在 iPhone 上打开 App Store → 点右上角头像 → 退出当前 Apple ID → 登录你的美区 Apple ID。

**这一步需要开科学上网（美国 IP）**，否则付款方式不会出现 "None" 选项。

登录后点击用户 ID，确认国家/地区是美国。如果显示中国大陆，需要手动改成美国。系统会要求填账单地址，在 [fakexy.com](https://www.fakexy.com/us-fake-address-generator-or) 生成一个即可。**选免税州可以避免额外税费**，比如：

- Oregon（俄勒冈） — 推荐
- Delaware — Wilmington, 302, 19801
- Montana — Billings, 406, 59101
- New Hampshire — Manchester, 603, 03101


**4. 购买美区 Apple 礼品卡**

推荐渠道：

- **[Pockyt Shop](https://shop.pockyt.io)** — 支持支付宝扫码付款，搜索 "App Store & iTunes US"，选金额，付款后 1 分钟左右拿到 16 位兑换码。这是我一直在用的渠道
- **[Apple 美区官网](https://www.apple.com/shop/gift-cards)** — 需要 Visa/Mastercard 信用卡或 Apple Pay
- 支付宝 App 内搜索 "Pockyt" 也能找到入口，但位置经常变

**充多少？** 按你想订阅的套餐价格来：

- Claude Pro / ChatGPT Plus — $20/月
- Gemini Advanced — $20/月
- Claude Max 5x — $125/月

建议先充一个月试试。

⚠️ **不要贪便宜买低价礼品卡！** 淘宝/闲鱼上低于面值的卡大概率是黑卡（盗刷信用卡购买），用了会导致 Apple ID 被封。正规渠道价格 = 面值 × 实时汇率。


**5. 兑换礼品卡**

在 iPhone 上打开 App Store → 点右上角头像 → **Redeem Gift Card or Code** → **Enter Code Manually** → 粘贴兑换码 → 点 Redeem。

成功后余额会显示在账户页面顶部。


**6. 下载 App 并订阅**

以 Claude 为例：

1. App Store 搜索 "Claude by Anthropic"，下载
2. 打开 App，保持科学上网，注册或登录
3. 进入 Settings → Subscription，选择套餐，点订阅
4. 系统自动从 Apple ID 余额扣款

ChatGPT、Gemini 流程一样——下载对应 App，登录后在设置里找到订阅入口。

**只有 iPhone / iPad 才能通过 Apple ID 余额订阅。** Mac 桌面端会跳转网页支付，网页端只接受信用卡。


**7. 验证余额支付是否正常**

如果你不确定余额支付能不能用，不想直接订阅 $20 的服务来试：

1. 在 App Store 找一个 $0.99 的付费 App，购买
2. 确认余额被扣减 → 说明支付正常
3. 到 [reportaproblem.apple.com](https://reportaproblem.apple.com) 申请退款，几天内退回余额

这样零成本验证。


**"无法完成购买" 怎么办？**

这是最常见的报错，可能的原因和解决办法：

- **IP 不是美国** — 最常见的原因。确认 Clash Verge 已开启系统代理 + TUN，浏览器打开 [ip.sb](https://ip.sb) 确认是 US
- **余额不足** — 检查账户余额是否够扣款金额（含税）
- **地区不匹配** — App Store 里确认国家/地区是 United States，不是 China Mainland
- **新账号风控** — 刚注册的 Apple ID 有时会被临时限制购买。等 24-48 小时再试，或联系 Apple 客服解除
- **付款方式问题** — 确认付款方式是 None（纯余额支付），不要绑定中国大陆的银行卡


**常见问题**

**Q：美区 Apple ID 会影响我现有的国区 ID 吗？**

不会。iCloud 保持国区 ID（通讯录、照片、iMessage 不受影响），App Store 单独切换到美区 ID 就行。

**Q：AI 服务的注册邮箱需要和 Apple ID 一致吗？**

不需要。Apple ID 只负责支付，和你用什么邮箱注册 Claude/ChatGPT 没关系。

**Q：注册 Claude 时要求输入海外手机号？**

可能是之前用这个邮箱注册失败过，被标记了。换一个 Gmail 邮箱试试。

**Q：订阅后可以取消吗？**

可以。iPhone「设置」→ Apple ID → 订阅 → 选择对应 App → 取消订阅。取消后当月仍可用，到期不续费。付款方式选了 None 的话，余额用完也不会续费。

**Q：一定要美国 IP 和美国 Apple ID 吗？**

不一定。日本、新加坡等 AI 服务支持的国家也行。但美国是 AI 公司大本营，用美区出问题的概率最低。


**费用总结**

- 美区 Apple ID — 免费
- 科学上网（机场） — 约 ¥15-50/月
- Apple 礼品卡 — 面值 × 实时汇率（如 $20 ≈ ¥145）
- AI 订阅 — $20/月起

有问题欢迎留言。

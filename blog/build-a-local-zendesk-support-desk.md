---
title: "把 Gmail、Shopify 和 AI 变成一套本地 Zendesk 客服系统"
description: "一份可以在另一台电脑复现的本地客服工作台方案，附 Codex Skill、GitHub 仓库和可复制部署 Prompt。"
pubDate: 2026-08-17
tags: [Codex, Gmail, Shopify, Customer Support, Zendesk, AI]
draft: false
---

我一直有三个客服痛点：不知道客户什么时候回了邮件，不翻译就难以判断紧急程度，也很难快速决定下一步该做什么。

所以我做了一套本地优先的 Zendesk 风格客服系统。它不是简单地把 Gmail 搬进网页，而是把完整邮件线程、Shopify 客户和订单、官网政策、AI 中文总结、处理建议以及可编辑回复草稿放到同一个工作台里。

## 它解决什么问题

这套系统只显示 Shopify 已有邮箱的客户邮件，因此可以把售前陌生邮件与已注册或已购买客户清楚分开。

每个 Case 会显示：

- 完整 Gmail 往来线程
- Shopify 客户和订单信息
- 中文事件摘要
- 中文处理建议
- 按客户语言生成的回复草稿
- 客服状态、优先级和 Activity 审计记录

后续版本还加入了“尾程物流异常 AI”：把物流商的派送失败通知粘贴进去，系统会识别原单号和转单号、匹配 Shopify 订单和客户、生成中文判断与客户语言草稿，再经过人工确认发送。它不能承诺再次派送、退款或赔偿，也不能编造尾程联系方式。

AI 回复不是直接发送。页面保留两个框：上方输入一次性修改要求，下方是可以继续人工编辑的最终回复。发送邮件还必须经过“准备发送”和“再次确认”两个步骤。

## 为什么把搭建方法做成 Skill

只写一篇安装教程还不够。不同电脑的 Node、Google OAuth、Shopify 权限和本地路径都可能不同。因此我把架构、数据规则、权限边界、同步机制、验收标准和部署顺序蒸馏成一个 Codex Skill。

在另一台电脑上，Codex 可以读取 Skill 后先检查环境，再逐步搭建，而不是机械执行一组可能已经过时的命令。

GitHub：[KryoZon Zendesk Support Desk Skill](https://github.com/ddcarolyn/kryozon-zendesk-support-desk-skill)

## 核心架构

本地版使用 React、Vite、Node API 和 SQLite。Gmail 负责邮件线程，Shopify 负责客户和订单事实，DeepSeek 负责中文总结、行动建议和回复草稿。

系统先同步 Shopify 客户，再读取 Gmail。只有外部联系人的邮箱能在 Shopify 客户或订单中精确匹配时，邮件线程才会进入 Case 列表。

同步必须采用幂等 upsert：即使某次 Gmail 请求失败或只返回一部分线程，也不能把已有 Case 清空。这是从“能跑的 Demo”变成“可靠客服系统”最重要的一条规则。

## 权限与安全

Gmail 只使用两个最小权限：

- `gmail.readonly`：读取完整线程
- `gmail.send`：人工确认后发送回复

Shopify 始终只读，AI 不允许执行退款、补发、取消订单等业务动作。所有 `.env`、OAuth Token、SQLite 数据库和客户内容都不能进入 GitHub。

如果 `support@kryozon.com` 是 Google Workspace 中的别名，它不需要单独登录。系统应使用邮箱所有者完成 OAuth，再通过 Gmail 已验证的 “Send mail as” alias 发信。

## 在公司电脑部署

先从 GitHub 安装 Skill，然后把下面这段 Prompt 完整复制给 Codex：

```text
Use $zendesk-support-desk-builder to build and verify a local Zendesk-style customer support desk on this computer.

Business goal:
- Show only Gmail threads whose external customer email exists in Shopify customers or orders.
- On one click, show the latest Cases that need a reply.
- Display the complete Gmail thread, matched Shopify order facts, a Chinese AI summary, a Chinese recommended next step, and an editable reply draft in the customer's language.
- Let me give DeepSeek a one-time revision instruction; do not keep a visible chat history.
- Email sending must use a prepare-and-confirm flow, reply inside the original Gmail thread, and send from the verified support@kryozon.com alias while authenticating with the mailbox owner's Google Workspace account.

Deployment requirements:
1. Build the local edition first using React/Vite, a local Node API, and SQLite.
2. Use Gmail readonly and send scopes only. Keep Shopify strictly read-only.
3. Start Gmail synchronization from March 1, 2026, then use incremental sync.
4. Never clear existing Cases when a sync is partial or fails.
5. Store every credential only in local environment variables or protected token files. Never print credentials, copy them into chat, or commit them.
6. Before installing system packages, changing scheduled services, sending test mail, or deploying online, show me the exact action and ask for approval.
7. Run the Skill's preflight and acceptance checklist. Do not stop at “the build succeeded”; compare Gmail, Shopify, database, and UI counts and show the verified result.

Begin by inspecting this computer and reporting only the missing prerequisites. Then implement everything you can safely complete without credentials. Give me beginner-friendly OAuth steps only when the application is ready for authorization.
```

## 最后的验收标准

我不会再用“页面能打开”作为完成标准。真正完成必须同时满足：同步不会丢 Case；Gmail、Shopify、数据库和 UI 数量能解释清楚；完整线程可见；AI 总结和草稿可用；发送前有确认；发送成功有提示和 Activity；失败时草稿不会消失。

这套方法的重点不是复刻 Zendesk 的外观，而是把客服响应速度、事实准确性和安全边界一起做好。

## 让 Skill 跟着产品继续进化

客服系统会持续升级，因此 Skill 也不应该停留在第一次发布的版本。项目采用“持续蒸馏”方式：每天比较 Obsidian 需求文档和本地生产源码，只把已经验证的长期规则、踩坑经验、接口约束和验收标准更新进 Skill。

自动更新不会上传客户邮件、订单、数据库、日志、OAuth Token、API Key、构建文件或 Cloudflare 资源 ID，也不会自动部署生产客服系统。只有 Skill 本身发生安全且有意义的变化时，才提交到指定的 GitHub 仓库。

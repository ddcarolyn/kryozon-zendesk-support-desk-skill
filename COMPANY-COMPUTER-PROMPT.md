# Company computer deployment prompt

Copy the prompt below into Codex on the company computer after installing this Skill.

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

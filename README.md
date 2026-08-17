# KryoZon Zendesk Support Desk Skill

A reusable Codex Skill for building a local-first, Zendesk-style customer support desk from Gmail threads, Shopify customer/order facts, policy knowledge, and AI-assisted summaries and reply drafts.

## Install on another computer

```bash
git clone https://github.com/ddcarolyn/kryozon-zendesk-support-desk-skill.git
mkdir -p ~/.codex/skills
cp -R kryozon-zendesk-support-desk-skill/zendesk-support-desk-builder ~/.codex/skills/
```

Restart Codex, then copy the prompt from [COMPANY-COMPUTER-PROMPT.md](COMPANY-COMPUTER-PROMPT.md).

## What the Skill contains

- Local and Cloudflare architecture
- Gmail OAuth, synchronization, thread reply, and send-as alias rules
- Shopify read-only matching rules
- Zendesk-style Case workflow and UI requirements
- DeepSeek summary, advice, translation, and editable draft contract
- Security boundaries and cross-device deployment playbook
- Acceptance checklist that compares source, database, and UI counts

## Security

This repository contains no customer email, order data, OAuth token, API key, database, Cloudflare resource ID, or local credential path. Configure secrets independently on each computer and never commit them.

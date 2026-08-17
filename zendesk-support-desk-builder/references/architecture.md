# Architecture

## Goal

Reduce support response time and improve reply quality by making new customer replies visible, understandable, actionable, and safely replyable from one workspace.

## Data flow

```text
Gmail threads ──┐
                ├─> normalization + customer matching ─> Cases ─> Zendesk-style UI
Shopify data ───┘                                      │
                                                       ├─> AI summary/advice/draft
Policy knowledge ──────────────────────────────────────┘
```

## Local edition

- Frontend: React + Vite.
- API: Node middleware or a small Node server.
- Database: SQLite stored outside the Git repository.
- Gmail token: local file with mode 0600, stored outside the repository.
- Secrets: `.env`, excluded from Git.
- Sync: manual refresh; optional OS scheduler only after explicit approval.

## Online edition

- Frontend/API: Cloudflare Worker with static assets.
- Database: D1.
- Secrets: Worker secrets.
- OAuth token: AES-GCM encrypted before D1 storage; encryption key remains a Worker secret.
- Access: Cloudflare Access allowlist plus an application-level mailbox check.
- Sync: scheduled Worker plus manual refresh.

## Core tables

- `gmail_threads`: thread ID, subject, participants, last message ID, timestamps, latest sender, raw sync metadata.
- `gmail_messages`: message ID, thread ID, RFC Message-ID, sender, recipients, date, body, attachments metadata.
- `shopify_customers`: Shopify ID, normalized email, name, registration metadata.
- `shopify_orders`: Shopify ID, order number, customer email, dates, products, amount, payment, fulfillment, tracking.
- `cases`: stable ID, Gmail thread ID, matched customer/order, status, priority, summary, advice, draft, timestamps.
- `activities`: Case ID, action type, actor, timestamp, non-secret metadata.
- `sync_state`: source, cursor/history ID, started/finished timestamps, counts, error.
- `send_attempts`: request ID, Case/draft revision, body hash, status, Gmail message ID.

## Matching policy

Accept a support Case only when the normalized external email matches either:

1. a Shopify customer email, or
2. an email on a Shopify order.

Mark exact email matches as high confidence. Treat order-number-only matches as reviewable, not definitive. Never merge two customer identities solely from similar names.

## Non-negotiable safety boundaries

- Shopify remains read-only.
- AI cannot execute business actions.
- Email send always requires a human confirmation.
- Sync is additive/upsert-based; a partial source response cannot clear the Case table.
- Customer content, OAuth tokens, databases, and logs never enter a public repository.

# Production lessons

## Mailbox owner and support alias

Authenticate the primary Google Workspace mailbox owner. Treat `support@kryozon.com` as the verified receive/send-as alias, not as a separate Gmail login.

Do not require historical threads to contain the support alias. Historical customer conversations may have used the primary address. Read eligible non-marketing threads from the primary mailbox, then apply the Shopify email match in the business layer. Requiring `{to:support from:support}` caused valid Shopify customers to disappear from the online edition.

## Backfill and incremental synchronization

- Backfill from 2026-03-01 through every Gmail page.
- Persist the next page token after each completed page.
- Keep a task lock with stale-lock recovery.
- Return immediately from manual sync and continue bounded work in the background.
- Expose running, error, finished time, backfill completion, and current counts through a status endpoint.
- Advance the final cursor only after the batch succeeds.
- Never clear existing Cases after a partial response or timeout.

## Automatic replies and manual status

Detect automatic replies from subject prefixes and `Auto-Submitted` headers. Exclude them from the needs-action queue.

Persist a manual status override together with the timestamp of the message on which it was based. Keep the override while the thread is unchanged. Remove it when a newer message arrives so the Case can be classified again.

## Last-mile logistics alert workflow

Support a separate operator workflow for pasted last-mile exception notices:

1. Extract original, transferred, and generic tracking numbers.
2. Match any extracted number against Shopify order tracking data.
3. Load the customer, order, and most recent related Case.
4. Use AI to produce a Chinese summary, Chinese next action, urgency, customer language, subject, and editable customer draft.
5. Preserve exact tracking numbers, stated exception reason, and verified carrier contact.
6. Never invent a carrier contact or promise redelivery, compensation, refund, replacement, or a deadline.
7. Allow a one-shot AI revision instruction without displaying chat history.
8. Prepare and confirm a new outbound email with a ten-minute confirmation token and duplicate-send protection.
9. On success, create or update a Pending Case and write the Gmail send audit.

## UI behavior verified in production

- Provide separate functional modules for customer mail, Shopify orders, and Knowledge Base.
- Show explicit sync progress rather than an endless spinner.
- Show success and failure toasts for Gmail sending.
- Preserve drafts after cancellation or failure.
- Make Case status editable for Open, Pending, On-hold, Needs Review, and Closed.
- Show sender, recipient, result, error, and time in Activity.
- Keep the two-field AI interaction: temporary instruction and editable final reply.

## Local/online parity and reminders

- Do not maintain separate Gmail filters or status rules for SQLite and D1. Put them behind shared business logic with storage adapters.
- Verify parity by diffing stable Case fields in both directions; a total such as “20 vs 20” can still hide different Cases.
- Notify Feishu only after a Case is durably stored as newly Open or reopened. Deduplicate by Gmail thread plus latest message/update revision.
- AI analysis or Feishu failure must be observable but must not erase or hide the underlying Case.

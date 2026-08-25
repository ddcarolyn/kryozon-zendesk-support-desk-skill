# Acceptance checklist

## Data

- Shopify customer and order pagination completes.
- Gmail backfill reaches the configured baseline date.
- Every visible Case matches a Shopify email.
- UI totals equal database totals for each status.
- Re-running sync does not duplicate or remove Cases.
- A failed page can resume without starting over.
- Local and online exports have the same Case IDs and matching customer, subject, status, and update fields.
- Every local-only, online-only, or mismatched Case is listed and explained; equal totals are not accepted as proof.

## Workflow

- Complete Gmail thread is visible chronologically.
- Chinese summary and recommended action are present.
- Draft language follows the customer's language.
- AI instruction input is cleared after generation.
- Final reply remains directly editable.
- Status views and right-side customer/order/knowledge/activity tabs work.
- Shopify Orders and Knowledge Base open as functional modules rather than decorative navigation.

## Notifications

- A newly Open or reopened Case creates one Feishu alert with customer, order, Chinese summary, urgency, next action, and Case link.
- Re-running the same sync does not send the same alert again.
- Notification failure is recorded and does not roll back the Case sync.
- Feishu cannot trigger or send a customer email.

## Sending

- Authenticated mailbox and selected From alias are visible.
- Prepare dialog shows recipient, From, subject, and exact body.
- Confirm sends only once.
- Success toast is visible.
- Activity contains Gmail message ID and timestamp.
- Failure preserves the draft and Case status.

## Security

- No secret or database file is tracked by Git.
- No credential is exposed to browser JavaScript.
- Shopify code contains no mutation.
- Application is inaccessible outside the approved identity list.
- Logs contain no OAuth refresh token or API key.

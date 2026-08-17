# Acceptance checklist

## Data

- Shopify customer and order pagination completes.
- Gmail backfill reaches the configured baseline date.
- Every visible Case matches a Shopify email.
- UI totals equal database totals for each status.
- Re-running sync does not duplicate or remove Cases.
- A failed page can resume without starting over.

## Workflow

- Complete Gmail thread is visible chronologically.
- Chinese summary and recommended action are present.
- Draft language follows the customer's language.
- AI instruction input is cleared after generation.
- Final reply remains directly editable.
- Status views and right-side customer/order/knowledge/activity tabs work.

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

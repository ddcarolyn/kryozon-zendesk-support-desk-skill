# Acceptance checklist

## Data

- Shopify customer and order pagination completes.
- Gmail backfill reaches the configured baseline date.
- Every visible Case matches a Shopify email.
- A Shopify customer without an order is visible as pre-sales; a customer with an order is visible as after-sales.
- A genuine human message routed to the support alias but unmatched in Shopify is excluded.
- UI totals equal database totals for each status.
- Re-running sync does not duplicate or remove Cases.
- A failed page can resume without starting over.
- A combined sync refreshes Shopify before Gmail classification.
- Shopify and Gmail expose separate last-success and error states. Force each connector to fail in turn and verify that the other connector's successful progress is preserved, while the combined cycle remains visibly incomplete.
- An unchanged Shopify cycle performs no unnecessary object upserts. When changed records exceed the online write budget, the result reports deferred work and `complete=false`; later idempotent cycles reach zero deferred records without removing existing orders or Cases.
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
- The Shopify Orders module shows the latest durable order result, last successful Shopify sync, and a source-specific sync error without hiding Gmail results.
- The FAQ dashboard count equals the visible eligible pre-sales Case set and excludes every unmatched support-routed sender.
- Every pre-sales FAQ category is one of `vat_invoice`, `product_selection`, `compatibility`, `shipping`, `discount`, `availability`, or `other`; after-sales Cases have no pre-sales FAQ category.
- Saving a FAQ template or toggling recognition keeps automatic sending off and sends no customer email.

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
- When the local workstation uses a macOS HTTPS proxy, local Gmail, Shopify, and AI connectivity works without logging proxy credentials; Cloudflare behavior remains unchanged.

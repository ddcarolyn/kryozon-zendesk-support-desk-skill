# Integration contracts

## Gmail OAuth

Use a Web application OAuth client. Configure exact redirect URIs for each environment.

Scopes:

- Read: `https://www.googleapis.com/auth/gmail.readonly`
- Send: `https://www.googleapis.com/auth/gmail.send`

Use `access_type=offline`, `include_granted_scopes=true`, state validation, and consent when requesting a refresh token. Verify the authenticated Google profile. A Workspace alias such as `support@example.com` is not a separate login; authenticate the mailbox owner, then verify the alias in Gmail “Send mail as” settings and use it as the From address.

## Gmail synchronization

- Initial backfill: configured baseline date.
- Incremental sync: Gmail history ID when available; otherwise a bounded recent-window query with idempotent upserts.
- Exclude newsletters, marketing, automated Shopify notifications, internal mail, and system notices.
- Apply Shopify eligibility after Gmail retrieval: a normalized external email must match a Shopify customer or order. Delivery to the support alias is routing evidence, not an eligibility override.
- Fetch complete threads, not only the latest message.
- Persist progress after each page.
- Display sync phase, scanned count, matched count, excluded count, and error details.
- When Shopify and Gmail run in one sync cycle, complete the Shopify refresh first so email eligibility and Case type use the newest available read-only customer and order snapshot.
- Isolate connector failures. Persist Shopify and Gmail last-success times and errors separately; a failure in one stage must not roll back or suppress successful work from the other stage. If Gmail proceeds after a Shopify failure, classify only against the last durable Shopify snapshot and surface that the combined result is stale or incomplete.

Classify an eligible Shopify customer with no order as pre-sales and one with an order as after-sales. Keep unmatched support-routed mail out of the Case set unless the requirements explicitly change.

## Pre-sales FAQ classification

Run FAQ classification only after Shopify eligibility has been established and only for pre-sales Cases with no matched order. Use a fixed identifier set:

- `vat_invoice`
- `product_selection`
- `compatibility`
- `shipping`
- `discount`
- `availability`
- `other`

Store the category and bounded confidence independently from the Chinese summary, advice, customer language, and editable reply draft. Heuristics may provide an initial category and AI may refine it through structured output, but neither path may admit an unmatched sender or create an outbound email.

Expose the same FAQ rule shape locally and online: identifier, label, description, reviewed template, recognition-enabled flag, automatic-send flag, and timestamps. A rule update may change the reviewed template and recognition flag, but it must always persist `auto_send=false`. Automatic sending requires a separate explicitly approved workflow and must not be coupled to saving a template or toggling recognition.

## Gmail reply construction

- Recipient: latest external message's Reply-To, otherwise From.
- Subject: preserve the thread subject.
- Headers: include RFC `In-Reply-To` and `References`.
- Request: send raw MIME with Gmail `threadId`.
- Sender: verified support send-as alias.
- Idempotency: store a unique request ID and draft revision before sending.

## Shopify

Use Admin GraphQL read queries only. Retrieve:

- customers: ID, email, display name, updated time
- orders: ID, name/number, creation time, financial and fulfillment status
- line items: title/name and quantity
- fulfillments: tracking numbers
- totals: amount and currency

Never include mutation operations. Page through all results and persist the page cursor.

Compare fetched objects with the stored snapshot before writing. Skip unchanged customers and orders. When the online runtime needs a per-invocation D1 write budget, return changed, unchanged, deferred, page, and completion counts; keep the cycle incomplete while any changed record is deferred, then retry idempotently on a later scheduled or manual cycle.

## AI provider

Keep the provider behind a server-side adapter. The browser never receives the API key. Accept a Case context object and return strict JSON. Store only the latest generated summary, advice, and editable draft unless the user explicitly requests history.

## Policy knowledge

Store policy title, canonical URL, retrieval time, and normalized text. Cite the canonical URL beside the draft. Do not claim a policy fact unless it exists in the retrieved policy text.

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
- Fetch complete threads, not only the latest message.
- Persist progress after each page.
- Display sync phase, scanned count, matched count, excluded count, and error details.

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

## AI provider

Keep the provider behind a server-side adapter. The browser never receives the API key. Accept a Case context object and return strict JSON. Store only the latest generated summary, advice, and editable draft unless the user explicitly requests history.

## Policy knowledge

Store policy title, canonical URL, retrieval time, and normalized text. Cite the canonical URL beside the draft. Do not claim a policy fact unless it exists in the retrieved policy text.

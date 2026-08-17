# Deployment playbook

## Local deployment

1. Install current Node.js LTS, Git, and Python 3.
2. Clone the application repository.
3. Copy `.env.example` to `.env`; enter credentials locally without pasting them into chat.
4. Create the SQLite database from the committed schema.
5. Start the app on `127.0.0.1`.
6. Complete Google OAuth in the browser.
7. Verify the authenticated mailbox owner and the support send-as alias.
8. Run Shopify sync first, then Gmail sync.
9. Compare counts and inspect sample Cases.
10. Test prepare/confirm sending to an internal test address before any customer send.

## Cloudflare deployment

1. Create a D1 database in the preferred jurisdiction.
2. Apply the schema to D1.
3. Bind D1 to the Worker.
4. Add secrets: Google client ID/secret, OAuth encryption key, Shopify credentials, AI key, and optional notification webhook.
5. Add the production OAuth redirect URI in Google Cloud.
6. Configure the Worker route below the protected Hub path.
7. Retain Cloudflare Access allowlisting.
8. Deploy the Worker and static assets.
9. Complete OAuth in production.
10. Run a bounded backfill and monitor progress; do not run one unbounded request.

## Cross-device rule

Do not copy a local `.env`, OAuth token file, or SQLite database through Git. Configure secrets anew on the second computer. If historical data must move, use an explicit encrypted migration approved by the user.

## Rollback

Keep the previous Worker version and database schema compatible until verification completes. A UI rollback must not delete or rewrite D1 data.

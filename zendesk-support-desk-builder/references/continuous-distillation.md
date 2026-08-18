# Continuous distillation

## Source hierarchy

Use this order when project artifacts disagree:

1. Explicit current user requirements.
2. The Obsidian project requirements and acceptance document.
3. Verified behavior in the newest local production source.
4. Existing Skill text.
5. Older implementation notes.

Do not treat chat history alone as verified product behavior. Confirm durable changes in requirements or source code.

## Daily workflow

1. Run `scripts/audit_source.py` against the living project.
2. Compare the manifest with the previous committed manifest.
3. Read only changed source and relevant Obsidian notes.
4. Extract reusable behavior, failure lessons, API contracts, and acceptance tests.
5. Exclude temporary debugging, production IDs, credentials, customer data, database contents, and generated builds.
6. Update Skill instructions or references.
7. Run the official Skill validator and the repository secret scan.
8. Commit only when the Skill actually changed.
9. Push only to the explicitly approved repository and account.
10. Produce a short report containing changed Skill files, validation result, commit hash, and push result.

## Scheduled-task prompt

Use a scheduled Codex task rather than a raw cron job when AI judgment is needed:

```text
Inspect the KryoZon support desk source and its Obsidian requirements document for changes since the last committed Skill manifest. Use $zendesk-support-desk-builder and follow continuous-distillation.md. Update only durable, verified workflows. Never read or publish credential values, customer messages, orders, databases, logs, build output, or Cloudflare resource IDs. Validate and secret-scan the Skill. If there is a meaningful safe change, commit and push it to the approved ddcarolyn Skill repository; otherwise report no change. Never deploy the customer-support application or send email.
```

The task must run in the local Obsidian workspace and requires the intended GitHub account to be active. Keep GitHub push separate from production Cloudflare deployment.

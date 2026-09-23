# Experiment 2 — Private Channel Management

## Objective
Extend the Experiment 1 Telegram bot to administer a real **private test channel**: issue invitations, handle join requests, verify membership, and record membership changes. This is an exploratory lab, not a production admission system.

## Prerequisites
- Experiment 1 bot working, with commands, inline buttons, structured logs, and basic error handling.
- A private Telegram test channel and at least two consenting test accounts.
- Bot token stored in environment variables; never commit credentials.
- Python and the Telegram library already used in Experiment 1.

## Scope and boundaries
**Included:** private-channel administration, bot permissions, invitation lifecycle, join-request processing, membership status, SQLite persistence, and edge-case tests.

**Excluded:** Meta campaigns, campaign attribution, broker integration, affiliate payments, production deployment, and full analytics dashboard.

## M2.1 — Channel setup and permission discovery
**Implementation**
1. Create a private test channel and add the bot as administrator.
2. Grant only permissions needed to create invitation links and manage join requests.
3. Store channel ID in configuration; inspect the bot's actual channel permissions at startup.
4. Add a restricted `/channel_status` admin command to report connectivity and relevant permissions.

**Acceptance**
- Bot can identify the configured channel and confirm required permissions.
- Missing permissions produce an actionable error, not a crash.
- Ordinary users cannot invoke administrator-only actions.

## M2.2 — Invitation lifecycle
**Implementation**
1. Implement an admin-only action to generate a short-lived, single-use invitation link.
2. Persist invitation ID/link metadata, creation time, expiration time, status, and intended test user (if known).
3. Implement expiration and explicit revocation; avoid publishing reusable admin invitations.
4. Test expired, revoked, and forwarded links.

**Acceptance**
- A valid link admits at most its configured member limit.
- Expired and revoked links cannot be reused.
- The bot records which invitation was issued and its current state.

**API distinction:** Telegram join-request links use `creates_join_request=true` and cannot simultaneously specify `member_limit`. Test them separately from single-use links.

## M2.3 — Join requests and controlled approval
**Implementation**
1. Generate a dedicated join-request invitation link.
2. Subscribe to `chat_join_request` updates; confirm the bot has the appropriate administrator permission.
3. Log requester Telegram ID, channel ID, request time, and invite-link metadata when available.
4. Implement explicit admin approval/rejection first; add a configurable automatic-approval mode for recognized test users.
5. Handle already-approved, withdrawn, and duplicate requests idempotently.

**Acceptance**
- A test user requests admission and the bot records the request.
- Authorized approval admits the user; rejection declines the request.
- Duplicate events do not trigger duplicate decisions or crash the bot.

## M2.4 — Membership tracking and persistence
**Implementation**
1. Subscribe to `chat_member` updates for the channel; ensure the bot is an administrator and explicitly requests the necessary update types.
2. Maintain SQLite tables for users, invitations, join requests, membership state, and append-only membership events.
3. Distinguish requested, approved, joined, left, removed, and rejoined states where supported by observed updates.
4. Add an admin-only `/member_status` command using `getChatMember` for targeted verification.
5. Record event timestamps and Telegram update IDs to deduplicate retried updates.

**Acceptance**
- Join, leave, and rejoin events update the current membership record and preserve history.
- A restarted bot retains stored state.
- A targeted membership check agrees with the observed test account's state.

**Limit:** The Bot API does not provide a complete export of all channel subscribers or individual post-view identities. Do not treat membership tracking as full engagement tracking.

## M2.5 — Reliability and edge cases
**Implementation**
1. Test forwarded links, expired links, revoked links, duplicate requests, repeated approvals, users leaving/rejoining, and missing permissions.
2. Restart the bot during a pending request; confirm state is recovered from SQLite.
3. Exercise rate-limit handling and transient API errors with bounded retries and logs.
4. Keep logs minimal; do not expose bot tokens or unnecessary personal data.
5. Write reproducible manual test cases and document Telegram-specific observations.

**Acceptance**
- All expected failures return clear messages and preserve database consistency.
- Duplicate updates are safe; administrator actions are access-controlled.
- README documents setup, permission requirements, test procedure, limitations, and teardown.

## Suggested project extension
```text
telegram-lab/
  bot/
    handlers/
      channel_admin.py
      join_requests.py
      membership.py
    services/
      invitations.py
      membership.py
  storage/
    models.py
    repository.py
  tests/
    test_invitation_service.py
    test_membership_state.py
  .env.example
  README.md
```
Keep existing Experiment 1 modules; adapt names to the actual repository rather than restructuring needlessly.

## End-to-end demonstration
1. Administrator generates a join-request link.
2. Test account A requests to join; the bot records the request.
3. Administrator approves; membership update confirms the join.
4. Account A leaves and rejoins; both events are preserved.
5. Account B attempts an expired or revoked link and cannot enter.
6. Restart the bot and verify the membership history remains available.

## Definition of done
- [ ] M2.1 channel configuration and permission checks pass.
- [ ] M2.2 invitation creation, expiration, and revocation work.
- [ ] M2.3 join requests and controlled admission work.
- [ ] M2.4 membership events persist and survive restart.
- [ ] M2.5 edge cases, authorization, and documentation pass.

## Handoff to IDE agent
Implement **one sub-milestone at a time**. Before each sub-milestone, summarize its API methods and expected Telegram update payloads. After implementation, show the smallest reproducible manual test, report observed results, and stop for approval before continuing. Do not introduce campaign tracking or affiliate logic during this experiment.

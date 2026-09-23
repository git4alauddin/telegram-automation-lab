# Experiment 3 — Campaign Referral Tracking

## Agent handoff

**Goal:** Extend Experiments 1 and 2 with a simulated traffic source and persistent referral attribution. A real Telegram user should be able to follow a campaign-specific bot deep link, start the bot, request admission to the existing private test channel, and be linked to the originating simulated campaign when membership is verified.

**Prerequisites:** Experiment 1 bot commands, callback handlers, structured logging; Experiment 2 private test channel, bot admin permissions, join requests, membership tracking and SQLite persistence. Reuse the existing codebase, conventions and schema; do not rebuild these components.

**Stack:** Python, existing Telegram Bot API library, SQLite, existing bot polling setup. No live Meta credentials, live broker integration, production dashboard or real financial transactions.

## Architectural boundary

The mock traffic source owns mock campaigns, ad sets, ads and referral-link generation. The Telegram module owns deep-link intake, Telegram identity, channel admission and membership events. The attribution module connects campaign tokens to bot starts and verified memberships. Keep the mock source behind a small interface that a future Meta adapter can replace. Never treat simulated ad clicks as verified Meta clicks.

## M3.1 — Mock campaign registry

**Tasks**
- Define campaign, ad-set and ad entities with stable IDs, display names and active/inactive status.
- Seed at least two campaigns with at least two distinguishable ads each.
- Provide a small CLI or local developer command to list campaigns and create a campaign-specific referral link.
- Keep all simulated records explicitly labeled as mock data.

**Acceptance criteria**
- Developer can select a mock ad and retrieve its campaign and ad-set ancestry.
- IDs remain stable after restarting the application.
- An inactive ad cannot generate new referral links unless deliberately reactivated.

## M3.2 — Referral tokens and Telegram deep links

**Tasks**
- Generate opaque, unpredictable, URL-safe referral tokens; store only the mapping to mock campaign/ad identifiers in the database.
- Generate links in the form `https://t.me/<BOT_USERNAME>?start=<TOKEN>` using Telegram's supported deep-link payload constraints (URL-safe characters and maximum payload length).
- Define token expiry, optional single-use policy and explicit invalid/expired states. For this lab, default to reusable campaign tokens and distinguish them from per-visitor tokens.
- Never embed personal information, credentials or untrusted redirect URLs in tokens.

**Acceptance criteria**
- Two ads produce distinguishable referral links.
- Valid links open the correct bot and deliver the token to `/start` after the user presses Start.
- Invalid or expired tokens receive a safe response and cannot create an attributed acquisition.

## M3.3 — Bot intake and attribution policy

**Tasks**
- Parse `/start <TOKEN>` without breaking the existing plain `/start` command.
- Validate the token and associate the Telegram user ID with the corresponding mock campaign, ad set and ad.
- Implement an explicit **first-valid-touch** policy for the initial lab: retain the first valid referral as acquisition source; log later valid touches separately without overwriting the original.
- Ensure repeated `/start` commands are idempotent and do not duplicate user or acquisition records.
- Record event timestamps and event provenance (`simulated_campaign`, `telegram_bot`).

**Acceptance criteria**
- First valid referral persists across restarts.
- Returning users retain original attribution; later touches appear in history.
- A user starting without a token is recorded as unattributed, not assigned to a guessed campaign.

## M3.4 — Connect referrals to private-channel membership

**Tasks**
- Reuse Experiment 2's join-request and membership handlers; do not create a second admission system.
- Associate an invitation or join request with the authenticated Telegram user and their existing referral record.
- Confirm acquisition only after an actual membership update verifies the user joined the private channel.
- Persist separate statuses for `bot_started`, `join_requested`, `approved` and `joined`; approval alone is not proof of joining.
- Handle departure and rejoining without inventing a new acquisition or losing original attribution.

**Acceptance criteria**
- An attributed user can be traced from mock ad to bot start to verified membership.
- A user who starts the bot but never joins remains a bot start, not a channel acquisition.
- A forwarded invite link cannot silently reassign another user's campaign attribution.

## M3.5 — Reliability, inspection and tests

**Tasks**
- Add a developer-only report or CLI query showing mock campaign → bot starts → join requests → verified joins.
- Test repeated deep links, returning users, malformed tokens, expired tokens, inactive ads, duplicate Telegram updates, forwarded invitations and out-of-order membership updates.
- Add database uniqueness constraints and idempotent event handling; avoid double-counting from repeated webhook/polling updates.
- Keep logs free of bot tokens and unnecessary personal data. Document a basic data-retention/deletion procedure for test users.
- Document the difference between simulated referral provenance and independently verified Telegram membership events.

**Acceptance criteria**
- Funnel counts reconcile with stored event records.
- Replaying the same update does not create duplicate acquisitions.
- Restarting the application preserves referral mappings and membership history.
- All existing Experiment 1 and 2 tests continue to pass.

## Suggested data model (adapt to existing schema)

| Entity | Important fields |
|---|---|
| `mock_campaigns` | id, name, status |
| `mock_ad_sets` | id, campaign_id, name |
| `mock_ads` | id, ad_set_id, name, status |
| `referral_tokens` | token, mock_ad_id, created_at, expires_at, status |
| `telegram_users` | telegram_user_id, first_seen_at |
| `referral_touches` | id, telegram_user_id, token, touched_at |
| `acquisitions` | telegram_user_id, first_referral_token, first_attributed_at |
| Existing membership tables | telegram_user_id, channel_id, membership_status, verified_at |
| Existing event log | event_type, source, external_update_id, timestamp |

Use migrations rather than dropping the Experiment 2 database. Do not duplicate existing user, membership or event tables.

## Demo walkthrough

1. Seed Campaign A and Campaign B, each with two ads.
2. Generate a Telegram deep link for Campaign A / Ad 1.
3. Open the link using a real test Telegram account and press Start.
4. Request access to the private channel using the existing bot flow; join the channel.
5. Inspect the database or CLI report: Campaign A / Ad 1 → one bot start → one verified join.
6. Open Campaign B's link with the same user; verify that first-touch attribution remains Campaign A and the new touch is logged.
7. Repeat a Telegram update or restart the bot; verify no duplicate acquisition is created.

## Definition of done

- [ ] Mock campaign registry is persistent and clearly simulated.
- [ ] Campaign-specific bot deep links work.
- [ ] Valid, invalid, expired and absent referral tokens are handled.
- [ ] First-valid-touch attribution and touch history work.
- [ ] Verified channel joins connect to the original referral.
- [ ] Duplicate updates and repeated starts do not inflate counts.
- [ ] Developer report shows campaign-to-join funnel.
- [ ] Tests pass and README includes setup, demo and limitations.

## Explicitly out of scope

Live Meta Marketing API, Meta click verification, broker or CPA integration, affiliate payouts, production analytics UI, ML optimization and financial promotions. These belong to later experiments or the production system.

## Agent execution instruction

Implement milestones sequentially, M3.1 through M3.5. At each milestone, report changed files, test commands, observed results and any deviations from the existing Experiment 1–2 architecture. Preserve working features and request clarification before changing the attribution policy or existing admission behavior.

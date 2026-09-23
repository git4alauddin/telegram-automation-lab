# Experiment 4 — Communication & Engagement

**Project:** Telegram Bot & Channel Lab  
**Status:** Implementation-ready IDE-agent handoff  
**Dependencies:** Experiments 1–3 (bot commands/callbacks, private channel admission, referral attribution)  
**Objective:** Explore and implement reliable bot-mediated communication, scheduled private-channel publishing, offer delivery, and two-way support. Do not build the full business platform in this experiment.

## Scope and constraints

- Reuse the existing bot, Telegram channel, SQLite database, configuration, and referral records. Extend existing code rather than creating a second bot.
- Use real Telegram Bot API interactions and a private **test** channel. Use dummy offers and placeholder URLs; no live broker promotion, deposit collection, trading advice, or real financial claims.
- The bot may initiate private messages only to users who have started it and have not blocked it. Channel post views do not reveal individual viewers; track only observable bot callbacks and redirects.
- Respect Telegram rate limits, privacy requirements, and channel administrator permissions. Do not collect passwords, KYC documents, payment credentials, or unnecessary personal data.
- Use the existing stack. SQLite is sufficient; scheduled jobs may use a lightweight scheduler, with persistent job state in SQLite. No React dashboard or external broker API yet.

## M4.1 — Interactive menus, FAQs and onboarding

**Tasks**
1. Add a compact main menu with inline buttons: `Join Channel`, `Latest Offers`, `FAQ`, and `Contact Support`.
2. Implement menu navigation and callback-query acknowledgement; reuse the existing `/start` referral capture without overwriting first-touch attribution.
3. Add 3–5 test FAQ entries, a back button, and a fallback for unknown or stale callbacks.
4. Show channel access status using existing membership data, rechecking Telegram when appropriate.

**Acceptance tests**
- New and returning users can navigate the menu without duplicate registration.
- All callback queries are acknowledged; invalid callbacks fail gracefully.
- Users cannot accidentally overwrite their stored referral source through menu navigation.

## M4.2 — Channel announcements and scheduled publishing

**Tasks**
1. Add admin-only command or CLI for creating a draft channel announcement.
2. Support immediate publication and scheduling at a specified timezone-aware timestamp.
3. Persist draft/scheduled/sent/failed/cancelled state and Telegram message IDs.
4. Add preview, confirmation, cancel, and safe retry controls; prevent duplicate posting after process restarts.
5. Validate the bot's channel posting permission before publication.

**Acceptance tests**
- Authorized admin can publish a test announcement immediately and schedule another.
- Unauthorized users cannot publish or change scheduled posts.
- Restarting the application does not lose pending jobs or duplicate already-sent messages.
- Missing permissions and API errors produce visible failure records.

## M4.3 — Mock affiliate offers and measurable interactions

**Tasks**
1. Define a mock offer with `offer_id`, title, neutral description, destination placeholder URL, status, and optional expiry.
2. Publish offers to the channel and expose them through the bot's `Latest Offers` menu.
3. Use a backend redirect URL with a signed or random opaque token to log eligible outbound clicks before redirecting to a harmless test destination.
4. Record `offer_id`, source surface (channel/bot), timestamp, and referral/user association **only when technically established**. Channel-link clicks must not be attributed to a specific Telegram member unless the user first identifies themselves through a bot-mediated flow.
5. Expired or disabled offers must not redirect to active promotions.

**Acceptance tests**
- Bot offer interactions can be associated with the known bot user.
- Generic channel-link clicks remain anonymous/aggregate unless identification is explicitly established.
- Invalid, expired, or tampered redirect tokens are rejected safely.
- No simulated click is presented as a broker conversion.

## M4.4 — Two-way support with admin privacy

**Tasks**
1. Add `Contact Support` to start a bot-mediated support thread; persist ticket ID, user ID, status, and timestamps.
2. Forward user messages to an authorized admin through the bot, with ticket reference but without exposing the admin's personal account to the user.
3. Allow admin replies through a restricted bot command or reply workflow, mapping responses to the correct ticket/user.
4. Support ticket closure and basic user-facing status updates.
5. Handle blocked bots, deleted messages, unknown ticket IDs, and duplicate replies.

**Acceptance tests**
- User can open a ticket and receive an admin response through the bot.
- An unrelated user cannot read or reply to another user's ticket.
- Admin identity remains hidden from end users in bot-delivered replies.
- Delivery failure is logged and does not silently mark a reply delivered.

## M4.5 — Engagement controls and reliability

**Tasks**
1. Add explicit opt-in/opt-out preferences for optional direct-message announcements; retain essential service messages separately.
2. Enforce admin authorization, input validation, per-user cooldowns, and conservative broadcast throttling.
3. Add structured logs for sends, callback handling, support events, scheduled jobs, API failures, and retries; redact bot tokens and sensitive payloads.
4. Test application restart, duplicate webhook/update delivery where relevant, blocked users, permission revocation, expired offers, and rate-limit responses.
5. Document Telegram's limits: bots cannot message users before `/start`; channel views are aggregate; external affiliate purchases require broker-side data.

**Acceptance tests**
- Opted-out users receive no optional direct-message announcements.
- Failed sends and rate limits are handled with bounded retry/backoff where safe.
- No duplicate announcements or support replies occur under repeated processing.
- Existing onboarding, membership, and attribution tests from Experiments 1–3 still pass.

## Suggested minimal data additions

- `announcements(id, body, status, scheduled_at, sent_at, telegram_message_id, created_by)`
- `offers(id, title, description, destination_url, status, expires_at)`
- `offer_clicks(id, offer_id, referral_id NULL, telegram_user_id NULL, source_surface, clicked_at)`
- `support_tickets(id, telegram_user_id, status, created_at, closed_at)`
- `support_messages(id, ticket_id, sender_role, telegram_message_id NULL, delivery_status, created_at)`
- `communication_preferences(telegram_user_id, optional_dm_opt_in, updated_at)`

Adapt names and migration style to the existing repository; do not duplicate existing user/referral tables. Minimize retained message content and define retention rules.

## Boundaries

**Included:** Interactive bot menus, FAQ, scheduled test-channel posts, mock offer links, bot-mediated support, consent controls, delivery logs, and reliability tests.  
**Excluded:** Real trading promotions, real broker conversions, personalized investment recommendations, paid subscriptions, advanced analytics dashboards, and Meta API integration. Experiment 5 will develop the event analytics layer; Experiment 6 will add simulated affiliate conversions.

## Definition of Done

- [ ] M4.1 menus and FAQ pass interaction tests.
- [ ] M4.2 immediate and scheduled announcements publish exactly once.
- [ ] M4.3 mock offers work and observable clicks are accurately attributed or explicitly anonymous.
- [ ] M4.4 support messages route correctly with admin access controls.
- [ ] M4.5 opt-out, rate-limit, restart, and error-handling tests pass.
- [ ] Regression tests for Experiments 1–3 pass.
- [ ] README explains setup, required Telegram permissions, test scenarios, and platform limitations.

## IDE-agent execution instructions

1. Inspect the existing repository and implementation of Experiments 1–3. Preserve working interfaces, data, and tests.
2. Implement milestones **sequentially**, M4.1 through M4.5. For each, provide a short implementation summary and demonstrate its acceptance tests before proceeding.
3. Ask for clarification only when an existing architectural choice conflicts with this planner; do not silently replace the current stack.
4. Keep all offers and external destinations simulated. Never insert real financial claims or ask users for deposits.
5. At completion, deliver runnable code, migrations, tests, example environment configuration (without secrets), and a concise limitations report.

# Experiment 5 — Event Tracking & Analytics

**Status:** Implementation handoff  
**Dependencies:** Experiments 1–4  
**Stack:** Python, existing Telegram bot, SQLite, Streamlit (local dashboard)  
**Objective:** Capture and analyze the Telegram funnel using real bot events and simulated acquisition data. Broker conversion and CPA reporting are explicitly deferred to Experiment 6.

## Scope and boundaries

**Included:** unified event contracts; event capture for bot starts, referral attribution, join requests, verified joins, departures, bot interactions and tracked offer-link clicks; durable SQLite storage; idempotent ingestion; aggregate funnel reporting; local dashboard; verification tests.

**Excluded:** live Meta Marketing API, broker API, actual financial transactions, broker CPA approval, automated ad optimization, passive channel view/read tracking and collection of unnecessary personal information.

Reuse existing user, referral, campaign, membership and offer records from Experiments 1–4. Extend their schema through migrations; do not replace or duplicate established functionality. The event log is append-only; derived membership state and dashboard aggregates may be recomputed from authoritative records.

## M5.1 — Unified event contract

**Tasks**
- Inventory existing handlers and records from Experiments 1–4.
- Define event types: `bot_started`, `referral_attributed`, `join_requested`, `join_approved`, `channel_joined`, `channel_left`, `bot_button_clicked`, `offer_link_clicked` and `message_delivery_failed`.
- Define common fields: `event_id`, `event_type`, `occurred_at` (UTC), `received_at` (UTC), `telegram_user_id` (nullable when not known), `campaign_id` (nullable), `referral_token_id` (nullable), `channel_id` (nullable), `source`, `source_event_id` (nullable), and a minimal validated `metadata` object.
- Define source-specific unique keys (e.g. Telegram `update_id` where available) and attribution policy. Preserve the original acquisition source; record later campaign interactions separately.
- Document what each event proves and what it does **not** prove. A bot start is not a channel join; an offer-link click is not a broker purchase.

**Acceptance:** All event types have documented triggers, required fields, validation rules and deduplication keys. Existing schema relationships are mapped without duplication.

## M5.2 — Instrument real bot interactions

**Tasks**
- Add a single event-recording service used by existing bot handlers.
- Record `/start` and referral attribution separately, so a returning user's new start does not silently overwrite their first acquisition.
- Capture join requests, approvals, verified membership transitions and departures using eligible Telegram updates and existing channel-admin permissions.
- Record callback queries for inline buttons; track offer clicks only through bot-controlled redirect endpoints or equivalent instrumented links.
- Do not claim that Telegram exposes individual passive channel post views, or that a button impression proves a click.

**Acceptance:** A test user entering via a mock campaign produces a traceable event sequence from bot start to verified channel join and an instrumented offer click. Missing permissions or events are explicitly surfaced rather than inferred.

## M5.3 — Durable storage and integrity

**Tasks**
- Create an `events` table with indexed timestamps, user IDs, event types and campaign IDs. Store minimal metadata; protect bot tokens and avoid logging unnecessary message bodies.
- Apply SQLite migrations; use transactions and uniqueness constraints for idempotent writes.
- Handle repeated Telegram updates, delayed/out-of-order updates and application restarts without duplicate funnel counts.
- Maintain separate current membership state and immutable historical events. Treat a user leaving and rejoining as distinct transitions without counting them as two unique acquired users.
- Add explicit test-data labeling and a retention/deletion procedure appropriate for the lab.

**Acceptance:** Replaying the same Telegram update does not duplicate an event; restarting the application retains history; out-of-order events do not corrupt current membership state.

## M5.4 — Local analytics dashboard

**Tasks**
- Build a small Streamlit dashboard using read-only queries or a dedicated analytics service.
- Display bot starts, unique attributed users, join requests, verified unique joins, current members, departures, rejoin counts, bot button clicks and instrumented offer-link clicks.
- Show campaign-level funnel breakdowns and conversion rates with clearly stated denominators.
- Add date filters and a single-user event timeline using internal pseudonymous IDs; keep sensitive Telegram identifiers out of public-facing views.
- Distinguish `simulated` campaign records from `real` Telegram events. Do not display broker conversions, deposits or commissions as measured outcomes in this experiment.

**Acceptance:** Dashboard totals reconcile with source event queries, date filters behave consistently, and one test user's event timeline matches their observed interactions.

## M5.5 — Verification, recovery and documentation

**Test scenarios**
1. New user follows a mock campaign link, starts bot, requests access, joins channel and clicks an instrumented offer link.
2. Same user starts bot again; first-touch attribution and unique acquisition count remain stable.
3. Duplicate and delayed Telegram updates do not inflate event or funnel totals.
4. User leaves and rejoins; current membership and historical transition counts are correct.
5. Invalid referral token, missing campaign metadata, blocked bot and insufficient channel permissions produce explicit, non-crashing outcomes.
6. Application restarts; stored events and dashboard aggregates remain consistent.
7. Dashboard date boundaries use UTC consistently; local display timezone is clearly labeled.

**Acceptance:** Automated tests pass for event validation, idempotency, attribution and aggregate calculations. Manual test results are recorded with observed Telegram behavior and known limitations.

## Suggested project additions

```text
app/
  analytics/
    event_contracts.py
    event_recorder.py
    aggregates.py
  db/
    migrations/
  dashboard/
    streamlit_app.py
tests/
  test_event_contracts.py
  test_event_idempotency.py
  test_attribution.py
  test_analytics.py
docs/
  experiment-05-test-results.md
  telegram-event-capability-matrix.md
```

Adapt these paths to the existing repository; do not reorganize Experiments 1–4 unnecessarily.

## Definition of Done

- [ ] Unified event schema documented and migrated.
- [ ] Existing bot and channel handlers instrumented without regressions.
- [ ] Repeated and out-of-order updates handled safely.
- [ ] Historical events and current membership state remain distinct.
- [ ] Streamlit dashboard reports verified Telegram funnel metrics.
- [ ] Campaign data is clearly labeled simulated.
- [ ] Manual end-to-end test and automated integrity tests pass.
- [ ] Capability matrix documents Telegram's measurable and unmeasurable actions.

## IDE agent handoff

Implement **Experiment 5 only** on top of the existing codebase. Inspect Experiments 1–4 before making schema or handler changes. Work milestone by milestone, demonstrate the acceptance test for each, and record deviations. Do not implement live Meta APIs, broker integrations or financial-event simulation here. End with a functioning local analytics dashboard and a reproducible test report.

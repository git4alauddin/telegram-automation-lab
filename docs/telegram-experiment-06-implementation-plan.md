# Experiment 6 — Mock Affiliate Platform Integration

**Status:** Implementation handoff  
**Depends on:** Experiments 1–5  
**Stack:** Python, FastAPI, SQLite, existing Telegram bot and analytics dashboard  
**Purpose:** Validate an end-to-end simulated campaign → real Telegram membership → simulated affiliate conversion workflow.

## Objective

Build a separate mock affiliate platform and integrate it with the existing Telegram system. Simulate broker registrations, deposits, qualifying actions, CPA approvals/rejections, and commissions. Preserve clear separation between **real Telegram events** and **simulated financial events**. Do not connect to a live broker, process real deposits, or imply that a simulated conversion is genuine.

## Scope and boundaries

**In scope:** Mock broker API, referral/click identifiers, simulated registration and qualification, authenticated conversion webhooks, idempotent ingestion, commission ledger, analytics integration, and end-to-end testing.

**Out of scope:** Live broker integrations, real money movement, KYC collection, real trading, investment recommendations, Meta API integration, and production deployment.

**Reuse:** Existing campaign/referral attribution, Telegram identity and membership records, tracked links, event schema, and dashboard from Experiments 1–5. Avoid reimplementing their ownership or changing their established contracts without documenting a migration.

## M6.1 — Mock affiliate platform

### Tasks
- Implement a separate mock broker service (FastAPI app or isolated module with a clear API boundary).
- Provide endpoints for simulated referral visits and registrations, plus an administrator-only simulation interface for deposit and qualification events.
- Assign stable mock broker customer IDs and retain the incoming affiliate tracking identifier (`sub_id`).
- Define configurable mock CPA terms: qualifying action, commission amount/currency, approval delay, and rejection reason.
- Label all mock API responses and records `simulation=true`.

### Acceptance criteria
- A valid tracked referral can create a simulated broker customer with a unique ID.
- The broker stores the tracking identifier without receiving or needing a Telegram user ID.
- Invalid or repeated registration requests return predictable, documented results.
- No endpoint performs real financial operations.

## M6.2 — Tracked affiliate links and registration attribution

### Tasks
- Reuse the tracked-link redirect mechanism from Experiment 4; generate an opaque affiliate click/sub-ID mapped to the internal referral record.
- Route test affiliate links to the mock broker registration page or endpoint.
- Persist click timestamp, offer ID, affiliate click ID, campaign/referral mapping, and mock broker customer ID when registered.
- Define a first-version attribution policy (e.g., last valid tracked affiliate click before registration) and document its limitations.
- Keep Telegram identifiers out of publicly exposed links and broker-facing identifiers.

### Acceptance criteria
- A test member clicks an offer and registers at the mock broker; the registration is associated with the correct internal referral.
- Different members/campaigns remain distinguishable.
- Repeated clicks and direct registrations behave according to the documented attribution policy.
- Unattributed registrations are recorded as unattributed rather than guessed.

## M6.3 — Simulated conversion and CPA lifecycle

### Tasks
- Define lifecycle states: `registered`, `deposit_simulated`, `qualification_pending`, `approved`, `rejected`, and `reversed`.
- Simulate first-deposit and other qualifying events according to configurable mock CPA terms.
- Emit mock broker events with unique event IDs, customer IDs, timestamps, status, commission amount/currency where relevant, and `simulation=true`.
- Implement state-transition validation; reject impossible transitions and record legitimate reversals as new ledger entries rather than silently overwriting history.
- Distinguish pending, approved, rejected, reversed, and paid commissions; do not equate approval with actual payment.

### Acceptance criteria
- A simulated qualifying customer progresses through pending → approved or rejected.
- Rejected events do not increase approved commission totals.
- A reversal corrects net commission totals while preserving the original approval event.
- All lifecycle transitions are auditable.

## M6.4 — Secure integration and dashboard

### Tasks
- Expose an authenticated conversion webhook on the Telegram/backend side. Verify a shared-secret HMAC signature (or equivalent agreed mechanism) over the raw payload, and reject invalid signatures.
- Validate payload schema and timestamps; use unique external event IDs for idempotency and safely handle out-of-order events.
- Store raw sanitized event metadata plus normalized affiliate events; do not store unnecessary sensitive financial/customer information.
- Join affiliate events to existing campaign → referral → Telegram membership records via internal mappings, not guessed identity matches.
- Extend the Experiment 5 dashboard with registrations, simulated deposits, pending/approved/rejected CPAs, gross and net simulated commissions, cost per approved acquisition (when simulated spend exists), and funnel drop-offs.
- Clearly label every mock conversion and revenue metric **SIMULATED**.

### Acceptance criteria
- A valid event updates the correct referral and dashboard exactly once, even if delivered repeatedly.
- Invalid signatures and malformed payloads are rejected and logged safely.
- Dashboard totals reconcile with the underlying event/commission ledger.
- Missing attribution or currency mismatch is visible rather than silently combined.

## M6.5 — End-to-end testing and handoff

### Test scenarios
1. Mock campaign generates a referral → real user starts the bot → joins the private channel → clicks a tracked affiliate link → registers at mock broker → completes simulated qualification → mock broker approves CPA → dashboard shows the complete chain.
2. Two users from different mock campaigns register; attribution and commissions remain separate.
3. Duplicate registration or webhook delivery does not duplicate customers or commissions.
4. Rejected and reversed CPAs produce accurate net totals.
5. Missing, expired, tampered, or unattributed referral identifiers fail safely or remain unattributed.
6. Webhook signature failure, delayed delivery, out-of-order events, and temporary backend downtime are handled without silently losing valid events.
7. A user leaves or rejoins the channel; historical attribution and broker event records remain consistent.
8. Restart services and reconcile the dashboard with stored events.

### Acceptance criteria
- All eight scenarios pass with reproducible test fixtures.
- Automated tests cover API contracts, signature validation, idempotency, lifecycle transitions, attribution, and metric calculations.
- A README documents startup, environment variables, simulated event generation, test commands, known limitations, and replacement points for a future real broker integration.

## Suggested project additions

```text
mock_affiliate/
  app.py                 # isolated mock broker API
  models.py              # simulated customers and CPA states
  simulator.py           # admin-controlled event generation
  webhook_sender.py      # signed event delivery and retries
backend/
  affiliate/
    routes.py            # authenticated conversion webhook
    schemas.py           # validated external event contracts
    service.py           # attribution and lifecycle processing
    repository.py        # persistence and idempotency
  analytics/             # extend existing Experiment 5 views
tests/
  test_mock_affiliate.py
  test_webhook_security.py
  test_attribution.py
  test_commission_ledger.py
  test_end_to_end.py
```

Adapt these paths to the existing repository rather than duplicating established modules.

## Definition of done

- [ ] M6.1 mock broker is isolated and functional.
- [ ] M6.2 tracked clicks and registrations resolve to correct referrals.
- [ ] M6.3 qualification, approval, rejection, and reversal lifecycle works.
- [ ] M6.4 authenticated, idempotent webhook integration and dashboard work.
- [ ] M6.5 all end-to-end and failure-path tests pass.
- [ ] Simulated data is clearly labeled and segregated from future production data.
- [ ] API contracts, environment setup, limitations, and migration seams are documented.

## IDE-agent handoff

Implement **Experiment 6 only**, on top of the completed Experiments 1–5. First inspect the existing repository, identify reusable event, referral, link, and dashboard interfaces, and briefly document integration points. Then implement M6.1 through M6.5 sequentially, demonstrating each milestone's acceptance criteria before proceeding. Do not integrate a live broker, process real payments, fabricate real conversion evidence, or introduce investment advice. Keep the mock affiliate adapter replaceable and ensure all mock events and financial figures are explicitly marked as simulated.

# Telegram Automation Lab — Project Workflow

**Status:** Final implementation workflow  
**Purpose:** Build the six planned Telegram Automation Lab experiments through guided, hands-on implementation, one verified task at a time.  
**Authority:** This file governs *how* work is executed. Each experiment's implementation planner governs *what* is built, its scope, acceptance criteria and boundaries. If a workflow instruction conflicts with an experiment-specific technical requirement, surface the conflict and ask before changing scope.

## 1. Project objective

Build a real Telegram bot and private-channel workflow around simulated advertising and affiliate systems. Progressively add channel membership, campaign attribution, communication, event analytics and mock CPA conversion reporting. Keep simulated components replaceable; do not claim that simulated traffic, deposits or broker conversions are real.

| Experiment | Planner | Main deliverable |
|---|---|---|
| 1 — Bot Fundamentals | `telegram-experiment-01-implementation-plan.md` | Commands, inline buttons, sanitized logging and reliable polling |
| 2 — Private Channel Management | `telegram-experiment-02-implementation-plan.md` | Admin permissions, invite lifecycle, join requests and membership tracking |
| 3 — Campaign Referral Tracking | `telegram-experiment-03-implementation-plan.md` | Mock campaigns, referral deep links and membership attribution |
| 4 — Communication & Engagement | `telegram-experiment-04-implementation-plan.md` | Menus, scheduled announcements, tracked mock offers and private support |
| 5 — Event Tracking & Analytics | `telegram-experiment-05-implementation-plan.md` | Durable event records, acquisition funnel and local dashboard |
| 6 — Mock Affiliate Platform Integration | `telegram-experiment-06-implementation-plan.md` | Mock registrations, deposits, CPA lifecycle, secure integration and end-to-end test |

Complete experiments in order unless the student explicitly changes priorities. Reuse verified code and schemas; do not reimplement earlier experiments.

## 2. Working rhythm

```text
Read the current experiment planner and identify its next unfinished milestone
    ↓
Break that milestone into small, independently verifiable features
    ↓
Explain ONE feature: purpose, rough flow, files and first small step
    ↓
Student writes/runs the code; agent guides and answers questions
    ↓
Agent verifies behavior, tests, diff and project status
    ↓
Agent reviews useful comments and readability
    ↓
Student commits and pushes using explicit file paths
    ↓
Agent updates the current milestone's implementation log
    ↓
Proceed only after the feature is verified or its blocker understood
```

**Never dump an entire milestone's code or proceed to the next feature merely because code was suggested.** If a feature is large, teach it in small internal steps, then verify and commit the completed feature as one unit.

## 3. Execution ownership

Default mode is **guidance-first**. The student writes code, installs packages, runs servers, executes commands, and commits/pushes. The agent may read files, inspect diffs, review code, check status, explain, debug and suggest verification commands. The agent must not scaffold, install, start long-running processes, edit implementation files, move/delete files or commit unless the student explicitly delegates that action (for example, “do it,” “run it,” “install it,” “add the test,” or “update the file”).

When the student says a step is done, inspect the changed files and evidence before issuing a commit block. If verification is run locally, ask for the relevant command output. Do not assume success.

## 4. Naming and progress tracking

Use the experiment number as the milestone prefix and the feature number within that experiment:

```text
m1.f1.bot_setup
m2.f1.channel_admin_permissions
m3.f2.referral_deep_links
m4.f3.tracked_mock_offers
m5.f1.event_contract
m6.f3.mock_cpa_lifecycle
```

These are examples, not an imposed feature decomposition. Derive the actual feature list from the current experiment planner before implementation. **The feature ID and name are the Git commit title.** Keep the same ID in the implementation log and progress tracker. For multi-step features, retain one feature ID and commit after all acceptance checks pass.

Suggested progress markers: `not started`, `in progress`, `blocked`, `verified`, `committed`. Do not mark a feature complete solely because files exist.

## 5. Format for proposing the next task

The agent should present only the next actionable feature:

```markdown
## m2.f1.channel_admin_permissions

**What and why:** Configure the bot's minimum permissions for the private test channel.

**Rough flow:**
Create or identify private test channel → add bot as administrator → inspect
its actual privileges → verify the bot can perform the planned channel action.

**Files to inspect or touch:**
- [Exact paths after inspecting the current repo]

**First step:**
[One small, concrete action for the student]

**Verification:**
[Observable result and command/manual check]
```

Give code only for the current small step. Explain unfamiliar Telegram Bot API, Python, async, database, FastAPI or testing concepts briefly when first used. Wait for implementation and verification before proceeding.

## 6. Source of truth and scope control

1. Read this workflow and the **current experiment planner** before proposing work.
2. Inspect the actual repository, current implementation log, Git status and relevant files; do not assume a suggested file structure has already been created.
3. Follow the current planner's milestone order, prerequisites, acceptance criteria, explicit exclusions and handoff instructions.
4. Earlier experiments remain the implementation baseline. Preserve existing contracts unless an approved change is necessary.
5. If a planner leaves a decision open (e.g., attribution policy, scheduler choice or schema migration), present the options and ask for a decision before implementing.
6. Do not silently add real Meta API integration, live broker connections, real deposits or financial transactions to these simulation experiments.
7. When a milestone is finished, run its full definition-of-done checks before advancing to the next milestone or experiment.

## 7. Code guidance and comments

- Use small, runnable code chunks tied to the current step, not a full project dump.
- Prefer readable, minimal implementations over speculative abstractions.
- Keep API credentials and bot tokens in environment variables; never commit secrets, real user data dumps or sensitive logs.
- Comment the purpose of handlers, services, schemas and important business rules. Do not comment obvious Python syntax or narrate every line.
- Review comments and readability **after functional verification and before committing**.
- Preserve the distinction between simulated campaign/affiliate data and observed Telegram events in names, schemas, dashboards and documentation.

## 8. Verification standard

Verify each meaningful step using evidence appropriate to the feature:

- Inspect changed files, configuration, dependency changes and `git status --short`.
- Run relevant tests and static checks when available; inspect actual output.
- For Telegram behavior, verify against the real test bot/channel when the planner calls for it, using test accounts where needed.
- For persistence, verify database records and expected behavior after restart.
- For callbacks, webhooks and mock integrations, test invalid payloads, duplicate deliveries, unauthorized requests and retries where relevant.
- For analytics, reconcile event counts and attribution against a controlled test journey; do not assume the dashboard is correct because it renders.
- For external API capabilities or changed library behavior, consult current official documentation before asserting support.

Never claim to have run a test, observed a Telegram event or verified a live integration without actual evidence. When blocked, record the exact failure, likely cause and next diagnostic step.

### Milestone-level acceptance

At the end of each milestone, check **every acceptance criterion in its experiment planner**. At the end of an experiment, run its end-to-end demonstration and definition of done. The next experiment starts only after the student approves the handoff.

## 9. Git and commit policy

Commit every completed, verified feature. Before proposing a commit:

1. Ensure the feature is complete, the project is not knowingly broken and the relevant checks passed.
2. Review the diff and readability; keep unrelated edits out of the commit.
3. Inspect `git status --short` and stage **only explicit, reviewed paths**.
4. Supply a PowerShell-compatible commit block without unnecessary directory changes.

```powershell
git add app/handlers.py tests/test_handlers.py
git commit -m "m1.f2.commands_and_messages"
git push
```

Paths and title above are illustrative; replace them with the **actual verified changed files and current feature ID**. Never use `git add .` or automatically commit/push without explicit delegation. The student executes the block by default and shares the commit hash for the log.

## 10. Implementation logs

Keep planning docs and implementation logs outside the application code when practical. Suggested layout (adapt to the existing repository rather than moving files automatically):

```text
telegram-automation-lab/
├── docs/
│   ├── TELEGRAM_PROJECT_WORKFLOW.md
│   ├── planners/
│   │   ├── telegram-experiment-01-implementation-plan.md
│   │   ├── ...
│   │   └── telegram-experiment-06-implementation-plan.md
│   └── implementation-log/
│       ├── m1-implementation-log.md
│       ├── ...
│       └── m6-implementation-log.md
└── [existing application code; preserve actual structure]
```

After each successful commit, the agent updates the corresponding milestone log. Include:

```markdown
## mX.fY.feature_name

**Status:** Committed
**Commit:** <actual commit hash>
**What we built:** [Concrete changes]
**Why this was needed:** [Purpose in the Telegram funnel]
**Concepts learned:** [Short explanation of new concepts]
**Technology notes:** [New APIs/libraries/patterns and why they matter]
**Code meaning:** [Small significant snippet, if helpful, with explanation]
**Files changed:** [Exact paths]
**Verification:** [Tests/manual steps actually performed and results]
**How to confirm later:** [Short reproducible check]
**Open issues:** [None or explicit follow-up]
```

The log is a learning resource, not merely a checklist. If the student has not yet committed, record the verified status but leave the commit hash pending; do not invent it.

## 11. Telegram-specific operational rules

- Use a test bot and private test channel during the lab. Grant only required admin permissions and check them before operations.
- Distinguish a user starting the bot, requesting access, receiving approval and **actually becoming a channel member**; do not count these as the same event.
- Treat referral tokens and affiliate callbacks as untrusted input; validate them and define duplicate-handling behavior.
- Preserve privacy in logs and support messages; avoid exposing admin identities or bot tokens.
- Keep bot commands, invite-link creation, join approvals and support actions consistent with the current experiment's authorized scope.
- Record observed Telegram events separately from mock campaigns and mock broker conversions. Broker registration or deposit cannot be verified from Telegram membership alone.
- Before any future live Meta or broker integration, separately review API permissions, attribution limitations, applicable financial-advertising rules and data-handling obligations.

## 12. Agent and student responsibilities

**Agent:** Guide one feature at a time; give precise file paths after inspection; explain unfamiliar concepts; review evidence; debug failures; check tests and Git diff; suggest explicit-path commit blocks; update the log after the commit; respect current planner boundaries and the student's execution ownership.

**Student:** Implement and run the guided step; ask questions as needed; share failures and test output; approve significant design changes; execute the verified commit block unless delegating; confirm before moving to the next feature or experiment.

## 13. Completion criteria for the full lab

The lab is complete when all six experiment planners have passed their definitions of done and a documented end-to-end demo shows:

```text
Simulated campaign
  → tracked Telegram deep link
  → real bot start
  → private-channel request and verified membership
  → engagement and tracked mock offer click
  → mock affiliate registration / qualifying action
  → mock CPA approval or rejection
  → persisted events and reconciled analytics dashboard
```

Record what was real versus simulated, demonstrate duplicate/retry handling and security checks, retain milestone logs and provide setup instructions. Do not describe the result as a live Meta-to-broker production integration unless those separate integrations have actually been built and verified.

---

**First instruction to the IDE agent:** Read this workflow and Experiment 1's planner, inspect the existing repository and implementation log, identify the first unfinished feature, and propose **only its first small step**. Do not install, edit, run or commit anything until the student asks.

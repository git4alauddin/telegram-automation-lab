# Agent Handoff

Use this file as the resume entry point for the Telegram Automation Lab. It should stay durable and process-focused. Detailed feature history belongs in the implementation logs.

## Resume Protocol

Before proposing or changing anything:

1. Run `git status --short` and inspect the latest commits with `git log --oneline -5`.
2. Read `docs/TELEGRAM_PROJECT_WORKFLOW.md`.
3. Read the planner for the current experiment.
4. Read the matching implementation log.
5. Inspect the current code before assuming file shape or behavior.

The workflow controls how work is done. The active experiment planner controls what is in scope. The implementation log records what has already been verified.

## Working Contract

- Work guidance-first by default.
- Propose one small, independently verifiable step at a time.
- Let the student write/run code unless they explicitly delegate a file edit.
- Do not run `git add`, `git commit`, or `git push` from the agent side.
- After verification, give the student a PowerShell commit block with explicit reviewed paths.
- Never use `git add .`.
- Keep implementation logs updated as part of normal feature work.
- It is acceptable for a just-finished feature to say `Commit: Pending`; fill the real hash during a later normal documentation/code update.
- Do not expose, print, or read the bot token. Do not inspect `.env` unless the student explicitly asks for a private local check, and never paste its contents.

## Current Checkpoint

Experiment 1 is complete.

Latest verified Experiment 1 features are recorded in:

- `docs/implementation-log/m1-implementation-log.md`

The next planned work is Experiment 2:

- Planner: `docs/telegram-experiment-02-implementation-plan.md`
- Topic: private channel management
- Expected first action: read the Experiment 2 planner, inspect current code/logs, then propose only the first small setup step.

Refresh this checkpoint from Git and the logs before acting. Do not rely on this file alone if the repository has moved on.

## Stable Project Context

- Project root: `C:\Users\alaud\OneDrive\Desktop\telegram_proj`
- GitHub remote: `https://github.com/git4alauddin/telegram-automation-lab.git`
- Main branch: `main`
- Test bot username: `@alaud_campaign_bot`
- Runtime style: local Python app using Telegram long polling
- Token source: local `.env` with `TELEGRAM_BOT_TOKEN`, ignored by Git
- Python environment: `.venv`

## Code Orientation

Start code inspection with:

- `app/main.py`
- `app/handlers.py`
- `app/logging_config.py`

As of Experiment 1 completion, the app has:

- secure token loading from `.env`
- long polling startup
- `/start` and `/help`
- unknown command fallback
- ordinary text handling
- inline menu callbacks
- application error handler
- sanitized structured logs using `event=` and `outcome=`

Verify the live code before relying on this list.

## Feature Loop

For every feature:

1. Identify the next unfinished planner requirement.
2. Explain one small feature: purpose, rough flow, files, and first step.
3. Let the student implement unless they delegate the edit.
4. Inspect changed files and relevant diffs.
5. Verify behavior with the right evidence.
6. Update README/logs when behavior or setup changes.
7. Provide an explicit-path commit block for the student.

Do not move to the next feature just because code exists. Move only after behavior is verified or the blocker is understood.

## Verification Rules

- Use `git status --short` before and after meaningful work.
- Use `git diff` to review exactly what changed.
- Run syntax/tests when appropriate.
- For behavior changes, run the bot locally and verify in Telegram when the planner calls for real Telegram behavior.
- Confirm `.env`, `.venv`, `.idea`, cache files, and tokens are not committed.
- Never claim a live Telegram behavior was verified unless it was actually observed.

## Scope Boundaries

- Preserve completed experiment behavior unless an approved change is necessary.
- Keep simulated campaign, offer, and affiliate concepts clearly simulated.
- Do not add referral attribution, database analytics, affiliate integration, deployment, real Meta integration, broker integration, real deposits, or financial transactions unless the active planner explicitly calls for it.
- When moving between experiments, ask the student before starting the next experiment's implementation work.

## Updating This File

Update this handoff only for durable resume guidance:

- current experiment checkpoint
- major source-of-truth path changes
- collaboration rules
- stable project context

Do not duplicate full implementation history here. Put feature details, commit hashes, verification evidence, and open issues in the relevant implementation log.

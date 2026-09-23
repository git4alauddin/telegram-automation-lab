# Agent Handoff

This file is the resume entry point for future agents working on the Telegram Automation Lab.

## Read first

1. `docs/TELEGRAM_PROJECT_WORKFLOW.md`
2. `docs/telegram-experiment-01-implementation-plan.md`
3. `docs/implementation-log/m1-implementation-log.md`
4. Current code in `app/main.py`, `app/handlers.py`, and `app/logging_config.py`

The workflow file controls how work is done. The experiment planner controls what is in scope.

## Working method

- Work guidance-first by default.
- Propose one small, independently verifiable step at a time.
- Let the student write/run code unless they explicitly delegate a file edit.
- Do not run `git add`, `git commit`, or `git push` from the agent side.
- After verification, provide an explicit PowerShell commit block with reviewed file paths.
- Never use `git add .`.
- Keep implementation logs updated, but it is acceptable for a just-finished feature to say `Commit: Pending`; the actual hash can be filled during a later normal documentation/code update.
- Do not expose or print the bot token. Do not read `.env` unless the student explicitly asks for a private local check, and never paste its contents.

## Current repository state

- Project path: `C:\Users\alaud\OneDrive\Desktop\telegram_proj`
- GitHub remote: `https://github.com/git4alauddin/telegram-automation-lab.git`
- Branch: `main`
- Test bot username: `@alaud_campaign_bot`
- Runtime style: local Python app using Telegram long polling
- Token source: local `.env` with `TELEGRAM_BOT_TOKEN`, ignored by Git
- Python environment: `.venv`

## Completed work

### m1.f1.bot_setup

Committed as `1f93501`.

Built the minimal project structure, safe token loading, pinned dependencies, logging setup, long polling startup, and `/start` handler. Verified valid startup, `/start`, and missing-token failure without leaking secrets.

### m1.f2.commands_and_messages

Committed as `6eaf971`.

Added `/help`, ordinary text handling, and sanitized logs for command/text updates. Verified `/start`, `/help`, and ordinary text responses.

### m1.f3.interactive_buttons

Latest commit observed: `8a94f55 m1.f3.interactive_buttons`.

Added inline buttons to `/start`, callback-query routing for:

- `menu:about`
- `menu:offer`
- `menu:back`

Verified that About lab and Mock offer open detail views, Back returns to the main menu, and callback loading clears.

Note: `docs/implementation-log/m1-implementation-log.md` may still show `Commit: Pending` for `m1.f3`; update that later as part of a normal work commit if desired.

## Current code shape

- `app/main.py`
  - Loads `.env`
  - Builds the Telegram application
  - Registers:
    - `/start`
    - `/help`
    - callback handler for `^menu:`
    - normal text handler
  - Runs long polling

- `app/handlers.py`
  - `build_main_menu()`
  - `build_back_menu()`
  - `start()`
  - `help_command()`
  - `echo_text()`
  - `handle_menu_callback()`

- `app/logging_config.py`
  - Basic `logging.basicConfig(...)` setup

## Next feature

Next planned feature: `m1.f4.event_inspection`.

Purpose: improve logs so startup, commands, ordinary messages, callbacks, and handler outcomes are easier to recognize and remain safe.

Planner source: Milestone 1.4 in `docs/telegram-experiment-01-implementation-plan.md`.

Expected scope:

- Add structured logs for startup, commands, messages, callbacks, and handler errors.
- Include timestamp, event type, update ID, relevant Telegram IDs, and handler outcome.
- Continue avoiding token values, message text, and unnecessary personal data.

Suggested first small step:

Inspect existing logging in `app/handlers.py` and introduce a small helper for safe Telegram IDs or event logging, without changing bot behavior yet.

## Verification style

For each feature:

- Inspect changed files.
- Run the bot locally when behavior changes.
- Verify behavior in Telegram with the test bot.
- Check `git diff` and `git status --short`.
- Update `README.md` and `docs/implementation-log/m1-implementation-log.md` when the verified behavior changes.
- Give the student a commit block with explicit paths.

## Important boundaries

- Do not add private-channel management during Experiment 1.
- Do not add referral attribution, database, FastAPI, webhooks, analytics dashboard, deployment, real Meta integration, broker integration, real deposits, or financial transactions during Experiment 1.
- Keep simulated offer language clearly simulated.

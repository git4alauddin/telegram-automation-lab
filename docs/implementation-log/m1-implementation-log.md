# Experiment 1 Implementation Log

## m1.f1.bot_setup

**Status:** Committed
**Commit:** `1f93501`

**What we built:** A minimal local Telegram bot project with secure token configuration, pinned dependencies, basic logging, long polling, and a working `/start` command.

**Why this was needed:** This is the foundation for the Telegram Automation Lab. Later experiments will reuse the bot startup, handler layout, logging pattern, and secure configuration approach.

**Concepts learned:** A Telegram bot is created through BotFather, but the token must stay private. The local app reads the token from `.env`, starts long polling, and responds to Telegram updates through async handlers.

**Technology notes:** The project uses `python-telegram-bot` for Telegram Bot API access and `python-dotenv` for local environment loading. Long polling keeps asking Telegram for updates, which is why repeated POST activity appears while the bot is running.

**Code meaning:** `app/main.py` loads `TELEGRAM_BOT_TOKEN`, builds the Telegram application, registers `CommandHandler("start", start)`, and starts polling. `app/handlers.py` logs sanitized Telegram IDs and sends the `/start` reply.

**Files changed:**
- `.env.example`
- `.gitignore`
- `README.md`
- `requirements.txt`
- `app/__init__.py`
- `app/handlers.py`
- `app/logging_config.py`
- `app/main.py`
- `docs/TELEGRAM_PROJECT_WORKFLOW.md`
- `docs/telegram-experiment-01-implementation-plan.md`
- `docs/telegram-experiment-02-implementation-plan.md`
- `docs/telegram-experiment-03-implementation-plan.md`
- `docs/telegram-experiment-04-implementation-plan.md`
- `docs/telegram-experiment-05-implementation-plan.md`
- `docs/telegram-experiment-06-implementation-plan.md`

**Verification:** The bot started locally with long polling, `/start` replied successfully in Telegram, sanitized startup and handler logs appeared, and the missing-token path raised `RuntimeError: TELEGRAM_BOT_TOKEN is missing. Add it to your local .env file.` without printing the token. Git status was clean after commit, branch was `main`, and the GitHub remote was configured.

**How to confirm later:** Activate the virtual environment, run `python -m app.main`, send `/start` to `@alaud_campaign_bot`, and confirm the reply plus sanitized console log.

**Open issues:** None for this feature. Milestone 1.1 can continue with any remaining setup/readability checks before moving to commands and messages.

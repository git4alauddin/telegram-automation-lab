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

## m1.f2.commands_and_messages

**Status:** Committed
**Commit:** `6eaf971`

**What we built:** Added a `/help` command with a distinct command-list reply and a normal text-message handler that responds separately from slash commands.

**Why this was needed:** The bot now has the basic command and message behavior required for Experiment 1. This separates command handling from ordinary user conversation before we add interactive buttons.

**Concepts learned:** `CommandHandler` routes slash commands like `/start` and `/help`. `MessageHandler(filters.TEXT & ~filters.COMMAND, echo_text)` catches ordinary text while excluding slash commands, so each kind of update can have its own response and log event.

**Technology notes:** The bot still uses long polling. Handler logs remain sanitized by recording update ID, user ID, chat ID, and message ID where available, without logging token values or message text.

**Code meaning:** `app/handlers.py` now contains `help_command` and `echo_text`. `app/main.py` imports those handlers and registers `/help` plus the text-message filter after the `/start` handler.

**Files changed:**
- `README.md`
- `app/handlers.py`
- `app/main.py`

**Verification:** The bot was run locally. `/start` returned the original connected message, `/help` returned the command list, and ordinary text returned the safe basic response. Console logs showed command and text event types with Telegram IDs only.

**How to confirm later:** Run `python -m app.main`, send `/start`, `/help`, and an ordinary text message to `@alaud_campaign_bot`, then confirm each receives the expected reply and logs do not include message text.

**Open issues:** None for this feature.

## m1.f3.interactive_buttons

**Status:** Committed
**Commit:** `8a94f55`

**What we built:** Added an inline menu to `/start` with About lab and Mock offer actions, plus a Back action for returning to the main menu.

**Why this was needed:** Experiment 1 requires interactive buttons and callback-query routing. This gives the bot a small menu flow before later experiments add richer engagement and offer tracking.

**Concepts learned:** Inline buttons display user-facing labels but send private `callback_data` values back to the bot. `CallbackQueryHandler` routes those button taps, and `await query.answer()` clears Telegram's loading indicator.

**Technology notes:** Callback data is filtered with the `^menu:` pattern in `app/main.py`. The callback handler edits the existing message instead of sending a new message, keeping the menu interaction tidy.

**Code meaning:** `build_main_menu()` creates the two main buttons, `build_back_menu()` creates the Back button, and `handle_menu_callback()` routes `menu:about`, `menu:offer`, and `menu:back`.

**Files changed:**
- `README.md`
- `app/handlers.py`
- `app/main.py`
- `docs/implementation-log/m1-implementation-log.md`

**Verification:** The bot was run locally. `/start` displayed About lab and Mock offer buttons. About lab and Mock offer each opened the intended detail view with a Back button. Back returned to the main menu. Console logs showed callback events with the expected callback data values.

**How to confirm later:** Run `python -m app.main`, send `/start` to `@alaud_campaign_bot`, tap About lab, Back, Mock offer, and Back, then confirm the message updates and button loading clears each time.

**Open issues:** None for this feature.

## m1.f4.event_inspection

**Status:** Committed
**Commit:** `d3dd5ed`

**What we built:** Standardized bot logs around `event=` and `outcome=` fields for startup, commands, ordinary messages, callbacks, callback outcomes, unsupported callback data, and application-level handler errors.

**Why this was needed:** Experiment 1 requires recognizable structured events without leaking credentials or unnecessary personal data. These logs make it easier to inspect the bot's behavior while keeping the output safe.

**Concepts learned:** A shared logging helper can extract safe Telegram identifiers from an update and keep each handler's log shape consistent. Application error handlers catch exceptions raised by bot handlers and record sanitized error types.

**Technology notes:** `log_update_event()` records event type, outcome, update ID, user ID, chat ID, message ID, and explicit safe details such as callback data or target screen. `application.add_error_handler(handle_error)` registers the sanitized error handler.

**Code meaning:** `app/handlers.py` now logs `received` and `replied` outcomes for commands/messages, `received` and `edited` outcomes for callbacks, and `failed` outcomes for handler errors. `app/main.py` logs structured startup and registers the error handler.

**Files changed:**
- `README.md`
- `app/handlers.py`
- `app/main.py`
- `docs/implementation-log/m1-implementation-log.md`
- `docs/AGENT_HANDOFF.md`

**Verification:** The bot was run locally. `/start`, `/help`, ordinary text, About lab, Back, Mock offer, and Back all still worked. Logs showed structured `event=` and `outcome=` fields for startup, commands, text messages, callbacks, and callback edit outcomes without printing the bot token or message text.

**How to confirm later:** Run `python -m app.main`, exercise `/start`, `/help`, ordinary text, and the inline buttons, then confirm logs include `event=bot.startup`, `event=command.start`, `event=command.help`, `event=message.text`, and `event=callback.menu`.

**Open issues:** None for this feature.

## m1.f5.reliability_and_edge_cases

**Status:** Committed
**Commit:** `85f18e3`

**What we built:** Added an unknown-command handler and verified the reliability edge cases required for the end of Experiment 1.

**Why this was needed:** The bot should fail gently for unsupported user input and keep working across repeated interactions and restarts before the project moves on to private-channel management.

**Concepts learned:** Handler order matters. Known `CommandHandler` routes for `/start` and `/help` must be registered before the generic `MessageHandler(filters.COMMAND, unknown_command)` fallback so valid commands do not get swallowed by the unknown-command handler.

**Technology notes:** Unknown slash commands are routed separately from ordinary text. Unsupported callback data is already handled in `handle_menu_callback()` through the fallback branch, which acknowledges the callback and edits the message to a safe unsupported-action response.

**Code meaning:** `unknown_command()` logs `command.unknown` with `received` and `replied` outcomes. `app/main.py` registers that fallback after known commands and before callback/text handlers.

**Files changed:**
- `README.md`
- `app/handlers.py`
- `app/main.py`
- `docs/implementation-log/m1-implementation-log.md`
- `docs/AGENT_HANDOFF.md`

**Verification:** The bot was run locally. `/start`, `/help`, `/unknown`, ordinary text, repeated About lab/Back/Mock offer button presses, and restart recovery all worked. Unsupported callback data was verified with a local synthetic `menu:bad` callback check; it acknowledged the callback, edited to the safe unsupported-action message, and kept a menu attached.

**How to confirm later:** Run `python -m app.main`, test `/start`, `/help`, `/unknown`, ordinary text, and repeated button navigation, then stop and restart the bot and repeat the core interactions.

**Open issues:** None for this feature.

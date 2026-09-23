# Telegram Automation Lab — Experiment 1: Bot Fundamentals

**Status:** Ready for implementation  
**Stack:** Python, Telegram Bot API, `python-telegram-bot` (current compatible stable release), long polling  
**Purpose:** A minimal, independently runnable bot for learning Telegram commands, messages, inline keyboards, callbacks, and update handling.

## Agent instructions

Implement this experiment incrementally, **one milestone at a time**. After each milestone, demonstrate the acceptance criteria and wait for approval before proceeding. Keep the code simple, typed where useful, and avoid introducing infrastructure reserved for later experiments. Do not commit or expose the bot token.

## Scope

**In:** BotFather setup guidance; local Python application; secure token configuration; long polling; `/start` and `/help`; basic text handling; inline keyboard and callback handlers; structured event logging; basic error handling; README and manual test checklist.

**Out:** Private-channel administration; invite links; membership tracking; referral attribution; database; FastAPI/webhooks; affiliate integration; analytics dashboard; deployment.

## Milestone 1.1 — Bot setup and connectivity

**Tasks**
- Create a bot through BotFather; obtain a token without sharing it in chat, logs, or commits.
- Initialize a minimal Python project with a virtual environment, pinned dependencies, `../.gitignore`, `.env.example`, and README setup steps.
- Load the token from an environment variable or local `.env` ignored by Git.
- Initialize the Telegram client with long polling and a `/start` handler.

**Acceptance criteria**
- Application starts with a valid token and shows a non-sensitive startup log.
- `/start` receives a reply in a private chat.
- Missing/invalid token fails clearly without printing secrets.

## Milestone 1.2 — Commands and messages

**Tasks**
- Implement `/start` and `/help`.
- Handle ordinary text messages separately from commands.
- Inspect Telegram's update, effective user, chat, and message identifiers using sanitized logs.

**Acceptance criteria**
- `/start` and `/help` produce distinct responses.
- Ordinary text receives a basic response.
- User ID, chat ID, message ID, and update ID can be observed without logging unnecessary personal content.

## Milestone 1.3 — Interactive buttons

**Tasks**
- Add an inline keyboard with at least two menu actions and a back action.
- Implement callback-query routing with explicit callback-data values.
- Acknowledge every callback query promptly; edit or send messages as appropriate.

**Acceptance criteria**
- Each button triggers its intended response.
- Navigation works, and Telegram's button-loading indicator clears.
- Unsupported callback data is handled safely.

## Milestone 1.4 — Event inspection

**Tasks**
- Add structured logs for startup, commands, ordinary messages, callbacks, and handler errors.
- Log timestamp, event type, update ID, relevant Telegram IDs, and handler outcome.
- Redact tokens and avoid collecting message text or personal data unless required for a specific test.

**Acceptance criteria**
- Each interaction produces a recognizable, structured event.
- Logs distinguish commands, messages, and callbacks.
- No credentials or unnecessary personal information appear in logs.

## Milestone 1.5 — Reliability and edge cases

**Tasks**
- Handle unknown commands, unexpected callback data, repeated button presses, and missing optional update fields.
- Add an application-level error handler and graceful shutdown behavior.
- Restart the app and confirm polling and handlers resume normally.

**Acceptance criteria**
- Expected invalid inputs do not crash the process.
- Callback queries are acknowledged, including unsupported ones.
- The bot resumes normal operation after restart.
- Errors are visible in sanitized logs.

## Suggested minimal project structure

```text
telegram-bot-lab/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── handlers.py
│   └── logging_config.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Keep this structure flexible; do not add extra layers until they solve an actual need.

## Manual test checklist

- [ ] Start with valid configuration.
- [ ] Missing token produces a safe, clear error.
- [ ] `/start` works.
- [ ] `/help` works.
- [ ] Ordinary text receives a response.
- [ ] Two inline actions and Back work.
- [ ] Unknown command is handled.
- [ ] Invalid callback data is handled.
- [ ] Repeated button presses do not crash the bot.
- [ ] Logs identify relevant event types without secrets.
- [ ] Restart and retest core interactions.

## Definition of done

All five milestones pass their acceptance tests; the bot runs locally; README explains installation, configuration, execution, and tests; no secrets are committed; and the implementation remains independent of future channel, attribution, and affiliate modules.

## Handoff to Experiment 2

Reuse the bot initialization, handlers, and logging foundation when introducing a private test channel, administrator permissions, invite links, join requests, and membership updates. Do not implement those capabilities during Experiment 1.

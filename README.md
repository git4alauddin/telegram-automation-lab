# Telegram Automation Lab

A guided Telegram bot lab for learning bot commands, private-channel workflows, campaign attribution, engagement tracking, analytics, and mock affiliate conversion reporting.

## Current Scope

Experiment 1 starts with a minimal local Telegram bot that runs with long polling and responds to `/start`.

## Setup

Create a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Create a local `.env` file:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
```

Do not commit `.env`.

## Run

```powershell
python -m app.main
```

Open Telegram and send `/start` to your test bot.

## Verification

- The terminal shows a non-sensitive startup log.
- `/start` receives a reply in a private chat.
- Logs include Telegram IDs needed for debugging.
- The bot token is never printed.

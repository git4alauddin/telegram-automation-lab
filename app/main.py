import logging
import os

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

from app.handlers import start
from app.logging_config import configure_logging

logger = logging.getLogger(__name__)


def get_bot_token() -> str:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is missing. Add it to your local .env file."
        )

    return token


def main() -> None:
    configure_logging()
    token = get_bot_token()

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))

    logger.info("Bot application starting with long polling")
    application.run_polling()


if __name__ == "__main__":
    main()
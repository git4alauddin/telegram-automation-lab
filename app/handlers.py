import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat

    logger.info(
        "start_command update_id=%s user_id=%s chat_id=%s",
        update.update_id,
        user.id if user else None,
        chat.id if chat else None,
    )

    await update.message.reply_text(
        "Hi! This is the Telegram Automation Lab bot. "
        "Experiment 1 is connected."
    )
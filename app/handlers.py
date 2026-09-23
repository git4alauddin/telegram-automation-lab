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


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat

    logger.info(
        "help_command update_id=%s user_id=%s chat_id=%s",
        update.update_id,
        user.id if user else None,
        chat.id if chat else None,
    )

    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the lab bot\n"
        "/help - Show this help message"
    )


async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat
    message = update.effective_message

    logger.info(
        "text_message update_id=%s user_id=%s chat_id=%s message_id=%s",
        update.update_id,
        user.id if user else None,
        chat.id if chat else None,
        message.message_id if message else None,
    )

    await update.message.reply_text(
        "I received your message. In this lab, I only log safe Telegram IDs."
    )
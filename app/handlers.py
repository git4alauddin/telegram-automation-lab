import logging
from typing import Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


def log_update_event(event_type: str, update: Update, outcome: str, **details: Any) -> None:
    user = update.effective_user
    chat = update.effective_chat
    message = update.effective_message

    detail_text = " ".join(f"{key}={value}" for key, value in details.items())

    logger.info(
        "event=%s outcome=%s update_id=%s user_id=%s chat_id=%s message_id=%s %s",
        event_type,
        outcome,
        update.update_id,
        user.id if user else None,
        chat.id if chat else None,
        message.message_id if message else None,
        detail_text,
    )


def build_main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("About lab", callback_data="menu:about"),
            InlineKeyboardButton("Mock offer", callback_data="menu:offer"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def build_back_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Back", callback_data="menu:back")],
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_update_event("command.start", update, "received")

    await update.message.reply_text(
        "Hi! This is the Telegram Automation Lab bot. "
        "Experiment 1 is connected.",
        reply_markup=build_main_menu(),
    )
    log_update_event("command.start", update, "replied")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_update_event("command.help", update, "received")

    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the lab bot\n"
        "/help - Show this help message"
    )
    log_update_event("command.help", update, "replied")


async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_update_event("message.text", update, "received")

    await update.message.reply_text(
        "I received your message. In this lab, I only log safe Telegram IDs."
    )
    log_update_event("message.text", update, "replied")


async def handle_menu_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query

    if query is None:
        log_update_event("callback.menu", update, "missing_query")
        return

    await query.answer()

    log_update_event(
        "callback.menu",
        update,
        "received",
        callback_data=query.data,
    )

    if query.data == "menu:about":
        await query.edit_message_text(
            "This lab builds Telegram automation step by step: commands, "
            "private-channel access, campaign tracking, engagement, analytics, "
            "and mock affiliate reporting.",
            reply_markup=build_back_menu(),
        )
        log_update_event(
            "callback.menu",
            update,
            "edited",
            callback_data=query.data,
            screen="about",
        )
        return

    if query.data == "menu:offer":
        await query.edit_message_text(
            "Mock offer preview: later experiments will track simulated offer "
            "clicks without using real deposits or broker conversions.",
            reply_markup=build_back_menu(),
        )
        log_update_event(
            "callback.menu",
            update,
            "edited",
            callback_data=query.data,
            screen="offer",
        )
        return

    if query.data == "menu:back":
        await query.edit_message_text(
            "Hi! This is the Telegram Automation Lab bot. "
            "Experiment 1 is connected.",
            reply_markup=build_main_menu(),
        )
        log_update_event(
            "callback.menu",
            update,
            "edited",
            callback_data=query.data,
            screen="main",
        )
        return

    await query.edit_message_text(
        "Sorry, that menu action is not supported.",
        reply_markup=build_main_menu(),
    )
    log_update_event(
        "callback.menu",
        update,
        "unsupported",
        callback_data=query.data,
    )


async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    error_type = type(context.error).__name__ if context.error else "unknown"

    if isinstance(update, Update):
        log_update_event(
            "handler.error",
            update,
            "failed",
            error_type=error_type,
        )
        return

    logger.error(
        "event=handler.error outcome=failed update_id=None "
        "user_id=None chat_id=None message_id=None error_type=%s",
        error_type,
    )

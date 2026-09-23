import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


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
        "Experiment 1 is connected.",
        reply_markup=build_main_menu(),
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


async def handle_menu_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    user = update.effective_user
    chat = update.effective_chat

    if query is None:
        logger.info("callback_missing_query update_id=%s", update.update_id)
        return

    await query.answer()

    logger.info(
        "menu_callback update_id=%s user_id=%s chat_id=%s data=%s",
        update.update_id,
        user.id if user else None,
        chat.id if chat else None,
        query.data,
    )

    if query.data == "menu:about":
        await query.edit_message_text(
            "This lab builds Telegram automation step by step: commands, "
            "private-channel access, campaign tracking, engagement, analytics, "
            "and mock affiliate reporting.",
            reply_markup=build_back_menu(),
        )
        return

    if query.data == "menu:offer":
        await query.edit_message_text(
            "Mock offer preview: later experiments will track simulated offer "
            "clicks without using real deposits or broker conversions.",
            reply_markup=build_back_menu(),
        )
        return

    if query.data == "menu:back":
        await query.edit_message_text(
            "Hi! This is the Telegram Automation Lab bot. "
            "Experiment 1 is connected.",
            reply_markup=build_main_menu(),
        )
        return

    await query.edit_message_text(
        "Sorry, that menu action is not supported.",
        reply_markup=build_main_menu(),
    )
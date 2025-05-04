from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.logger import logger


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user = update.effective_user
        logger.info(f"User {user.id} started bot")

        keyboard = [
            [InlineKeyboardButton("Начать викторину! 🐾", callback_data="start_quiz")]
        ]
        await update.message.reply_text(
            "Привет! Я бот Московского зоопарка 🦒\n"
            "Пройди викторину и узнай своё тотемное животное!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logger.error(f"Start error: {e}")
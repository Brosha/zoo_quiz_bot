from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    filters
)
from utils.logger import logger

RATING, FEEDBACK_TEXT = range(2)

async def start_feedback(update: Update, context: CallbackContext) -> int:
    try:
        keyboard = [
            [InlineKeyboardButton("⭐️", callback_data="1")],
            [InlineKeyboardButton("⭐️⭐️", callback_data="2")],
            [InlineKeyboardButton("⭐️⭐️⭐️", callback_data="3")],
            [InlineKeyboardButton("⭐️⭐️⭐️⭐️", callback_data="4")],
            [InlineKeyboardButton("⭐️⭐️⭐️⭐️⭐️", callback_data="5")]
        ]
        await update.callback_query.message.reply_text(
            "Оцените бота от 1 до 5 звезд:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return RATING
    except Exception as e:
        logger.error(f"Ошибка в start_feedback: {e}")
        return ConversationHandler.END

async def receive_rating(update: Update, context: CallbackContext) -> int:
    try:
        query = update.callback_query
        await query.answer()
        context.user_data["rating"] = query.data
        await query.message.reply_text("Напишите ваш отзыв (или /cancel для отмены):")
        return FEEDBACK_TEXT
    except Exception as e:
        logger.error(f"Ошибка в receive_rating: {e}")
        return ConversationHandler.END

async def receive_text(update: Update, context: CallbackContext) -> int:
    try:
        feedback = {
            "user_id": update.message.from_user.id,
            "rating": context.user_data.get("rating", "0"),
            "text": update.message.text
        }
        logger.info(f"Отзыв: {feedback}")
        await update.message.reply_text("Спасибо! ❤️")
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Ошибка в receive_text: {e}")
        return ConversationHandler.END

async def cancel_feedback(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("❌ Отменено.")
    context.user_data.clear()
    return ConversationHandler.END

feedback_conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(start_feedback, pattern="^feedback$")
    ],
    states={
        RATING: [CallbackQueryHandler(receive_rating)],
        FEEDBACK_TEXT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text),
            CommandHandler("cancel", cancel_feedback)
        ]
    },
    fallbacks=[CommandHandler("cancel", cancel_feedback)],
    per_message=True  # ✅ Правильное место для параметра!
)
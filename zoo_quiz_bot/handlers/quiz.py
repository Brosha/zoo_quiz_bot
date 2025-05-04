from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from data.questions import QUESTIONS
from data.animals import ANIMALS
from utils.logger import logger
from handlers.result import show_result

async def start_quiz(update: Update, context: CallbackContext) -> None:
    """Обработчик старта викторины"""
    try:
        # Инициализация данных
        context.user_data["current_question"] = 0
        context.user_data["scores"] = {animal: 0 for animal in ANIMALS}
        await send_question(update, context)
    except Exception as e:
        logger.error(f"Start quiz error: {e}")

async def handle_quiz_answer(update: Update, context: CallbackContext) -> None:
    """Обработка ответа на вопрос"""
    try:
        query = update.callback_query
        await query.answer()

        # Проверка инициализации данных (на всякий случай)
        if "current_question" not in context.user_data:
            await start_quiz(update, context)
            return

        current_q = context.user_data["current_question"]

        # Обновление баллов
        answer = query.data
        for animal, score in QUESTIONS[current_q]["options"][answer].items():
            context.user_data["scores"][animal] += score

        logger.info(f"User {query.from_user.id} answered: {answer}")

        # Переход к следующему вопросу или результату
        if current_q < len(QUESTIONS) - 1:
            context.user_data["current_question"] += 1
            await send_question(update, context)
        else:
            await show_result(update, context)

    except Exception as e:
        logger.error(f"Quiz error: {e}")

async def send_question(update: Update, context: CallbackContext) -> None:
    """Отправка вопроса пользователю"""
    try:
        current_q = context.user_data["current_question"]
        question = QUESTIONS[current_q]

        buttons = [
            [InlineKeyboardButton(option, callback_data=option)]
            for option in question["options"]
        ]

        await update.effective_message.reply_text(
            f"Вопрос {current_q + 1}/{len(QUESTIONS)}\n\n{question['text']}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        logger.error(f"Error sending question: {e}")
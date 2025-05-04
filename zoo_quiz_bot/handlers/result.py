import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config import OPECA_URL, SUPPORT_CONTACT
from data.animals import ANIMALS
from utils.logger import logger


async def show_result(update: Update, context: CallbackContext) -> None:
    """Показ результата викторины"""
    try:
        scores = context.user_data.get("scores", {})
        if not scores:
            await update.effective_message.reply_text("❌ Произошла ошибка. Попробуйте начать заново: /start")
            return

        max_score = max(scores.values())
        max_animals = [animal for animal, score in scores.items() if score == max_score]
        totem_animal = random.choice(max_animals)
        animal_info = ANIMALS.get(totem_animal, {})

        # Формируем текст результата
        text = (
            f"{animal_info.get('emoji', '🦄')} *Твоё тотемное животное — {totem_animal}!*\n\n"
            f"{animal_info.get('desc', 'Ты особенный!')}\n\n"
            "🎯 *Интересный факт:* "
            f"{random.choice(animal_info.get('facts', ['Секреты хранить умею!']))}"
        )

        # Создаем клавиатуру
        keyboard = [
            [InlineKeyboardButton("Стать опекуном 🌿", url=OPECA_URL)],
            [
                InlineKeyboardButton("Связаться с куратором 📞", url=f"https://t.me/{SUPPORT_CONTACT}"),
                InlineKeyboardButton("Пройти ещё раз 🔄", callback_data="start_quiz")
            ]
        ]

        # Отправляем результат
        await update.effective_message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard))

        logger.info(f"User {update.effective_user.id} получил результат: {totem_animal}")
        context.user_data.clear()

    except Exception as e:
        logger.error(f"Result error: {e}")
        await update.effective_message.reply_text("⚠️ Что-то пошло не так. Попробуйте /start")
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN
from handlers.start import start_command
from handlers.quiz import start_quiz, handle_quiz_answer
from handlers.feedback import feedback_conversation
from utils.logger import logger

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Регистрация обработчиков
app.add_handler(CommandHandler("start", start_command))
app.add_handler(CallbackQueryHandler(start_quiz, pattern="^start_quiz$"))  # Старт викторины
app.add_handler(CallbackQueryHandler(handle_quiz_answer))  # Ответы на вопросы
app.add_handler(feedback_conversation)  # Обратная связь

if __name__ == "__main__":
    logger.info("Starting bot...")
    try:
        app.run_polling()
    except Exception as e:
        logger.critical(f"Bot crashed: {e}")
    logger.info("Bot stopped")
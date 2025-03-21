import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import openai
import os

# Настраиваем API-ключи
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Создаём бота
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Функция для команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Отправь мне шутку, и я помогу сделать её смешнее!")

# Функция обработки сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text

    # Отправляем запрос в OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Сделай эту шутку смешнее: {user_text}"}]
    )
    
    joke = response["choices"][0]["message"]["content"]
    
    await update.message.reply_text(joke)

# Добавляем обработчики команд
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# **Важно:** Запуск бота
if __name__ == "__main__":
    print("Бот запущен!")
    app.run_polling()

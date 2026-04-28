from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from prometheus_client import start_http_server, Counter

# Метрика: лічильник отриманих повідомлень
MESSAGES_TOTAL = Counter('bot_messages_received_total', 'Total number of messages received', ['user_id'])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    
    MESSAGES_TOTAL.labels(user_id=str(user.id)).inc()
    
    print(f"Отримано повідомлення: '{text}' від {user.username}. Метрика оновлена.")
    await update.message.reply_text(f"Повідомлення опрацьовано")

if __name__ == '__main__':
    # Запуск HTTP-сервер для Prometheus на порту 9091
    start_http_server(9091)
    print("Сервер метрик запущено на порту 9091")

    app = ApplicationBuilder().token('').build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Бот запущений")
    app.run_polling()
    

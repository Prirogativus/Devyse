from constants.constants_manager import TELEGRAM_BOT_TOKEN
import telebot

TOKEN = TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(TOKEN)

subscribers = set()

@bot.message_handler(commands=['start'])
def start(message):
    subscribers.add(message.chat.id)
    bot.send_message(message.chat.id, "✅ Вы подписаны на уведомления!")

def send_push(text):
    for chat_id in subscribers:
        bot.send_message(chat_id, text)

import threading, time
def auto_push():
    while True:
        send_push("🔔 Это пуш-уведомление!")
        time.sleep(10)

threading.Thread(target=auto_push, daemon=True).start()

bot.polling()
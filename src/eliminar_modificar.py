import telebot
from decouple import config
import time

BOT_TOKEN = config('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

# @bot.message_handler(commands = ['eliminar'])


def cmd_delete_msg(message):
    initial_message = bot.send_message(
        message.chat.id, "Este mensaje cambiará y tu mensaje sera eliminado en:")
    for i in range(3, 0, -1):
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(1)
        bot.send_message(message.chat.id, f"{i}...")

    bot.edit_message_text("Salúdame primero antes de comenzar",
                          message.chat.id, initial_message.message_id)
    bot.delete_message(message.chat.id, message.message_id)

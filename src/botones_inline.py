import telebot
# import time
# Biblioteca para manejar botones
# from telebot.types import ReplyKeyboardMarkup
# from telebot.types import ForceReply  # Para citar un mensaje
# from telebot.types import ReplyKeyboardRemove  # Para remover botones
# Biblioteca para acceder a las variables de entorno del archivo .env
# from random import randint
from telebot.types import InlineKeyboardMarkup  # Para crear botonera inline
from telebot.types import InlineKeyboardButton  # Para definir botones inline

from decouple import config
BOT_TOKEN = config('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
# @bot.message_handler(commands = ['opciones'])


def cmd_options(message):
    cid = message.chat.id
    # Numero de botones en cada fila, 3 por default
    markup = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton('Mi GitHub', 'https://github.com/GoldTryck')
    button2 = InlineKeyboardButton(
        'Repo ChatBotTelegram', 'https://github.com/GoldTryck/ChatbotTelegram')
    button3 = InlineKeyboardButton(
        'Repo desarrollo web', 'https://github.com/GoldTryck/PF_DesarrolloWeb')
    button4 = InlineKeyboardButton(
        'Video random YouTube', 'https://www.youtube.com/watch?v=Ap4DtvUu7Bk&list=RDEM3wFvEfOjriWsWNr4hRPsng&start_radio=1')
    close_button = InlineKeyboardButton(
        'Cerrar', callback_data="close_options")
    markup.add(button1, button2, button3, button4, close_button)

    bot.send_message(cid, "Mis proyectos de programación", reply_markup=markup)


# @bot.callback_query_handler(func=lambda x: True)
def response_options(call):
    cid = call.from_user.id
    mid = call.message.id
    if call.data == "close_options":
        bot.delete_message(cid, mid)


'''if __name__ == '__main__':
    print('Starting bot...')
    bot.infinity_polling()'''

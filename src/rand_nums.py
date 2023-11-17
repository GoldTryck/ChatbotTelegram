import telebot
import time
# Biblioteca para manejar botones
from telebot.types import ReplyKeyboardMarkup
# from telebot.types import ForceReply  # Para citar un mensaje
from telebot.types import ReplyKeyboardRemove  # Para remover botones
# Biblioteca para acceder a las variables de entorno del archivo .env
from random import randint
from decouple import config

BOT_TOKEN = config('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
usuarios = {}  # variable global


@bot.message_handler(commands=["jugar"])
def cmd_game(message):
    num = randint(1, 10)  # generamos un numero aleatorio entre 1 y 10
    cid = message.chat.id  # guardamos el chat id
    usuarios[cid] = num

    buttons = ReplyKeyboardMarkup(
        input_field_placeholder="Selecciona una opcion...",
        row_width=5)
    buttons.add('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    ans = bot.send_message(
        cid, "Adivina el número entre 1 y 10", reply_markup=buttons)
    bot.register_next_step_handler(ans, verify_num)


def verify_num(message):
    cid = message.chat.id
    if not message.text.isdigit():
        ans = bot.send_message(cid, "ERROR. Introduce un número")
        bot.register_next_step_handler(ans, verify_num)
    else:
        n = int(message.text)
        if n < 0 or n > 10:
            ans = bot.send_message(cid, "ERROR. Número fuera del rango")
            bot.register_next_step_handler(ans, verify_num)
        else:
            if n == usuarios[cid]:
                markup = ReplyKeyboardRemove()
                bot.reply_to(message, "Felicidades! Has ganado!",
                             reply_markup=markup)
                return
            elif n > usuarios[cid]:
                ans = bot.reply_to(
                    message, "Pista: el numero que buscas es menor.")
                bot.register_next_step_handler(ans, verify_num)
            else:
                ans = bot.reply_to(
                    message, "Pista: El número que buscas es mayor.")
                bot.register_next_step_handler(ans, verify_num)


if __name__ == '__main__':
    bot.infinity_polling()

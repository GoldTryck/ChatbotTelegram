import telebot
import time
from telebot.types import InlineKeyboardMarkup  # Para crear botonera inline
from telebot.types import InlineKeyboardButton  # Para definir botones inline
from decouple import config
from src.botones_inline import cmd_options, response_options
from src.eliminar_modificar import cmd_delete_msg

BOT_TOKEN = config('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


# @bot.message_handler(content_types=[])
# def some_func(message):
#    print("hello")

@bot.message_handler(commands=["start"])
def saludar(message):
    bot.reply_to(
        message, "Hola soy un bot de prueba para el taller de Creación de Bots con Python de PROTECO y soy tu asistente de telegram.")


@bot.message_handler(commands=['ayuda', 'help'])
def ayuda(message):
    bot.reply_to(
        message, "Dejame ayudarte a interactuar conmigo."
    )


@bot.message_handler(commands=['eliminar'])
def handle_cmd_delete_msg(message):
    cmd_delete_msg(message)


@bot.message_handler(commands=['opciones'])
def handle_cmd_options(message):
    cmd_options(message)


@bot.callback_query_handler(func=lambda x: True)
def handle_response_options(call):
    response_options(call)


@bot.message_handler(func=lambda m: True)
def responder(message):
    if message.text.startswith('/'):
        bot.reply_to(message, "Comando no disponible")
    else:
        bot.reply_to(message, "Hola ¿En que puedo ayudarte?")


############ EJECUCION PRINCIPAL ########################
if __name__ == '__main__':
    bot.set_my_commands([
        telebot.types.BotCommand('/start', 'Inicia el ChatBot'),
        telebot.types.BotCommand('/help', 'Muestra lista de ayuda'),
        telebot.types.BotCommand(
            '/registro', 'Inica proceso de registro de usuario'),
        telebot.types.BotCommand('/jugar', 'Adivina el numero'),
        telebot.types.BotCommand(
            '/proyectos', 'Lista de enlaces a mis proyectos en GitHub'),
        telebot.types.BotCommand('/eliminar', 'elimina y modifica un mensaje'),
    ])
    print('iniciando bot...')
    bot.infinity_polling()

# Para agregar lista de comandos con descripcion al chat
import telebot
from telebot.types import BotCommand
from telebot.types import ForceReply
from decouple import config  # Para leer las variables del archivo .env
# Para importar todas las funciones en botones_respuesta
from src.botones_inline import *
from src.eliminar_modificar import cmd_delete_msg
from src.nekos import cmd_neko
from src.rand_nums import *


BOT_TOKEN = "6871252130:AAF4OZwHMTEcI8_YJLclIlud5kXzoKSKhoU"

bot = telebot.TeleBot(BOT_TOKEN)
usuarios = {}


@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.reply_to(
        message, "Hola soy un bot de prueba para el taller de Creación de Bots con Python de PROTECO y soy tu asistente de telegram.")


bot.infinity_polling()

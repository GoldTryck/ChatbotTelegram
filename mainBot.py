# Para agregar lista de comandos con descripcion al chat
import telebot
from decouple import config  # Para leer las variables del archivo .env
from src.botones_inline import *
from src.botones_respuesta import *
from src.eliminar_modificar import *
from src.nekos import *
from src.rand_nums import *


BOT_TOKEN = config('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.reply_to(
        message, "Hola soy un bot de prueba para el taller de Creación de Bots con Python de PROTECO y soy tu asistente de telegram.")


@bot.message_handler(commands=['ayuda', 'help'])
def cmd_help(message):
    bot.reply_to(message, "Dejame ayudarte a interactuar conmigo:\n/start: Inicia la interacción con el bot.\n/help: Muestra un menu de ayuda con comandos y su función")


# Envío de archivos multimedia
@bot.message_handler(commands=['neko'])
def call_cmd_neko(message):
    cmd_neko(bot, message)


# Edición/Eliminacion de mensajes
@bot.message_handler(commands=['eliminar'])
def call_cmd_delete_msg(message):
    cmd_delete_msg(bot, message)


# Botones de respuesta
@bot.message_handler(commands=['registro'])
def cmd_register(message):
    markup = ForceReply()  # Instanciando un objeto de la clase ForceReplay
    # guardamos el mensaje devuelto por el usuario en una variable
    ans = bot.send_message(
        message.chat.id, "¿Cúal es tu nombre?", reply_markup=markup)

    # Recibe como primer argumento un mensaje y como segundo argumento la funcion que va a gestionar dicho mensaje
    bot.register_next_step_handler(ans, get_age)


def get_age(message):
    usuarios[message.chat.id] = {}
    # message.text devuelve el nombre del usuario
    usuarios[message.chat.id]["nombre"] = message.text
    markup = ForceReply()
    ans = bot.send_message(
        message.chat.id, f'Hola {usuarios[message.chat.id]["nombre"]} ¿Cuál es tu edad?', reply_markup=markup)
    bot.register_next_step_handler(ans, get_gender)


def get_gender(message):
    if not message.text.isdigit():
        markup = ForceReply()
        ans = bot.send_message(
            message.chat.id, "ERROR. Debes ingresar una edad valida.\n¿Cúal es tu edad?", reply_markup=markup)
        bot.register_next_step_handler(ans, get_gender)
    else:
        usuarios[message.chat.id]["edad"] = int(message.text)
        # Configuracion de la botonera
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True,
            input_field_placeholder="Selecciona una opción",
            resize_keyboard=True)
        markup.add("Hombre", "Mujer", "Otro", "Prefiero no especificar")
        ans = bot.send_message(
            message.chat.id, "¿Cúal es tu género?", reply_markup=markup)
        bot.register_next_step_handler(ans, save_data)


def save_data(message):
    if not message.text in ["Hombre", "Mujer", "Otro", "Prefiero no especificar"]:
        ans = bot.send_message(
            message.chat.id, "ERROR. Debes seleccionar una opción valida.\n¿Cúal es tu geénero?")
    else:
        usuarios[message.chat.id]["genero"] = message.text
        data = "Datos ingresados:\n"
        data += f"<code>Nombre:</code> {usuarios[message.chat.id]['nombre']}\n"
        data += f"<code>Edad  :</code> {usuarios[message.chat.id]['edad']}\n"
        data += f"<code>Género:</code> {usuarios[message.chat.id]['genero']}\n"

        markup = ReplyKeyboardRemove()
        # parse_mode indica el tipo de sintaxis con el que va a interpretar las cadenas de texto, acepta markdown y html
        bot.send_message(message.chat.id, data,
                         parse_mode="html", reply_markup=markup)

        # Aquí va el código para almacenar los datos en tu base de datos

        # Eliminar los datos en menoría
        del usuarios[message.chat.id]

# Adivina el numero


@bot.message_handler(commands=['jugar'])
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
                del usuarios[cid]
                return
            elif n > usuarios[cid]:
                ans = bot.reply_to(
                    message, "Pista: el numero que buscas es menor.")
                bot.register_next_step_handler(ans, verify_num)
            else:
                ans = bot.reply_to(
                    message, "Pista: El número que buscas es mayor.")
                bot.register_next_step_handler(ans, verify_num)

# Callback_query_handdler


@bot.message_handler(commands=['enlaces'])
def call_cmd_links(message):
    cmd_links(bot, message)


@bot.callback_query_handler(func=lambda x: True)
def call_response_links(call):
    response_links(bot, call)


@bot.message_handler(func=lambda m: True)
def responder(message):
    if message.text.startswith('/'):
        bot.reply_to(message, "Comando no disponible")
    else:
        bot.reply_to(message, "Hola ¿En que puedo ayudarte?")


if __name__ == '__main__':
    print('iniciando bot...')
    bot.infinity_polling()

import telebot
from telebot.types import ReplyKeyboardMarkup  # Biblioteca para manejar botones
from telebot.types import ForceReply  # Para citar un mensaje
from telebot.types import ReplyKeyboardRemove  # Para remover botones
# Biblioteca para acceder a las variables de entorno del archivo .env
from decouple import config

BOT_TOKEN = config('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
usuarios = {}  # variable global


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


if __name__ == '__main__':
    print("Starting bot...")
    bot.infinity_polling()

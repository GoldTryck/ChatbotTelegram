from telebot.types import InlineKeyboardMarkup  # Para crear botonera inline
from telebot.types import InlineKeyboardButton  # Para definir botones inline

# @bot.message_handler(commands = ['opciones'])


def cmd_links(bot, message):
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
        'Cerrar', callback_data="close_options")  # Callback_data activara el manejador de consulta de retorno bot.callback_query_handler cuando el usuario presione el boton cerrar
    markup.add(button1, button2, button3, button4, close_button)

    bot.send_message(cid, "Mis proyectos de programación", reply_markup=markup)


# Manejar las consultas de retorno de llamada con cualquier dato:
# @bot.callback_query_handler(func=lambda x: True)
# (response_links se ejecutará siempre que se reciba una consulta de retorno de llamada)
def response_links(bot, call):
    # Obtiene el ID del usuario que inició la consulta de retorno de llamada
    cid = call.from_user.id

    # Obtiene el ID del mensaje al que se refiere la consulta de retorno de llamada
    mid = call.message.id

    # Verifica si el dato asociado con la consulta de retorno de llamada es "close_options"
    if call.data == "close_options":
        # Utiliza el método delete_message para eliminar el mensaje asociado a la consulta de retorno de llamada
        bot.delete_message(cid, mid)

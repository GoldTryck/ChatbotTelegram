import telebot

from decouple import config

BOT_TOKEN = config('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hola, ¿Cómo estas?")


@bot.message_handler(content_types=['text'])
def process_message(message):
    # Comprobamos si el mensaje contiene alguno de los operadores
    operadores = ["suma", "resta", "multiplicacion", "division"]
    for operador in operadores:
        if operador in message.text:
            # Dividimos el mensaje en dos partes: la primera parte será el comando y la segunda parte será una lista de números
            partes = message.text.split(operador)
            numeros = [int(numero)
                       for numero in partes[1].split() if numero.isdigit()]
            # Comprobamos si la lista de números está vacía
            if len(numeros) < 2:
                bot.reply_to(message, "No has ingresado suficientes números.")
            else:
                # Realizamos la operación indicada y enviamos el resultado al usuario
                if operador == "suma":
                    resultado = sum(numeros)
                    bot.reply_to(
                        message, f"La suma de {numeros} es {resultado}.")
                elif operador == "resta":
                    resultado = numeros[0] - numeros[1]
                    bot.reply_to(
                        message, f"La resta de {numeros[0]} y {numeros[1]} es {resultado}.")
                elif operador == "multiplicacion":
                    resultado = numeros[0] * numeros[1]
                    bot.reply_to(
                        message, f"La multiplicación de {numeros[0]} y {numeros[1]} es {resultado}.")
                elif operador == "division":
                    if numeros[1] != 0:
                        resultado = numeros[0] / numeros[1]
                        bot.reply_to(
                            message, f"La división de {numeros[0]} y {numeros[1]} es {resultado}.")
                    else:
                        bot.reply_to(
                            message, "Error: No se puede dividir por cero.")
                break


bot.infinity_polling()

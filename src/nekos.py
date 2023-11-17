import telebot
from random import randint


def cmd_neko(bot, message):
    # img = ["nekos/n1.jpg","nekos/n2.jpg","nekos/n3.jpg","nekos/n4.jpg","nekos/n5.jpg"]
    imagen = "nekos/n"+str(randint(1, 5))+".jpg"
    # imagen = img[random.randint(0, 2)]
    with open(imagen, 'rb') as image:
        bot.send_photo(message.chat.id, image)

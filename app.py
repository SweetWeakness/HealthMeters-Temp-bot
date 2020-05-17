import os
import telebot
from flask import Flask, request
from keyboards import get_main_admin_keyboard


TOKEN = '1245516512:AAFAPDaDe2DwPgqTZxy4eanjSpLd5VigsUg'
bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    if message.text == '1337':
        bot.reply_to(message, 'Hello, ' + message.from_user.first_name, reply_markup=get_main_admin_keyboard())
    else:
        bot.reply_to(message, 'Wrong license code')

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://health-meters-bot.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
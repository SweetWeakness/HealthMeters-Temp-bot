import os
import telebot
from flask import Flask, request


TOKEN = '1245516512:AAFAPDaDe2DwPgqTZxy4eanjSpLd5VigsUg'
bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    print(message)
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://health-meters-bot.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
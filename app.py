import telebot
from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_manager as cfg
from databases.users import users


server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = cfg.get_postgresql_url()
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server_host = cfg.get_server_host()
server_port = cfg.get_server_port()
db = SQLAlchemy(server)

from databases import api_db


TOKEN = cfg.get_token()
bot = telebot.TeleBot(TOKEN)
webhook_url = cfg.get_webhook_url()


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message) -> None:
    print(message.from_user.id)
    if message.from_user.id not in users:
        bot.send_message(message.from_user.id, "Съебал отсюда в ужасе")
        return

    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton(text="Выкинул 1 мешок, бля"))
    keyboard.add(telebot.types.KeyboardButton(text="Ты аухеешь, аж 2"))
    bot.send_message(message.from_user.id,
                     "👉👈, sweet \"" + str(message.from_user.id) + "\" user",
                     parse_mode="markdown", reply_markup=keyboard)


@bot.message_handler(commands=["clear"])
def clear(message: telebot.types.Message) -> None:
    if message.from_user.id == 410891371:
        bot.reply_to(message, "Отчистил базу данных")
        api_db.first_commit()
    else:
        bot.reply_to(message, "Ебааааать, ты что себе позволяешь???")


def code_breaker(message, cnt):
    result = api_db.add_note(message.from_user.id, cnt)
    bot.send_message(message.from_user.id, result[1])
    if result[0] != 0:
        return
    exit_code = api_db.get_stats(message.from_user.id)
    bot.send_message(message.from_user.id, exit_code[0])

    for user in exit_code[1:]:
        if message.from_user.id == user:
            bot.send_message(user, "Как видишь, ты проебываешь в этих собачьих гонках(((")
        else:
            bot.send_message(user, "Опааааа, кто то выкинул мусор больше тебя на 3 раза\n"
                                   "Ты там сходи выброси... Заодно статы чекнешь")


@bot.message_handler(content_types=["text"])
def text_handler(message: telebot.types.Message) -> None:
    if message.from_user.id not in users:
        bot.send_message(message.from_user.id, "Съебал отсюда в ужасе, я сказал")
        return

    if message.text == "Выкинул 1 мешок, бля":
        code_breaker(message, 1)
    elif message.text == "Ты аухеешь, аж 2":
        bot.reply_to(message, "Да ну нахер, реально два????")
        code_breaker(message, 2)
    else:
        bot.send_message(message.from_user.id, "Ты еблан? Жми на кнопки тока")


@server.route("/" + TOKEN, methods=["POST"])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "bot got new update", 200


@server.route("/")
def webhook():
    print("webhook's url was: {}\n".format(bot.get_webhook_info().url))
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    print("now webhook's url is: {}\n".format(bot.get_webhook_info().url))
    return "webhook was changed", 200


if __name__ == "__main__":
    server.run(threaded=True, host=server_host, port=server_port)

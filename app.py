import telebot
from flask import request

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_manager as cfg


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
    if message.from_user.id == 410891371:
        bot.reply_to(message, "Здарова, мужик! Жду твоих фоток UWU")
    else:
        bot.reply_to(message, "Здарова, мужик! Жду твоих фоток UWU\n"
                              "За доступом к нему -> @definitely_the_chosen_one\n"
                              "(напиши цифру, чтобы получить последние n фоток)")


@bot.message_handler(commands=["clear"])
def clear(message: telebot.types.Message) -> None:
    if message.from_user.id == 410891371:
        bot.reply_to(message, "Отчистил базу данных")
        api_db.first_commit()
    else:
        bot.reply_to(message, "Ебааааать, ты что себе позволяешь???")


@bot.message_handler(content_types=["text"])
def text_handler(message: telebot.types.Message) -> None:
    tmp = int(message.text)
    if tmp <= 0:
        tmp = 1
    while tmp > 0:
        img = api_db.get_photo(tmp)
        if img != -1:
            bot.send_photo(chat_id=message.from_user.id, photo=img)
        else:
            break
        tmp -= 1


@bot.message_handler(content_types=["photo"])
def photo_handler(message: telebot.types.Message) -> None:
    #if message.from_user.id != 410891371:
    #    bot.reply_to(message, "А вот хуй тебе, загружать может тока админ -_-")
    #    return

    fileID = message.photo[-1].file_id
    file = bot.get_file(fileID)
    downloaded_file = bot.download_file(file.file_path)
    print(file.file_path)

    api_db.add_photo(downloaded_file)
    #with open("image.jpg", 'wb') as new_file:
    #    new_file.write(downloaded_file)

    bot.reply_to(message, "Загружаю...")


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

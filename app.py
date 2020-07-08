import os
import telebot
from flask import Flask, request
import configparser

import database as db
import api_requests as ar
import screens as sc


config = configparser.ConfigParser()
config.read("config.ini")

TOKEN = config["bot"]["token"]
webhook_url = config["debug"]["webhook_url"] + "/" + TOKEN
print(webhook_url)

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message) -> None:
    uid = message.from_user.id

    companies = ar.get_companies_list(uid)

    if len(companies) == 1:
        # Todo Изменить на выбор из вариантов
        role = ar.get_role(uid, companies[0])
        user_info = sc.UserInfo(uid, role, message)
        sc.set_start_screen(bot, new_session, user_info)

    else:
        bot.reply_to(message, 'Вас нет в системе. Обратитесь к администратору.')


@bot.message_handler(content_types=["text"])
def text_handler(message: telebot.types.Message):
    uid = message.from_user.id
    role = new_session.get_role(uid)
    stage = new_session.get_role_stage(uid, role)

    user_info = sc.UserInfo(uid, role, message)
    # print(role)
    # print(stage)

    if role == "Role.WORKER":
        if stage == "WorkerStage.GET_TEMP":
            sc.set_getting_temp_screen(bot, new_session, user_info)

        elif stage == "WorkerStage.VALIDATION_TEMP":
            sc.set_validation_temp_screen(bot, new_session, user_info)

        elif stage == "WorkerStage.ACCEPT_TEMP":
            sc.set_accept_temp_screen(bot, new_session, user_info)

        elif stage == "WorkerStage.ACCEPT_PHOTO":
            sc.set_accept_photo_screen(bot, new_session, user_info)

    elif role == "Role.MANAGER":
        if stage == "ManagerStage.GET_INFO":
            sc.set_stat_screen(bot, user_info)

    else:
        bot.reply_to(message, "Мб зарегаетесь для начала!")


@bot.message_handler(content_types=["photo"])
def photo_handler(message):
    uid = message.from_user.id
    role = new_session.get_role(uid)
    stage = new_session.get_role_stage(uid, role)

    user_info = sc.UserInfo(uid, role, message)

    if role == "Role.WORKER":
        if stage == "WorkerStage.GET_PHOTO":
            sc.set_getting_photo_screen(bot, new_session, user_info)


@server.route("/" + TOKEN, methods=["POST"])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    print(bot.get_webhook_info())
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    print(bot.get_webhook_info())
    return "!", 200


if __name__ == "__main__":
    print(bot.get_webhook_info())
    new_session = db.SessionsStorage()
    server.run(host="127.0.0.1", port=int(os.environ.get("PORT", 80)))

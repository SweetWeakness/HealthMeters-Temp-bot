import os
import telebot
from flask import Flask, request
import configparser

import database as db
import api_requests as ar
from screens import worker_screens as ws, manager_screens as ms, default_screens as ds
from localization import Localization, Language


config = configparser.ConfigParser()
config.read("config.ini")
conf_state = "release"

localization = Localization(Language.ru)


TOKEN = config["release"]["token"]
webhook_url = config[conf_state]["webhook_url"] + "/" + TOKEN

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
users_db = db.SessionsStorage(conf_state)


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message) -> None:
    uid = message.from_user.id

    companies = ar.get_companies_list(uid)

    if len(companies) > 0:
        user_info = ds.UserInfo(message=message, users_db=users_db)
        role = ar.get_role(uid, companies[0]["guid"])
        user_info.set_role(role)

        ds.set_start_screen(bot, users_db, user_info)

    else:
        bot.reply_to(message, localization.system_access_error)


@bot.message_handler(content_types=["text"])
def text_handler(message: telebot.types.Message):
    user_info = ds.UserInfo(message=message, users_db=users_db)

    if user_info.role == "Role.WORKER":
        if user_info.stage == "WorkerStage.GET_TEMP":
            ws.set_getting_temp_screen(bot, users_db, user_info)

        elif user_info.stage == "WorkerStage.VALIDATION_TEMP":
            ws.set_validation_temp_screen(bot, users_db, user_info)

        elif user_info.stage == "WorkerStage.ACCEPT_TEMP":
            ws.set_accept_temp_screen(bot, users_db, user_info)

        elif user_info.stage == "WorkerStage.ACCEPT_PHOTO":
            ws.set_accept_photo_screen(bot, users_db, user_info)

        elif user_info.stage == "WorkerStage.GET_COMPANY":
            receiving_companies = ds.get_choosed_company(users_db, user_info)
            user_info.set_companies(receiving_companies)

            ws.set_worker_send_screen(bot, users_db, user_info)

        else:
            bot.reply_to(message, localization.missing_reply)

    elif user_info.role == "Role.MANAGER":
        if user_info.stage == "ManagerStage.CHOOSING_OPTION":
            ms.set_choosing_option_screen(bot, users_db, user_info)

        elif user_info.stage == "ManagerStage.GET_INFO":
            receiving_companies = ds.get_choosed_company(users_db, user_info)
            user_info.set_companies(receiving_companies)

            ms.set_manager_info_screen(bot, users_db, user_info)

        elif user_info.stage == "ManagerStage.ASK_TEMP":
            receiving_companies = ds.get_choosed_company(users_db, user_info)
            user_info.set_companies(receiving_companies)

            ms.set_manager_temp_screen(bot, users_db, user_info)

    else:
        bot.reply_to(message, localization.system_access_error)


@bot.message_handler(content_types=["photo"])
def photo_handler(message):
    user_info = ds.UserInfo(message=message, users_db=users_db)

    if user_info.role == "Role.WORKER":
        if user_info.stage == "WorkerStage.GET_PHOTO":
            ws.set_getting_photo_screen(bot, users_db, user_info)

        else:
            bot.reply_to(message, localization.missing_reply)

    elif user_info.role == "Role.MANAGER":
        bot.reply_to(message, localization.missing_reply)

    else:
        bot.reply_to(message, localization.system_access_error)


@bot.message_handler(content_types=["audio", "document", "sticker", "video",
                                    "video_note", "voice", "location", "contact"])
def other_types_handler(message):
    bot.reply_to(message, localization.missing_reply)


@server.route("/" + TOKEN, methods=["POST"])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    print("webhook's url was: {}\n".format(bot.get_webhook_info().url))
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    print("now webhook's url is: {}\n".format(bot.get_webhook_info().url))
    return "!", 200


@server.route("/telegram_schedule", methods=['POST'])
def get_telegram_schedule():
    res = request.get_json()
    if "telegram_id" in res:
        for telegram_id in res["telegram_id"]:
            try:
                bot.send_message(telegram_id, localization.manager_ask_measure)
            except telebot.apihelper.ApiException:
                print("не зарегался {}".format(telegram_id))
        return "ok"

    else:
        return "failed to get list of tg_id", 404


if __name__ == "__main__":
    webhook()
    print("webhook's url is: {}\n".format(bot.get_webhook_info().url))
    server.run(threaded=True, host="127.0.0.1", port=int(os.environ.get("PORT", 80)))

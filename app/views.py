import telebot
import requests
from flask import request

from app import server
from app.databases import redis_database as db
from app import api_requests as ar
from app.config import config_manager as cfg
from app.screens import manager_screens as ms, default_screens as ds, worker_screens as ws
from app.localizations.localization import Localization, Language


# TODO: Локаль предлагаю устанавливать не глобально, а для каждого пользователя.
#  хранить ее можно например в какой-нибудь мапе внутри Localization.
#  То есть для каждого юзера добавляем запись в мапу вида uid: locale_type.
#  Это не критично, пока локаль одна, однако в будущем может быть полезно сделать
#  английскую версию.
#  Передавать сам uid можно внутрь функции localization service-а.
#  Пример: localization.system_access_error(uid).
#  Единсвтенное – из-за этого может возникнуть копипаста, но я придумал как ее обойти,
#  смотри localization.py для пояснений.
localization = Localization(Language.ru)


TOKEN = cfg.get_token()
bot = telebot.TeleBot(TOKEN)
webhook_url = cfg.get_webhook_url()
users_db = db.UserStorage()


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message) -> None:
    uid = message.from_user.id

    try:
        companies = ar.get_companies_list(uid)
    except requests.exceptions.RequestException:
        bot.reply_to(message, "Связь с сервером отсутсвует, попробуйте позже.")
        return

    if len(companies) > 0:
        user_info = ds.UserInfo(message=message, users_db=users_db)
        # TODO [это уже персистентный TODO, который не относится к рефакторингу по первой ревизии]
        #  Тут как раз и стоит сетапить контекст 'роль/компания' пользователя,
        #  то есть пользователь в будущем сможет выбирать глобально с данными какой компании
        #  он взаимодействует в данный момент.
        try:
            role = ar.get_role(uid, companies[0]["guid"])
        except requests.exceptions.RequestException:
            bot.reply_to(message, "Связь с сервером отсутсвует, попробуйте позже.")
            return

        user_info.set_role(role)

        ds.set_start_screen(bot, users_db, user_info)

    else:
        bot.reply_to(message, localization.system_access_error)


@bot.message_handler(content_types=["text"])
def text_handler(message: telebot.types.Message) -> None:
    user_info = ds.UserInfo(message=message, users_db=users_db)

    if user_info.role == "Role.WORKER":
        if user_info.stage == "WorkerStage.GET_TEMP":
            ws.set_getting_temp_screen(bot, users_db, user_info)

        elif user_info.stage == "WorkerStage.VALIDATION_TEMP":
            ws.set_validation_temp_screen(bot, users_db, user_info)

        elif user_info.stage == "WorkerStage.ACCEPT_TEMP":
            ws.set_accept_temp_screen(bot, users_db, user_info)

        elif user_info.stage == "WorkerStage.GET_PHOTO":
            bot.reply_to(message, localization.missing_reply)
            bot.send_message(user_info.uid, localization.photo_validation)

        elif user_info.stage == "WorkerStage.ACCEPT_PHOTO":
            ws.set_accept_photo_screen(bot, users_db, user_info)

        elif user_info.stage == "WorkerStage.GET_COMPANY":
            receiving_companies = ds.get_chosen_company(users_db, user_info)
            user_info.set_companies(receiving_companies)

            ws.set_worker_send_screen(bot, users_db, user_info)

        else:
            bot.reply_to(message, localization.missing_reply)

    elif user_info.role == "Role.MANAGER":
        if user_info.stage == "ManagerStage.CHOOSING_OPTION":
            ms.set_choosing_option_screen(bot, users_db, user_info)

        elif user_info.stage == "ManagerStage.GET_INFO":
            receiving_companies = ds.get_chosen_company(users_db, user_info)
            user_info.set_companies(receiving_companies)

            ms.set_manager_info_screen(bot, users_db, user_info)

        elif user_info.stage == "ManagerStage.ASK_TEMP":
            receiving_companies = ds.get_chosen_company(users_db, user_info)
            user_info.set_companies(receiving_companies)

            ms.set_manager_temp_screen(bot, users_db, user_info)

    else:
        bot.reply_to(message, localization.system_access_error)


@bot.message_handler(content_types=["photo"])
def photo_handler(message: telebot.types.Message) -> None:
    user_info = ds.UserInfo(message=message, users_db=users_db)

    if user_info.role == "Role.WORKER":
        if user_info.stage == "WorkerStage.VALIDATION_TEMP":
            bot.reply_to(message, localization.missing_reply)
            bot.send_message(user_info.uid, localization.insert_temp)

        elif user_info.stage == "WorkerStage.GET_PHOTO":
            ws.set_getting_photo_screen(bot, users_db, user_info)

        else:
            bot.reply_to(message, localization.missing_reply)

    elif user_info.role == "Role.MANAGER":
        bot.reply_to(message, localization.missing_reply)

    else:
        bot.reply_to(message, localization.system_access_error)


@bot.message_handler(content_types=["audio", "document", "sticker", "video",
                                    "video_note", "voice", "location", "contact"])
def other_types_handler(message: telebot.types.Message) -> None:
    user_info = ds.UserInfo(message=message, users_db=users_db)

    if user_info.role == "Role.WORKER" or user_info.role == "Role.MANAGER":
        bot.reply_to(message, localization.missing_reply)
        if user_info.stage == "WorkerStage.VALIDATION_TEMP":
            bot.send_message(user_info.uid, localization.insert_temp)

        elif user_info.stage == "WorkerStage.GET_PHOTO":
            bot.send_message(user_info.uid, localization.photo_validation)

    else:
        bot.reply_to(message, localization.system_access_error)


@server.route("/" + TOKEN, methods=["POST"])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "bot got new update", 200


@server.route("/")
def webhook():
    print(123)
    print("webhook's url was: {}\n".format(bot.get_webhook_info().url))
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    print("now webhook's url is: {}\n".format(bot.get_webhook_info().url))
    return "webhook was changed", 200


@server.route("/telegram_schedule", methods=['POST'])
def get_telegram_schedule():
    res = request.get_json()
    if "telegram_id" in res:
        for telegram_id in res["telegram_id"]:
            try:
                bot.send_message(telegram_id, localization.manager_ask_measure)
            except telebot.apihelper.ApiException:
                print("не зарегался {}".format(telegram_id))

        return {"status": "ok"}, 200

    else:
        return "failed to get list of telegram_id", 404

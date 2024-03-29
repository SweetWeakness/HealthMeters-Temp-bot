import telebot
from flask import request

from databases import redis_database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import api_requests as ar
from config import config_manager as cfg
from screens import manager_screens as ms, worker_screens as ws, default_screens as ds
import localizations.localization as lc
from screens.keyboards import get_empty_keyboard


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
users_db = redis_database.UserStorage()


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message) -> None:
    user_info = ds.UserInfo(message=message, users_db=users_db)
    uid = message.from_user.id

    ans = api_db.set_worker_id(message.from_user.username, uid)
    if "employees" in ans:
        try:
            ar.send_request("/get_employee_tg_id", ans)
            api_db.confirm_deletion(message.from_user.username)
        except:
            print("Бэк не врубили")

    try:
        companies = ar.get_companies_list(uid)
    except:
        bot.reply_to(message, "Связь с сервером отсутсвует, попробуйте позже.")
        return

    if len(companies) > 0:
        # TODO [это уже персистентный TODO, который не относится к рефакторингу по первой ревизии]
        #  Тут как раз и стоит сетапить контекст 'роль/компания' пользователя,
        #  то есть пользователь в будущем сможет выбирать глобально с данными какой компании
        #  он взаимодействует в данный момент.
        try:
            role = ar.get_role(uid, companies[0]["guid"])
        except:
            bot.reply_to(message, "Связь с сервером отсутсвует, попробуйте позже.")
            return

        user_info.set_role(role)

        ds.set_start_screen(bot, users_db, user_info)

    else:
        bot.reply_to(message, lc.translate(user_info.lang, "system_access_error"))


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
            bot.reply_to(message, lc.translate(user_info.lang, "missing_reply"))
            bot.send_message(user_info.uid, lc.translate(user_info.lang, "photo_validation"))

        elif user_info.stage == "WorkerStage.GET_COMPANY":
            try:
                ds.set_company_context(users_db, user_info)
                ws.set_getting_company_screen(bot, users_db, user_info)
            except:
                print("бек не врубили")
                bot.reply_to(message, "Связь с сервером отсутсвует, попробуйте позже.")
                return

        elif user_info.stage == "WorkerStage.GET_LANG":
            ds.set_language_screen(bot, users_db, user_info)

        else:
            bot.reply_to(message, lc.translate(user_info.lang, "missing_reply"))

    elif user_info.role == "Role.MANAGER":
        if user_info.stage == "ManagerStage.CHOOSING_OPTION":
            ms.set_choosing_option_screen(bot, users_db, user_info)

        elif user_info.stage == "ManagerStage.MULTICOMPANY_TEXT_STATS":
            try:
                ds.set_company_context(users_db, user_info)
                ms.set_multicompany_screen(bot, users_db, user_info, "send_text_stats")
            except:
                print("бек не врубили")
                bot.reply_to(message, "Связь с сервером отсутсвует, попробуйте позже.")
                return

        elif user_info.stage == "ManagerStage.MULTICOMPANY_MEASURE":
            try:
                ds.set_company_context(users_db, user_info)
                ms.set_multicompany_screen(bot, users_db, user_info, "ask_measure")
            except:
                print("бек не врубили")
                bot.reply_to(message, "Связь с сервером отсутсвует, попробуйте позже.")
                return

        elif user_info.stage == "ManagerStage.MULTICOMPANY_FILE_STATS":
            try:
                ds.set_company_context(users_db, user_info)
                ms.set_multicompany_screen(bot, users_db, user_info, "send_file_stat")
            except:
                print("бек не врубили")
                bot.reply_to(message, "Связь с сервером отсутсвует, попробуйте позже.")
                return

        elif user_info.stage == "ManagerStage.MULTICOMPANY_EMAIL_STATS":
            try:
                ds.set_company_context(users_db, user_info)
                ms.set_multicompany_screen(bot, users_db, user_info, "set_getting_email_screen")
            except:
                print("бек не врубили")
                bot.reply_to(message, "Связь с сервером отсутсвует, попробуйте позже.")
                return

        elif user_info.stage == "ManagerStage.GET_STAT_TYPE":
            ms.set_stat_type_screen(bot, users_db, user_info)

        elif user_info.stage == "ManagerStage.ASK_MEASURE":
            ms.set_ask_measure_screen(bot, users_db, user_info)

        elif user_info.stage == "ManagerStage.GET_EMAIL":
            ms.set_get_email_screen(bot, users_db, user_info)

        elif user_info.stage == "ManagerStage.GET_LANG":
            ds.set_language_screen(bot, users_db, user_info)

        elif user_info.stage == "ManagerStage.VALIDATION_TEMP":
            ms.set_validation_temp_screen(bot, users_db, user_info)

        elif user_info.stage == "ManagerStage.ACCEPT_TEMP":
            ms.set_accept_temp_screen(bot, users_db, user_info)

        elif user_info.stage == "ManagerStage.GET_PHOTO":
            bot.reply_to(message, lc.translate(user_info.lang, "missing_reply"))
            bot.send_message(user_info.uid, lc.translate(user_info.lang, "photo_validation"))

        else:
            bot.reply_to(message, lc.translate(user_info.lang, "missing_reply"))

    else:
        bot.reply_to(message, lc.translate(user_info.lang, "system_access_error"),
                     reply_markup=get_empty_keyboard())


@bot.message_handler(content_types=["photo"])
def photo_handler(message: telebot.types.Message) -> None:
    user_info = ds.UserInfo(message=message, users_db=users_db)

    if user_info.role == "Role.WORKER" or user_info.role == "Role.MANAGER":
        if user_info.stage == "WorkerStage.VALIDATION_TEMP" or user_info.stage == "ManagerStage.VALIDATION_TEMP":
            bot.reply_to(message, lc.translate(user_info.lang, "missing_reply"))
            bot.send_message(user_info.uid, lc.translate(user_info.lang, "insert_temp"))

        elif user_info.stage == "WorkerStage.GET_PHOTO":
            ws.set_getting_photo_screen(bot, users_db, user_info)

        elif user_info.stage == "ManagerStage.GET_PHOTO":
            ms.manager_common_handler(bot, users_db, user_info, "accept_photo")

        else:
            bot.reply_to(message, lc.translate(user_info.lang, "missing_reply"))

    else:
        bot.reply_to(message, lc.translate(user_info.lang, "system_access_error"),
                     reply_markup=get_empty_keyboard())


@bot.message_handler(content_types=["audio", "document", "sticker", "video",
                                    "video_note", "voice", "location", "contact"])
def other_types_handler(message: telebot.types.Message) -> None:
    user_info = ds.UserInfo(message=message, users_db=users_db)

    if user_info.role == "Role.WORKER" or user_info.role == "Role.MANAGER":
        bot.reply_to(message, lc.translate(user_info.lang, "missing_reply"))
        if user_info.stage == "WorkerStage.VALIDATION_TEMP" or user_info.stage == "ManagerStage.VALIDATION_TEMP":
            bot.send_message(user_info.uid, lc.translate(user_info.lang, "insert_temp"))

        elif user_info.stage == "WorkerStage.GET_PHOTO" or user_info.stage == "ManagerStage.GET_PHOTO":
            bot.send_message(user_info.uid, lc.translate(user_info.lang, "photo_validation"))

    else:
        bot.reply_to(message, lc.translate(user_info.lang, "system_access_error"),
                     reply_markup=get_empty_keyboard())


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


@server.route("/telegram_schedule", methods=['POST'])
def get_telegram_schedule():
    res = request.get_json()
    if "telegram_id" in res:
        for telegram_id in res["telegram_id"]:
            try:
                bot.send_message(telegram_id, lc.translate(users_db.get_language(telegram_id), "manager_ask_measure"))
            except telebot.apihelper.ApiException:
                print("Попытка отправить на несуществующий tg_id {}".format(telegram_id))

        return {"status": "ok"}, 200

    else:
        return {"status": "failed to get list of telegram_id"}, 404


@server.route("/new_employees", methods=['POST'])
def get_new_employees():
    res = request.get_json()

    if "add" in res and "delete" in res and "edit" in res:
        api_db.add_pending_users(res["add"])

        for user in res["delete"]:
            if user["telegram_id"] is None:
                api_db.delete_waiting_user(user)
            else:
                ds.set_deleting_screen(bot, users_db, user["telegram_id"])

        for user in res["edit"]:
            if user["telegram_id"] is None:
                api_db.add_pending_users([user])
            else:
                ds.set_changing_role_screen(bot, users_db, user)

        return {"status": "ok"}, 200

    else:
        return {"status": "failed to get list of workers"}, 404


if __name__ == "__main__":
    try:
        ar.synchronize()
    except:
        print("Бэк не врубили")
    server.run(threaded=True, host=server_host, port=server_port)

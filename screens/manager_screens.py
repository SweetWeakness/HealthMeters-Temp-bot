import telebot
import base64
import pickle

import api_requests as ar
import stages as st
from screens.default_screens import UserInfo
import localizations.localization as lc
from screens import stat_maker, keyboards
from screens.default_screens import user_data_deletion
from screens.worker_screens import temp_validation


def add_measurement(bot: telebot.TeleBot, users_db, user: UserInfo, companies: list):
    reply_mes = lc.translate(user.lang, "accept_photo")
    keyboard = keyboards.get_manager_keyboard(user.lang)

    for company in companies:
        ar.add_health_data(user.uid, company["guid"], users_db.get_temp(user.uid))

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def send_text_stats(bot: telebot.TeleBot, user: UserInfo) -> st.ManagerStage:
    temp_stats = stat_maker.get_temp_stats(user.uid, user.companies, user.lang)

    temp_stats_str = temp_stats[0]
    need_measurement = temp_stats[1]

    bot.reply_to(user.message, temp_stats_str, parse_mode="markdown")

    if need_measurement:
        reply_mes = lc.translate(user.lang, "ask_measure_for_info")
        keyboard = keyboards.get_yes_no_keyboard(user.lang)
        new_stage = st.ManagerStage.ASK_MEASURE

    else:
        reply_mes = lc.translate(user.lang, "choose_option")
        keyboard = keyboards.get_manager_keyboard(user.lang)
        new_stage = st.ManagerStage.CHOOSING_OPTION

    bot.send_message(user.uid, reply_mes, reply_markup=keyboard)
    return new_stage


def ask_measure(bot: telebot.TeleBot, user: UserInfo):
    for company_guid in user.companies:
        workers_list = ar.get_attached_workers(user.uid, company_guid)

        for worker in workers_list:
            try:
                bot.send_message(worker["telegram_id"], lc.translate(user.lang, "manager_ask_measure"))
            except telebot.apihelper.ApiException:
                print("Попытка отправить на несуществующий tg_id {}".format(worker["telegram_id"]))

    reply_mes = lc.translate(user.lang, "asked_measure")
    keyboard = keyboards.get_manager_keyboard(user.lang)

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def send_file_stat(bot: telebot.TeleBot, user: UserInfo) -> None:
    bot.reply_to(user.message, lc.translate(user.lang, "looking_for_stats"))

    for company_guid in user.companies:
        df = ar.get_base64_file(user.uid, company_guid)
        df = pickle.loads(base64.b64decode(df))
        df.to_excel(company_guid + ".xlsx")
        excel_df = open(company_guid + ".xlsx", "rb")

        bot.send_document(user.uid, excel_df,
                          reply_markup=keyboards.get_manager_keyboard(user.lang))
        # todo delete file after sending and also fix problem on heroku


def set_getting_email_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if users_db.data_exist(user.uid):
        last_email = users_db.get_data(user.uid)
        keyboard = keyboards.get_emails_keyboard(user.lang, last_email)
        reply_mes = lc.translate(user.lang, "choose_email")

    else:
        keyboard = keyboards.get_back_keyboard(user.lang)
        reply_mes = lc.translate(user.lang, "insert_email")

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def manager_common_handler(bot: telebot.TeleBot, users_db, user: UserInfo, func: str) -> None:
    # func == "ask_measure" | "send_text_stats" | "send_file_stat" | "set_getting_email_screen"
    try:
        companies = ar.get_companies_list(user.uid)
    except:
        print("бек не врубили")
        bot.reply_to(user.message, lc.translate(user.lang, "server_response_error"))
        return

    if len(companies) == 1:
        user.set_companies([companies[0]["guid"]])
        users_db.set_comp_context(user.uid, companies[0]["guid"])

        try:
            if func == "ask_measure":
                ask_measure(bot, user)
                users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)
            elif func == "send_text_stats":
                new_stage = send_text_stats(bot, user)
                users_db.set_stage(user.uid, new_stage)
            elif func == "send_file_stat":
                send_file_stat(bot, user)
                users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)
            elif func == "set_getting_email_screen":
                set_getting_email_screen(bot, users_db, user)
                users_db.set_stage(user.uid, st.ManagerStage.GET_EMAIL)
            elif func == "accept_photo":
                add_measurement(bot, users_db, user, companies)
                users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)
        except:
            print("бек не врубили")
            bot.reply_to(user.message, lc.translate(user.lang, "server_response_error"))

        return

    elif len(companies) > 1:
        # new_stage is always initialized, bcs this handler is used in these func's contexts
        if func == "ask_measure":
            new_stage = st.ManagerStage.MULTICOMPANY_MEASURE
        elif func == "send_text_stats":
            new_stage = st.ManagerStage.MULTICOMPANY_TEXT_STATS
        elif func == "send_file_stat":
            new_stage = st.ManagerStage.MULTICOMPANY_FILE_STATS
        elif func == "set_getting_email_screen":
            new_stage = st.ManagerStage.MULTICOMPANY_EMAIL_STATS
        elif func == "accept_photo":
            try:
                add_measurement(bot, users_db, user, companies)
                users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)
            except:
                print("бек не врубили")
                bot.reply_to(user.message, lc.translate(user.lang, "server_response_error"))
            return

        users_db.set_stage(user.uid, new_stage)
        reply_mes = lc.translate(user.lang, "choose_company_stats")
        keyboard = keyboards.get_companies_keyboard(user.lang, companies)

    else:
        user_data_deletion(users_db, user.uid)
        reply_mes = lc.translate(user.lang, "access_error")
        keyboard = keyboards.get_empty_keyboard()

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_choosing_option_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == lc.translate(user.lang, "common_stat"):
        reply_mes = lc.translate(user.lang, "get_stat_type")
        keyboard = keyboards.get_stat_types_keyboard(user.lang)
        new_stage = st.ManagerStage.GET_STAT_TYPE

    elif user.message.text == lc.translate(user.lang, "ask_measure"):
        manager_common_handler(bot, users_db, user, "ask_measure")
        return

    elif user.message.text == lc.translate(user.lang, "measure_temp"):
        reply_mes = lc.translate(user.lang, "insert_temp")
        keyboard = keyboards.get_back_keyboard(user.lang)
        new_stage = st.ManagerStage.VALIDATION_TEMP

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
    users_db.set_stage(user.uid, new_stage)


def set_multicompany_screen(bot: telebot.TeleBot, users_db, user: UserInfo,  func: str) -> None:
    comp_context = users_db.get_comp_context(user.uid)

    if comp_context != "None":
        user.set_companies(comp_context.split())

        if func == "ask_measure":
            ask_measure(bot, user)
            users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)
        elif func == "send_text_stats":
            new_stage = send_text_stats(bot, user)
            users_db.set_stage(user.uid, new_stage)
        elif func == "send_file_stat":
            send_file_stat(bot, user)
            users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)
        elif func == "set_getting_email_screen":
            set_getting_email_screen(bot, users_db, user)
            users_db.set_stage(user.uid, st.ManagerStage.GET_EMAIL)

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))


def set_stat_type_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == lc.translate(user.lang, "text_in_chat"):
        manager_common_handler(bot, users_db, user, "send_text_stats")

    elif user.message.text == lc.translate(user.lang, "file_in_chat"):
        manager_common_handler(bot, users_db, user, "send_file_stat")

    elif user.message.text == lc.translate(user.lang, "file_on_email"):
        manager_common_handler(bot, users_db, user, "set_getting_email_screen")

    elif user.message.text == lc.translate(user.lang, "back"):
        bot.reply_to(user.message, lc.translate(user.lang, "choose_option"),
                     reply_markup=keyboards.get_manager_keyboard(user.lang))
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))


def set_ask_measure_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == lc.translate(user.lang, "yes"):
        comp_context = users_db.get_comp_context(user.uid)
        user.set_companies(comp_context.split())

        try:
            ask_measure_list = stat_maker.get_measure_list(user.uid, comp_context.split())
        except:
            print("Бэк не врубили")
            bot.reply_to(user.message, lc.translate(user.lang, "server_response_error"))
            return

        for worker in ask_measure_list:
            try:
                bot.send_message(worker["telegram_id"], lc.translate(user.lang, "manager_ask_measure"))
            except telebot.apihelper.ApiException:
                print("Попытка отправить на несуществующий tg_id {}".format(worker["telegram_id"]))

        bot.reply_to(user.message, lc.translate(user.lang, "asked_measure_for_info"),
                     reply_markup=keyboards.get_manager_keyboard(user.lang))
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    elif user.message.text == lc.translate(user.lang, "no"):
        bot.reply_to(user.message, lc.translate(user.lang, "choose_option"),
                     reply_markup=keyboards.get_manager_keyboard(user.lang))
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))


def set_get_email_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text != lc.translate(user.lang, "back"):
        comp_context = users_db.get_comp_context(user.uid)
        user.set_companies(comp_context.split())

        for company_guid in user.companies:
            try:
                ar.send_file_on_email(user.uid, company_guid, user.message.text)
            except:
                print("Бэк не врубили")
                bot.reply_to(user.message, lc.translate(user.lang, "server_response_error"))
                return

        reply_mes = lc.translate(user.lang, "sending_stats")
        keyboard = keyboards.get_manager_keyboard(user.lang)
        new_stage = st.ManagerStage.CHOOSING_OPTION

        users_db.set_data(user.uid, user.message.text)

    else:
        reply_mes = lc.translate(user.lang, "choose_option")
        keyboard = keyboards.get_stat_types_keyboard(user.lang)
        new_stage = st.ManagerStage.GET_STAT_TYPE

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
    users_db.set_stage(user.uid, new_stage)


def set_validation_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    temp = user.message.text.replace(",", ".")
    if temp_validation(temp):
        temp = round(float(temp), 1)
        if 35.0 < temp < 41.0:
            reply_mes = lc.translate(user.lang, "ask_temp").format(temp)
            keyboard = keyboards.get_accept_keyboard(user.lang)

            users_db.set_stage(user.uid, st.ManagerStage.ACCEPT_TEMP)
            users_db.set_temp(user.uid, temp)
        else:
            reply_mes = lc.translate(user.lang, "temp_validation")
            keyboard = keyboards.get_back_keyboard(user.lang)

    elif temp == lc.translate(user.lang, "back"):
        bot.reply_to(user.message, lc.translate(user.lang, "choose_option"), reply_markup=keyboards.get_employee_keyboard(user.lang))
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)
        return

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))
        bot.send_message(user.uid, lc.translate(user.lang, "insert_temp"))
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_accept_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == lc.translate(user.lang, "mistake"):
        new_stage = st.ManagerStage.VALIDATION_TEMP
        reply_mes = lc.translate(user.lang, "reinsert_temp")
        keyboard = keyboards.get_back_keyboard(user.lang)

    elif user.message.text == lc.translate(user.lang, "accept"):
        new_stage = st.ManagerStage.GET_PHOTO
        reply_mes = lc.translate(user.lang, "accept_temp")
        keyboard = keyboards.get_empty_keyboard()

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
    users_db.set_stage(user.uid, new_stage)

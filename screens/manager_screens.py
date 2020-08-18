import telebot

import api_requests as ar
import stages as st
import keyboards
from screens.default_screens import UserInfo
import localizations.localization as lc
from screens import stat_maker


def send_stats(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    try:
        temp_stats = stat_maker.get_temp_stats(user.uid, user.companies, user.lang)
    except:
        print("Бэк не врубили")
        bot.reply_to(user.message, lc.translate(user.lang, "server_response_error"))
        return

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
    users_db.set_stage(user.uid, new_stage)


def ask_measure(bot: telebot.TeleBot, users_db, user: UserInfo):
    for company in user.companies:
        workers_list = ar.get_attached_workers(user.uid, company)

        for worker in workers_list:
            try:
                bot.send_message(worker["telegram_id"], lc.translate(user.lang, "manager_ask_measure"))
            except telebot.apihelper.ApiException:
                print("Попытка отправить на несуществующий tg_id {}".format(worker["telegram_id"]))

    reply_mes = lc.translate(user.lang, "asked_measure")
    keyboard = keyboards.get_manager_keyboard(user.lang)

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
    users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)


def manager_stats_handler(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    try:
        companies = ar.get_companies_list(user.uid)
    except:
        print("бек не врубили")
        bot.reply_to(user.message, lc.translate(user.lang, "server_response_error"))
        return

    if len(companies) == 1:
        user.set_companies([companies[0]["guid"]])
        send_stats(bot, users_db, user)
        users_db.set_comp_context(user.uid, companies[0]["guid"])
        return

    elif len(companies) > 1:
        users_db.set_stage(user.uid, st.ManagerStage.MULTICOMPANY_STATS)
        reply_mes = lc.translate(user.lang, "choose_company_stats")
        keyboard = keyboards.get_companies_keyboard(user.lang, companies)

    else:
        users_db.set_role(user.uid, st.Role.NOBODY)
        reply_mes = lc.translate(user.lang, "access_error")
        keyboard = keyboards.get_empty_keyboard()

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def manager_temp_handler(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    try:
        companies = ar.get_companies_list(user.uid)
    except:
        print("бек не врубили")
        bot.reply_to(user.message, lc.translate(user.lang, "server_response_error"))
        return

    if len(companies) == 1:
        user.set_companies([companies[0]["guid"]])

        try:
            ask_measure(bot, users_db, user)
        except:
            print("бек не врубили")
            bot.reply_to(user.message, lc.translate(user.lang, "server_response_error"))

        return

    elif len(companies) > 1:
        users_db.set_stage(user.uid, st.ManagerStage.MULTICOMPANY_MEASURE)
        reply_mes = lc.translate(user.lang, "choose_company_measure")
        keyboard = keyboards.get_companies_keyboard(user.lang, companies)

    else:
        users_db.set_role(user.uid, st.Role.NOBODY)
        reply_mes = lc.translate(user.lang, "access_error")
        keyboard = keyboards.get_empty_keyboard()

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_choosing_option_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == lc.translate(user.lang, "common_stat"):
        reply_mes = lc.translate(user.lang, "get_stat_type")
        keyboard = keyboards.get_stat_types_keyboard(user.lang)
        bot.reply_to(user.message, reply_mes, reply_markup=keyboard)

        users_db.set_stage(user.uid, st.ManagerStage.GET_STAT_TYPE)

    elif user.message.text == lc.translate(user.lang, "ask_measure"):
        manager_temp_handler(bot, users_db, user)

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))


def set_multicompany_stats_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    comp_context = users_db.get_comp_context(user.uid)

    if comp_context != "None":
        user.set_companies(comp_context.split())
        send_stats(bot, users_db, user)

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))


def set_multicompany_measure_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    comp_context = users_db.get_comp_context(user.uid)

    if comp_context != "None":
        user.set_companies(comp_context.split())
        ask_measure(bot, users_db, user)

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))


def set_stat_type_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == lc.translate(user.lang, "text_in_chat"):
        manager_stats_handler(bot, users_db, user)

    elif user.message.text == lc.translate(user.lang, "file_in_chat"):
        bot.reply_to(user.message, lc.translate(user.lang, "looking_for_stats"))
        # TODO запрос статистики и ее вывод
        bot.send_message(user.uid, "Zdes budet statistika", reply_markup=keyboards.get_manager_keyboard(user.lang))
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    elif user.message.text == lc.translate(user.lang, "file_on_email"):
        if users_db.data_exist(user.uid):
            last_email = users_db.get_data(user.uid)
            keyboard = keyboards.get_emails_keyboard(user.lang, last_email)
            reply_mes = lc.translate(user.lang, "choose_email")

        else:
            keyboard = keyboards.get_back_keyboard(user.lang)
            reply_mes = lc.translate(user.lang, "insert_email")

        bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
        users_db.set_stage(user.uid, st.ManagerStage.GET_EMAIL)

    elif user.message.text == lc.translate(user.lang, "back"):
        bot.reply_to(user.message, lc.translate(user.lang, "choose_option"), reply_markup=keyboards.get_manager_keyboard(user.lang))
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
                bot.send_message(worker["id"], lc.translate(user.lang, "manager_ask_measure"))
            except telebot.apihelper.ApiException:
                print("Попытка отправить на несуществующий tg_id {}".format(worker["id"]))

        bot.reply_to(user.message, lc.translate(user.lang, "asked_measure_for_info"), reply_markup=keyboards.get_manager_keyboard(user.lang))
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    elif user.message.text == lc.translate(user.lang, "no"):
        bot.reply_to(user.message, lc.translate(user.lang, "choose_option"), reply_markup=keyboards.get_manager_keyboard(user.lang))
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))


def set_get_email_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text != lc.translate(user.lang, "back"):
        # TODO отправляем на такую то почту (user.message.text)
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

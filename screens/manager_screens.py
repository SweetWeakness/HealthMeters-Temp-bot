import telebot
from datetime import datetime

import keyboards
import stages as st
import api_requests as ar
from screens.default_screens import UserInfo
from localization import Localization, Language


localization = Localization(Language.ru)


def pretty_date(ugly_date) -> str:
    date = datetime.strptime(ugly_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date.strftime('%Y-%m-%d %H:%M:%S')


def get_temp_stats(manager_uid: int, companies_list: list) -> str:
    ans = ""

    for company in companies_list:
        workers_stats = ar.get_workers_stats(manager_uid, company)
        for stat in workers_stats:
            ans += "_" + stat["initials"] + "_"
            if "date" in stat:
                ans += " *" + str(stat["last_temp"]) + "* "
                ans += pretty_date(stat["date"])
            else:
                ans += " *-*"

            ans += "\n"

    ans += "\n\n" + localization.stats_message + " " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return ans


def manager_stats_handler(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    companies = ar.get_companies_list(user.uid)

    if len(companies) == 1:
        temp_stats = get_temp_stats(user.uid, companies)

        bot.send_message(user.uid, temp_stats, parse_mode="markdown")

        reply_mes = localization.made_stats
        keyboard = None

    elif len(companies) > 1:
        users_db.set_stage(user.uid, st.ManagerStage.GET_INFO)
        reply_mes = localization.choose_company_stats
        keyboard = keyboards.get_companies_keyboard(companies)

    else:
        users_db.set_role(user.uid, st.Role.NOBODY)
        reply_mes = localization.access_error
        keyboard = keyboards.get_empty_keyboard()

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def manager_temp_handler(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    companies = ar.get_companies_list(user.uid)

    if len(companies) == 1:
        workers_list = ar.get_attached_workers(user.uid, companies[0])
        for worker in workers_list:
            try:
                bot.send_message(worker["telegram_id"], localization.manager_ask_measure)
            except telebot.apihelper.ApiException:
                print("не зарегался {}".format(worker["telegram_id"]))

        reply_mes = localization.asked_measure
        keyboard = None

    elif len(companies) > 1:
        users_db.set_stage(user.uid, st.ManagerStage.ASK_TEMP)
        reply_mes = localization.choose_company_measure
        keyboard = keyboards.get_companies_keyboard(companies)

    else:
        users_db.set_role(user.uid, st.Role.NOBODY)
        reply_mes = localization.access_error
        keyboard = keyboards.get_empty_keyboard()

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_choosing_option_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == localization.common_stat:
        manager_stats_handler(bot, users_db, user)

    elif user.message.text == localization.ask_measure:
        manager_temp_handler(bot, users_db, user)

    else:
        bot.reply_to(user.message, localization.missing_reply)


def set_manager_info_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if len(user.companies) > 0:
        reply_mes = localization.made_stats
        keyboard = keyboards.get_manager_keyboard()

        temp_stats = get_temp_stats(user.uid, user.companies)

        bot.send_message(user.uid, temp_stats)
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    else:
        bot.reply_to(user.message, localization.missing_reply)
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_manager_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if len(user.companies) > 0:
        reply_mes = localization.asked_measure
        keyboard = keyboards.get_manager_keyboard()

        for company_guid in user.companies:
            workers_list = ar.get_attached_workers(user.uid, company_guid)
            for worker in workers_list:
                try:
                    bot.send_message(worker["telegram_id"], localization.manager_ask_measure)
                except telebot.apihelper.ApiException:
                    print("не зарегался {}".format(worker["telegram_id"]))

        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    else:
        bot.reply_to(user.message, localization.missing_reply)
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)

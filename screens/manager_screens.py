import telebot
import re
import time


import keyboards
import stages as st
import api_requests as ar
from screens.default_screens import UserInfo


def pretty_date(ugly_date) -> str:
    date = time.strptime(ugly_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return "{}.{}.{} {}:{}".format(date.tm_mday, date.tm_mon, date.tm_year, date.tm_hour, date.tm_min)


def get_temp_stats(workers_list: list) -> str:
    ans = "Запрашиваемая статистика:\n"

    for measure in workers_list:
        p_date = ""
        if "date" in measure:
            p_date = pretty_date(measure["date"])
        temp = "-"
        # Todo Убрать регулярку
        if not re.match(r"^-?\d+(?:\.\d+)?$", str(measure["last_temp"])) is None:
            temp = str(measure["last_temp"])
        ans += "_" + measure["initials"] + "_ *" + temp + "* " + p_date + "\n"

    return ans


def manager_stats_handler(bot: telebot.TeleBot, users_db, user: UserInfo):
    companies = ar.get_companies_list(user.uid)

    if len(companies) == 1:
        bot.reply_to(user.message, "Вывожу общую статистику")

        workers_list = ar.get_workers_stats(user.uid, companies[0])
        temp_stats = get_temp_stats(workers_list)

        bot.send_message(user.uid, temp_stats, parse_mode="markdown")
        return

    elif len(companies) > 1:
        users_db.set_stage(user.uid, st.ManagerStage.GET_INFO)
        reply_mes = "Выберите компанию, по которой нужна статистика:"
        keyboard = keyboards.get_companies_keyboard(companies)

    else:
        users_db.set_role(user.uid, st.Role.NOBODY)
        reply_mes = "У вас нет доступа. Обратитесь к администратору."
        keyboard = None

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def manager_temp_handler(bot: telebot.TeleBot, users_db, user: UserInfo):
    companies = ar.get_companies_list(user.uid)

    if len(companies) == 1:
        bot.reply_to(user.message, "Запросил измерения температуры")

        workers_list = ar.get_attached_workers(user.uid, companies[0])
        for worker in workers_list:
            bot.send_message(worker["telegram_id"], "Ваш менеджер просит измерить температуру!")
        return

    elif len(companies) > 1:
        users_db.set_stage(user.uid, st.ManagerStage.ASK_TEMP)
        reply_mes = "Выберите компанию, в которой надо првоести замеры:"
        keyboard = keyboards.get_companies_keyboard(companies)

    else:
        users_db.set_role(user.uid, st.Role.NOBODY)
        reply_mes = "У вас нет доступа. Обратитесь к администратору."
        keyboard = None

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_choosing_option_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == "Вывести общую статистику":
        manager_stats_handler(bot, users_db, user)

    elif user.message.text == "Запросить измерения температуры":
        manager_temp_handler(bot, users_db, user)

    else:
        bot.reply_to(user.message, "Извините, я вас не понял")


def set_manager_info_screen(bot: telebot.TeleBot, users_db, user: UserInfo):
    if len(user.companies) > 0:
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)
        reply_mes = "Вывел общую статистику"
        keyboard = keyboards.get_manager_keyboard()

        temp_stats = ""

        for company_guid in user.companies:
            workers_list = ar.get_workers_stats(user.uid, company_guid)
            print(workers_list)
            temp_stats += get_temp_stats(workers_list)

        bot.send_message(user.uid, temp_stats)

    else:
        reply_mes = "Ошибка, такой компании нет. Выберите компанию:"
        keyboard = None

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_manager_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo):
    if len(user.companies) > 0:
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)
        reply_mes = "Отправил уведомление сотрудникам"
        keyboard = keyboards.get_manager_keyboard()

        for company_guid in user.companies:
            workers_list = ar.get_attached_workers(user.uid, company_guid)
            for worker in workers_list:
                bot.send_message(worker["telegram_id"], "Ваш менеджер просит измерить температуру!")

    else:
        reply_mes = "Ошибка, такой компании нет. Выберите компанию:"
        keyboard = None

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)

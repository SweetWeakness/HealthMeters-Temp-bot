import telebot
from datetime import datetime

import api_requests as ar
import stages as st
import keyboards
from screens.default_screens import UserInfo
import localizations.localization as lc


def pretty_date(ugly_date) -> str:
    date = datetime.utcfromtimestamp(ugly_date)
    return date.strftime("%d.%m %H:%M")


def get_key_from_stats(worker_stats: dict) -> float:
    if "date" in worker_stats:
        measure_date = datetime.utcfromtimestamp(worker_stats["date"]).strftime("%d.%m")
        current_date = datetime.today().strftime("%d.%m")
        if current_date == measure_date:
            return worker_stats["last_temp"]
        else:
            return 0.
    else:
        return 0.


def get_temp_stats(manager_uid: int, companies_list: list, lang: str) -> list:
    ans = ""
    flg = False

    for company in companies_list:
        workers_stats = ar.get_workers_stats(manager_uid, company)
        workers_stats = sorted(workers_stats, key=get_key_from_stats, reverse=True)

        first_block = []
        second_block = []
        third_block = []

        for stat in workers_stats:
            if stat["last_temp"] is not None:
                measure_date = datetime.utcfromtimestamp(stat["date"]).strftime("%d.%m")
                current_date = datetime.today().strftime("%d.%m")
                if current_date == measure_date:
                    if stat["last_temp"] >= 37:
                        first_block.append(stat)
                    else:
                        second_block.append(stat)
                else:
                    third_block.append(stat)
            else:
                third_block.append(stat)

        if len(first_block) != 0:
            ans += "Измерили, есть температура:\n"
            for stat in first_block:
                ans += "_%s_\t\t*%s*\t\t%s\n" % (stat["initials"], str(stat["last_temp"]), pretty_date(stat["date"]))
            ans += "\\_" * 30 + "\n\n"

        if len(second_block) != 0:
            ans += "Измерили, температура отсутствует:\n"
            for stat in second_block:
                ans += "_%s_\t\t*%s*\t\t%s\n" % (stat["initials"], str(stat["last_temp"]), pretty_date(stat["date"]))
            ans += "\n"

        if len(third_block) != 0:
            flg = True
            ans += "Не измеряли:\n"
            for stat in third_block:
                ans += "_%s_" % (stat["initials"])
                if "date" in stat:
                    ans += "\t\t*%s*\t\tпоследний замер\t\t%s\n" % (str(stat["last_temp"]), pretty_date(stat["date"]))
                else:
                    ans += "\t\tданные отсутсвуют (нет измерений)\n"

            ans += "\n"

    if ans == "":
        return ["У вас нет прикрепленных сотрудников.", False]

    ans += "%s\t\t%s." % (lc.translate(lang, "stats_message"), datetime.now().strftime('%d.%m.%Y %H:%M'))

    return [ans, flg]


def send_stats(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    temp_stats = get_temp_stats(user.uid, user.companies, user.lang)
    temp_stats_str = temp_stats[0]
    need_measurement = temp_stats[1]

    bot.reply_to(user.message, temp_stats_str, parse_mode="markdown")

    if need_measurement:
        reply_mes = "Запросить измерения у тех, кто не померился?"
        keyboard = keyboards.get_keyboard(["Да", "Нет"])
        new_stage = st.ManagerStage.ASK_MEASURE

    else:
        reply_mes = "Выберите опцию:"
        keyboard = keyboards.get_manager_keyboard(user.lang)
        new_stage = st.ManagerStage.CHOOSING_OPTION

    bot.send_message(user.uid, reply_mes, reply_markup=keyboard)
    users_db.set_stage(user.uid, new_stage)


def ask_measure(bot: telebot.TeleBot, users_db, user: UserInfo):
    reply_mes = lc.translate(user.lang, "asked_measure")
    keyboard = keyboards.get_manager_keyboard(user.lang)

    for company in user.companies:
        workers_list = ar.get_attached_workers(user.uid, company)

        for worker in workers_list:
            try:
                bot.send_message(worker["telegram_id"], lc.translate(user.lang, "manager_ask_measure"))
            except telebot.apihelper.ApiException:
                print("Попытка отправить на несуществующий tg_id {}".format(worker["telegram_id"]))

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)

    users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)


def manager_stats_handler(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    try:
        companies = ar.get_companies_list(user.uid)
    except:
        print("бек не врубили")
        bot.reply_to(user.message, "Связь с сервером отсутсвует, попробуйте позже.")
        return

    if len(companies) == 1:
        user.set_companies([companies[0]["guid"]])
        send_stats(bot, users_db, user)
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
        bot.reply_to(user.message, "Связь с сервером отсутсвует, попробуйте позже.")
        return

    if len(companies) == 1:
        user.set_companies([companies[0]["guid"]])

        try:
            ask_measure(bot, users_db, user)
        except:
            print("бек не врубили")
            bot.reply_to(user.message, "Связь с сервером отсутсвует, попробуйте позже.")

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
        reply_mes = "Как вам вывести статистику?\nВыберите опцию:"
        keyboard = keyboards.get_stat_types_keyboard()
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
    if user.message.text == "Текстом в чат":
        manager_stats_handler(bot, users_db, user)

    elif user.message.text == "Файлом в чат":
        bot.reply_to(user.message, "Запрашиваю статистику.")
        # TODO запрос статистики и ее вывод
        bot.send_message(user.uid, "Zdes budet statistika", reply_markup=keyboards.get_manager_keyboard(user.lang))

        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    elif user.message.text == "Файлом на почту":
        if users_db.data_exist(user.uid):
            last_email = users_db.get_data(user.uid)
            keyboard = keyboards.get_emails_keyboard(last_email)
            reply_mes = "Введите почту или выберите предыдущую:"

        else:
            keyboard = keyboards.get_empty_keyboard()
            reply_mes = "Введите почту:"

        bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
        users_db.set_stage(user.uid, st.ManagerStage.GET_EMAIL)

    elif user.message.text == "Назад":
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)
        bot.reply_to(user.message, "Выберите опцию:", reply_markup=keyboards.get_manager_keyboard(user.lang))

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))


def set_ask_measure_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == "Да":
        # TODO запрос измерения
        bot.reply_to(user.message, "Запросил измерения у тех, кто не померился", reply_markup=keyboards.get_manager_keyboard(user.lang))
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    elif user.message.text == "Нет":
        bot.reply_to(user.message, "Выберите опцию:", reply_markup=keyboards.get_manager_keyboard(user.lang))
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))


def set_get_email_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text != "Назад":
        # TODO отправляем на такую то почту (user.message.text)
        reply_mes = "Собираю статистику и отправляю ее вам на почту..."
        keyboard = keyboards.get_manager_keyboard(user.lang)
        new_stage = st.ManagerStage.CHOOSING_OPTION

        users_db.set_data(user.uid, user.message.text)

    else:
        reply_mes = "Выберите опцию:"
        keyboard = keyboards.get_stat_types_keyboard()
        new_stage = st.ManagerStage.GET_STAT_TYPE

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)

    users_db.set_stage(user.uid, new_stage)

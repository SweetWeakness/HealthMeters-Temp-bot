import telebot
from datetime import datetime

import api_requests as ar
import stages as st
import keyboards
from screens.default_screens import UserInfo
from localizations.localization import Localization, Language


# TODO: Про localization уже поговорили в файлах app.py и localization.py
localization = Localization(Language.ru)


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


def get_temp_stats(manager_uid: int, companies_list: list) -> list:
    ans = ""
    flg = False

    for company in companies_list:
        workers_stats = ar.get_workers_stats(manager_uid, company["guid"])
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

    ans += "%s\t\t%s." % (localization.stats_message, datetime.now().strftime('%d.%m.%Y %H:%M'))

    return [ans, flg]


def manager_stats_handler(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    try:
        companies = ar.get_companies_list(user.uid)
    except:
        print("бек не врубили")
        bot.reply_to(user.message, "Связь с сервером отсутсвует, попробуйте позже.")
        return

    if len(companies) == 1:
        temp_stats = get_temp_stats(user.uid, companies)
        temp_stats_str = temp_stats[0]
        need_measurement = temp_stats[1]

        bot.reply_to(user.message, temp_stats_str, parse_mode="markdown")

        if need_measurement:
            reply_mes = "Запросить измерения у тех, кто не померился?"
            keyboard = keyboards.get_keyboard(["Да", "Нет"])
            new_stage = st.ManagerStage.ASK_MEASURE

        else:
            reply_mes = "Выберите опцию:"
            keyboard = keyboards.get_manager_keyboard()
            new_stage = st.ManagerStage.CHOOSING_OPTION

        bot.send_message(user.uid, reply_mes, reply_markup=keyboard)
        users_db.set_stage(user.uid, new_stage)
        return

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
    try:
        companies = ar.get_companies_list(user.uid)
    except:
        print("бек не врубили")
        bot.reply_to(user.message, "Связь с сервером отсутсвует, попробуйте позже.")
        return

    if len(companies) == 1:
        try:
            workers_list = ar.get_attached_workers(user.uid, companies[0]["guid"])
        except:
            print("бек не врубили")
            bot.reply_to(user.message, "Связь с сервером отсутсвует, попробуйте позже.")
            return
        
        for worker in workers_list:
            try:
                bot.send_message(worker["telegram_id"], localization.manager_ask_measure)
            except telebot.apihelper.ApiException:
                print("Попытка отправить на несуществующий tg_id {}".format(worker["telegram_id"]))

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
        bot.reply_to(user.message, "Как вам вывести статистику?\nВыберите опцию:", reply_markup=keyboards.get_stat_types_keyboard())
        users_db.set_stage(user.uid, st.ManagerStage.GET_STAT)

    elif user.message.text == localization.ask_measure:
        manager_temp_handler(bot, users_db, user)

    else:
        bot.reply_to(user.message, localization.missing_reply)


def set_manager_info_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if len(user.companies) > 0:
        temp_stats = get_temp_stats(user.uid, user.companies)
        temp_stats_str = temp_stats[0]
        need_measurement = temp_stats[1]

        bot.reply_to(user.message, temp_stats_str, parse_mode="markdown")

        if need_measurement:
            reply_mes = "Запросить измерения у тех, кто не померился?"
            keyboard = keyboards.get_keyboard(["Да", "Нет"])
            new_stage = st.ManagerStage.ASK_MEASURE

        else:
            reply_mes = "Выберите опцию:"
            keyboard = keyboards.get_manager_keyboard()
            new_stage = st.ManagerStage.CHOOSING_OPTION

        bot.send_message(user.uid, reply_mes, reply_markup=keyboard)
        users_db.set_stage(user.uid, new_stage)
        return

    else:
        bot.reply_to(user.message, localization.missing_reply)


def set_manager_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if len(user.companies) > 0:
        reply_mes = localization.asked_measure
        keyboard = keyboards.get_manager_keyboard()

        for company in user.companies:
            try:
                workers_list = ar.get_attached_workers(user.uid, company["guid"])
            except:
                print("бек не врубили")
                bot.reply_to(user.message, "Связь с сервером отсутсвует, попробуйте позже.")
                return
            
            for worker in workers_list:
                try:
                    bot.send_message(worker["telegram_id"], localization.manager_ask_measure)
                except telebot.apihelper.ApiException:
                    print("Попытка отправить на несуществующий tg_id {}".format(worker["telegram_id"]))

        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    else:
        bot.reply_to(user.message, localization.missing_reply)
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_stat_type_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == "Текстом в чат":
        manager_stats_handler(bot, users_db, user)

    elif user.message.text == "Файлом в чат":
        bot.reply_to(user.message, "Запрашиваю статистику.")
        # TODO запрос статистики и ее вывод
        bot.send_message(user.uid, "Zdes budet statistika", reply_markup=keyboards.get_manager_keyboard())

        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    elif user.message.text == "Файлом на почту":
        if users_db.data_exist(user.uid):
            emails = users_db.get_data(user.uid).split()
            keyboard = keyboards.get_emails_keyboard(emails)
            reply_mes = "Введите почту или выберите предыдущую:"

        else:
            keyboard = keyboards.get_empty_keyboard()
            reply_mes = "Введите почту:"

        bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
        users_db.set_stage(user.uid, st.ManagerStage.GET_EMAIL)

    else:
        bot.reply_to(user.message, localization.missing_reply)


def set_ask_measure_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == "Да":
        # TODO запрос измерения
        bot.reply_to(user.message, "Запросил измерения у тех, кто не померился", reply_markup=keyboards.get_manager_keyboard())
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    elif user.message.text == "Нет":
        bot.reply_to(user.message, "Выберите опцию:", reply_markup=keyboards.get_manager_keyboard())
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

    else:
        bot.reply_to(user.message, localization.missing_reply)


def set_get_email_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    # TODO отправляем на такую то почту
    bot.reply_to(user.message, "Собираю статистику и отправляю ее вам на почту...", reply_markup=keyboards.get_manager_keyboard())
    users_db.set_data(user.uid, user.message.text)
    users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)

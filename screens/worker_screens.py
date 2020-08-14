import telebot

import api_requests as ar
import stages as st
import keyboards
from screens.default_screens import UserInfo
import localizations.localization as lc


def temp_validation(temp: str) -> bool:
    try:
        float(temp)
        return True
    except:
        return False


def set_getting_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == lc.translate(user.lang, "measure_temp"):
        reply_mes = lc.translate(user.lang, "insert_temp")
        keyboard = keyboards.get_back_keyboard()
        new_stage = st.WorkerStage.VALIDATION_TEMP

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
    users_db.set_stage(user.uid, new_stage)


def set_validation_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    temp = user.message.text.replace(",", ".")
    if temp_validation(temp):
        temp = round(float(temp), 1)
        if 35.0 < temp < 41.0:
            reply_mes = lc.translate(user.lang, "ask_temp").format(temp)
            keyboard = keyboards.get_accept_keyboard(user.lang)

            users_db.set_stage(user.uid, st.WorkerStage.ACCEPT_TEMP)
            users_db.set_data(user.uid, temp)
        else:
            reply_mes = lc.translate(user.lang, "temp_validation")
            keyboard = keyboards.get_back_keyboard()

    elif temp == "Назад":
        bot.reply_to(user.message, "Выберите опцию:", reply_markup=keyboards.get_employee_keyboard(user.lang))
        users_db.set_stage(user.uid, st.WorkerStage.GET_TEMP)
        return

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))
        bot.send_message(user.uid, lc.translate(user.lang, "insert_temp"))
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_accept_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == lc.translate(user.lang, "mistake"):
        new_stage = st.WorkerStage.VALIDATION_TEMP
        reply_mes = lc.translate(user.lang, "reinsert_temp")
        keyboard = keyboards.get_back_keyboard()

    elif user.message.text == lc.translate(user.lang, "accept"):
        new_stage = st.WorkerStage.GET_PHOTO
        reply_mes = lc.translate(user.lang, "accept_temp")
        keyboard = keyboards.get_empty_keyboard()

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
    users_db.set_stage(user.uid, new_stage)


def set_getting_photo_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    try:
        companies = ar.get_companies_list(user.uid)
    except:
        print("бек не врубили")
        bot.reply_to(user.message, "Связь с сервером отсутсвует, попробуйте позже.")
        return

    if len(companies) == 1:
        new_stage = st.WorkerStage.GET_TEMP
        reply_mes = lc.translate(user.lang, "accept_photo")
        keyboard = keyboards.get_employee_keyboard(user.lang)

        try:
            ar.add_health_data(user.uid, companies[0]["guid"], users_db.get_data(user.uid))
        except:
            print("бек не врубили")
            bot.reply_to(user.message, "Связь с сервером отсутсвует, попробуйте позже.")
            return

    elif len(companies) > 1:
        new_stage = st.WorkerStage.GET_COMPANY
        reply_mes = lc.translate(user.lang, "accept_companies")
        keyboard = keyboards.get_companies_keyboard(user.lang, companies)

    else:
        users_db.set_role(user.uid, st.Role.NOBODY)
        bot.reply_to(user.message, lc.translate(user.lang, "access_error"))
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
    users_db.set_stage(user.uid, new_stage)


""" подтверждение фотки
def set_accept_photo_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == lc.translate(user.lang, mistake:
        new_stage = st.WorkerStage.GET_PHOTO
        reply_mes = lc.translate(user.lang, reinsert_photo
        keyboard = keyboards.get_empty_keyboard()

    elif user.message.text == lc.translate(user.lang, accept:
        try:
            companies = ar.get_companies_list(user.uid)
        except:
            print("бек не врубили")
            bot.reply_to(user.message, "Связь с сервером отсутсвует, попробуйте позже.")
            return

        if len(companies) == 1:
            new_stage = st.WorkerStage.GET_TEMP
            reply_mes = lc.translate(user.lang, accept_photo
            keyboard = keyboards.get_employee_keyboard()

            try:
                ar.add_health_data(user.uid, companies[0]["guid"], users_db.get_data(user.uid))
            except:
                print("бек не врубили")
                bot.reply_to(user.message, "Связь с сервером отсутсвует, попробуйте позже.")
                return

        elif len(companies) > 1:
            new_stage = st.WorkerStage.GET_COMPANY
            reply_mes = lc.translate(user.lang, accept_companies
            keyboard = keyboards.get_companies_keyboard(companies)

        else:
            users_db.set_role(user.uid, st.Role.NOBODY)
            bot.reply_to(user.message, lc.translate(user.lang, access_error)
            return

    else:
        bot.reply_to(user.message, lc.translate(user.lang, missing_reply)
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
    users_db.set_stage(user.uid, new_stage)
"""


def set_worker_send_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    comp_context = users_db.get_comp_context(user.uid)

    if comp_context != "None":
        reply_mes = lc.translate(user.lang, "accept_photo")
        keyboard = keyboards.get_employee_keyboard(user.lang)

        for company in comp_context.split():
            ar.add_health_data(user.uid, company, users_db.get_data(user.uid))

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
    users_db.set_stage(user.uid, st.WorkerStage.GET_TEMP)

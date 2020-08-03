import telebot

from app import keyboards, stages as st, api_requests as ar
from app.screens.default_screens import UserInfo
from app.localizations.localization import Localization, Language


# TODO: Про localization уже поговорили в файлах views.py и localization.py
localization = Localization(Language.ru)


def temp_validation(temp: str) -> bool:
    try:
        float(temp)
        return True
    except:
        return False


def set_getting_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == localization.measure_temp:
        reply_mes = localization.insert_temp
        keyboard = keyboards.get_empty_keyboard()
        new_stage = st.WorkerStage.VALIDATION_TEMP
    else:
        bot.reply_to(user.message, localization.missing_reply)
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
    users_db.set_stage(user.uid, new_stage)


def set_validation_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    temp = user.message.text.replace(",", ".")
    if temp_validation(temp):
        temp = round(float(temp), 1)
        if 35.0 < temp < 41.0:
            reply_mes = localization.ask_temp.format(temp)
            keyboard = keyboards.get_accept_keyboard()

            users_db.set_stage(user.uid, st.WorkerStage.ACCEPT_TEMP)
            users_db.set_data(user.uid, temp)
        else:
            reply_mes = localization.temp_validation
            keyboard = keyboards.get_empty_keyboard()

    else:
        bot.reply_to(user.message, localization.missing_reply)
        bot.send_message(user.uid, localization.insert_temp)
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_accept_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == localization.mistake:
        new_stage = st.WorkerStage.VALIDATION_TEMP
        reply_mes = localization.reinsert_temp

    elif user.message.text == localization.accept:
        new_stage = st.WorkerStage.GET_PHOTO
        reply_mes = localization.accept_temp

    else:
        bot.reply_to(user.message, localization.missing_reply)
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboards.get_empty_keyboard())
    users_db.set_stage(user.uid, new_stage)


def set_getting_photo_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    bot.reply_to(user.message, localization.got_photo, reply_markup=keyboards.get_accept_keyboard())
    users_db.set_stage(user.uid, st.WorkerStage.ACCEPT_PHOTO)


def set_accept_photo_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == localization.mistake:
        new_stage = st.WorkerStage.GET_PHOTO
        reply_mes = localization.reinsert_photo
        keyboard = keyboards.get_empty_keyboard()

    elif user.message.text == localization.accept:
        try:
            companies = ar.get_companies_list(user.uid)
        except:
            print("бек не врубили")
            bot.reply_to(user.message, "Связь с сервером отсутсвует, попробуйте позже.")
            return

        if len(companies) == 1:
            new_stage = st.WorkerStage.GET_TEMP
            reply_mes = localization.accept_photo
            keyboard = keyboards.get_employee_keyboard()

            try:
                ar.add_health_data(user.uid, companies[0]["guid"], users_db.get_data(user.uid))
                users_db.set_last_date(user.uid)
            except:
                print("бек не врубили")
                bot.reply_to(user.message, "Связь с сервером отсутсвует, попробуйте позже.")
                return

        elif len(companies) > 1:
            new_stage = st.WorkerStage.GET_COMPANY
            reply_mes = localization.accept_companies
            keyboard = keyboards.get_companies_keyboard(companies)

        else:
            users_db.set_role(user.uid, st.Role.NOBODY)
            bot.reply_to(user.message, localization.access_error)
            return

    else:
        bot.reply_to(user.message, localization.missing_reply)
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
    users_db.set_stage(user.uid, new_stage)


def set_worker_send_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if len(user.companies) > 0:
        reply_mes = localization.accept_photo
        keyboard = keyboards.get_employee_keyboard()

        for company in user.companies:
            try:
                ar.add_health_data(user.uid, company["guid"], users_db.get_data(user.uid))
                users_db.set_last_date(user.uid)
            except:
                print("бек не врубили")
                bot.reply_to(user.message, "Связь с сервером отсутсвует, попробуйте позже.")
                return

    else:
        bot.reply_to(user.message, localization.missing_reply)
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)
    users_db.set_stage(user.uid, st.WorkerStage.GET_TEMP)

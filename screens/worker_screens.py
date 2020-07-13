import telebot

import keyboards
import stages as st
import api_requests as ar
from screens.default_screens import UserInfo


def temp_validation(temp: str) -> bool:
    try:
        float(temp)
        return True
    except:
        return False


def set_getting_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == "Измерить температуру":
        users_db.set_stage(user.uid, st.WorkerStage.VALIDATION_TEMP)
        reply_mes = "Введите вашу температуру (например, 36.6):"
        keyboard = keyboards.get_empty_keyboard()

    else:
        bot.reply_to(user.message, "Извините, я вас не понял")
        return

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_validation_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    temp = user.message.text.replace(",", ".")
    if temp_validation(temp):
        temp = round(float(temp), 1)
        if 35.0 < temp < 41.0:
            users_db.set_stage(user.uid, st.WorkerStage.ACCEPT_TEMP)
            users_db.set_data(user.uid, temp)

            reply_mes = "Ваша температура {}, все верно?".format(temp)
            keyboard = keyboards.get_accept_keyboard()
        else:
            reply_mes = "Неправильный ввод, вы не человек, введите еще раз."
            keyboard = keyboards.get_empty_keyboard()
    else:
        reply_mes = "Неправильный ввод, мб нормально введете? Введите еще раз."
        keyboard = keyboards.get_empty_keyboard()

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_accept_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == "Ошибка, щас исправлю":
        new_stage = st.WorkerStage.VALIDATION_TEMP
        reply_mes = "Хорошо, введите вашу температуру еще раз:"

    elif user.message.text == "Все верно":
        new_stage = st.WorkerStage.GET_PHOTO
        reply_mes = "Отлично, жду фотку"

    else:
        bot.reply_to(user.message, "Извините, я вас не понял")
        return

    users_db.set_stage(user.uid, new_stage)
    bot.reply_to(user.message, reply_mes, reply_markup=keyboards.get_empty_keyboard())


def set_getting_photo_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    users_db.set_stage(user.uid, st.WorkerStage.ACCEPT_PHOTO)
    bot.reply_to(user.message, "Фотку получил", reply_markup=keyboards.get_accept_keyboard())


def set_accept_photo_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == "Ошибка, щас исправлю":
        new_stage = st.WorkerStage.GET_PHOTO
        reply_mes = "Хорошо, отправьте фото еще раз:"
        keyboard = keyboards.get_empty_keyboard()

    elif user.message.text == "Все верно":
        companies = ar.get_companies_list(user.uid)

        if len(companies) == 1:
            new_stage = st.WorkerStage.GET_TEMP
            reply_mes = "Спасибо за фотку)"
            keyboard = keyboards.get_employee_keyboard()

            ar.add_health_data(user.uid, companies[0], users_db.get_data(user.uid))

        elif len(companies) > 1:
            new_stage = st.WorkerStage.GET_COMPANY
            reply_mes = "Спасибо за фотку) Выберите компанию, в которую надо отправить фото:"
            keyboard = keyboards.get_companies_keyboard(companies)

        else:
            users_db.set_role(user.uid, st.Role.NOBODY)
            bot.reply_to(user.message, "У вас нет доступа. Обратитесь к администратору.")
            return

    else:
        bot.reply_to(user.message, "Извините, я вас не понял")
        return

    users_db.set_stage(user.uid, new_stage)
    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_worker_send_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if len(user.companies) > 0:
        users_db.set_stage(user.uid, st.WorkerStage.GET_TEMP)
        reply_mes = "Отправил замеры"
        keyboard = keyboards.get_employee_keyboard()

        for company_guid in user.companies:
            ar.add_health_data(user.uid, company_guid, users_db.get_data(user.uid))

    else:
        reply_mes = "Ошибка, такой компании нет. Выберите компанию:"
        keyboard = None

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)

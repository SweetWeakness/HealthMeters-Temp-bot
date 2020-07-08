import re
import time
import telebot

import keyboards
import stages as st
import api_requests as ar


class UserInfo:
    def __init__(self, uid: int, role: str, message: telebot.types.Message):
        self.uid = uid
        self.role = role
        self.message = message


def pretty_date(ugly_date) -> str:
    date = time.strptime(ugly_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return "{}.{}.{} {}:{}".format(date.tm_mday, date.tm_mon, date.tm_year, date.tm_hour, date.tm_min)


def temp_validation(temp: str) -> bool:
    try:
        temp = temp.replace(",", ".")
        float(temp)
        return True
    except:
        return False


def set_start_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.role == "worker":
        new_role = st.Role.WORKER
        stage = st.WorkerStage.GET_TEMP
        keyboard = keyboards.get_employee_keyboard()
    elif user.role == "manager":
        new_role = st.Role.MANAGER
        stage = st.ManagerStage.GET_INFO
        keyboard = keyboards.get_manager_keyboard()
    else:
        bot.reply_to(user.message, "У вас нет доступа. Обратитесь к администратору.")
        return

    users_db.set_role(user.uid, new_role)
    users_db.set_role_stage(user.uid, new_role, stage)

    bot.reply_to(user.message, "Здравствуйте!", reply_markup=keyboard)


def set_accept_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == "Ошибка, щас исправлю":
        new_stage = st.WorkerStage.VALIDATION_TEMP
        reply_mes = "Хорошо, введите вашу температуру еще раз:"

    elif user.message.text == "Все верно":
        new_stage = st.WorkerStage.GET_PHOTO
        reply_mes = "Отлично, жду фотку"

    else:
        return

    users_db.set_role_stage(user.uid, st.Role.WORKER, new_stage)

    bot.reply_to(user.message, reply_mes, reply_markup=keyboards.get_empty_keyboard())


def set_accept_photo_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == "Ошибка, щас исправлю":
        new_stage = st.WorkerStage.GET_PHOTO
        reply_mes = "Хорошо, отправьте фото еще раз:"
        keyboard = keyboards.get_empty_keyboard()

    elif user.message.text == "Все верно":
        new_stage = st.WorkerStage.GET_TEMP
        reply_mes = "Спасибо за фотку)"
        keyboard = keyboards.get_employee_keyboard()

        companies = ar.get_companies_list(user.uid)
        ar.add_health_data(user.uid, companies[0], users_db.get_data(user.uid))
    else:
        return

    users_db.set_role_stage(user.uid, st.Role.WORKER, new_stage)

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_validation_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if temp_validation(user.message.text):
        temp = float(user.message.text)
        if 35.0 < temp < 41.0:
            users_db.set_role_stage(user.uid, st.Role.WORKER, st.WorkerStage.ACCEPT_TEMP)
            reply_mes = "Ваша температура {}, все верно?".format(temp)
            keyboard = keyboards.get_accept_keyboard()
            users_db.set_data(user.uid, temp)
        else:
            reply_mes = "Неправильный ввод, вы не человек, введите еще раз."
            keyboard = keyboards.get_empty_keyboard()
    else:
        reply_mes = "Неправильный ввод, мб нормально введете? Введите еще раз."
        keyboard = keyboards.get_empty_keyboard()

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def get_temp_stats(workers_list: list) -> str:
    ans = ""

    for measure in workers_list:
        p_date = ""
        if "date" in measure:
            p_date = pretty_date(measure["date"])
        temp = "-"
        if not re.match(r"^-?\d+(?:\.\d+)?$", str(measure["last_temp"])) is None:
            temp = str(measure["last_temp"])
        ans += "_" + measure["initials"] + "_ *" + temp + "* " + p_date + "\n"

    return ans


def set_stat_screen(bot: telebot.TeleBot, user: UserInfo) -> None:
    if user.message.text == "Вывести общую статистику":
        guid = ar.get_companies_list(user.uid)[0]
        workers_list = ar.get_workers_stats(user.uid, guid)

        temp_stats = get_temp_stats(workers_list)

        bot.reply_to(user.message, temp_stats, reply_markup=keyboards.get_manager_keyboard(), parse_mode="markdown")

    elif user.message.text == "Запросить измерения температуры":
        guid = ar.get_companies_list(user.uid)[0]
        workers_list = ar.get_attached_workers(user.uid, guid)

        for worker in workers_list:
            bot.send_message(worker["telegram_id"], "Ваш менеджер просит измерить температуру!")


def set_getting_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == "Измерить температуру":
        users_db.set_role_stage(user.uid, st.Role.WORKER, st.WorkerStage.VALIDATION_TEMP)
        bot.reply_to(user.message, "Введите вашу температуру (например, 36.6):", reply_markup=keyboards.get_empty_keyboard())


def set_getting_photo_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    users_db.set_role_stage(user.message.from_user.id, st.Role.WORKER, st.WorkerStage.ACCEPT_PHOTO)
    bot.reply_to(user.message, "Фотку получил", reply_markup=keyboards.get_accept_keyboard())

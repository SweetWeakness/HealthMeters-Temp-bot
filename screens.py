import re
import time
import telebot

import keyboards
import stages as st
import api_requests as ar


class UserInfo:
    def __init__(self, uid: int, role: str, companies: list, message: telebot.types.Message):
        self.uid = uid
        self.message = message
        self.role = role
        self.companies = companies

    def set_role(self, role):
        self.role = role

    def set_companies(self, companies):
        self.companies = companies


def pretty_date(ugly_date) -> str:
    date = time.strptime(ugly_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return "{}.{}.{} {}:{}".format(date.tm_mday, date.tm_mon, date.tm_year, date.tm_hour, date.tm_min)


def temp_validation(temp: str) -> bool:
    try:
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
        stage = st.ManagerStage.CHOOSING_OPTION
        keyboard = keyboards.get_manager_keyboard()

    else:
        bot.reply_to(user.message, "У вас нет доступа. Обратитесь к администратору.")
        return

    users_db.set_role(user.uid, new_role)
    users_db.set_stage(user.uid, stage)

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

    users_db.set_stage(user.uid, new_stage)

    bot.reply_to(user.message, reply_mes, reply_markup=keyboards.get_empty_keyboard())


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
        return

    users_db.set_stage(user.uid, new_stage)

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_validation_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    temp = user.message.text.replace(",", ".")
    if temp_validation(temp):
        temp = float(temp)
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


def get_temp_stats(workers_list: list) -> str:
    ans = ""

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


def set_choosing_option_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == "Вывести общую статистику":
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

    elif user.message.text == "Запросить измерения температуры":
        companies = ar.get_companies_list(user.uid)

        if len(companies) == 1:
            bot.reply_to(user.message, "Запросил измерения температуры")

            workers_list = ar.get_workers_stats(user.uid, companies[0])
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

    else:
        reply_mes = "Извините, я вас не понял"
        keyboard = None

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_getting_temp_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.message.text == "Измерить температуру":
        users_db.set_stage(user.uid, st.WorkerStage.VALIDATION_TEMP)
        reply_mes = "Введите вашу температуру (например, 36.6):"
        keyboard = keyboards.get_empty_keyboard()

    else:
        reply_mes = "Извините, я вас не понял"
        keyboard = None

    bot.reply_to(user.message, reply_mes, reply_markup=keyboard)


def set_getting_photo_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    users_db.set_stage(user.message.from_user.id, st.WorkerStage.ACCEPT_PHOTO)
    bot.reply_to(user.message, "Фотку получил", reply_markup=keyboards.get_accept_keyboard())


def get_choosed_company(user: UserInfo) -> list:
    companies = ar.get_companies_list(user.uid)

    if user.message.text in companies:
        return [user.message.text]

    elif user.message.text == "Выбрать все":
        return companies

    else:
        return []


def set_worker_send_screen(bot: telebot.TeleBot, users_db, user: UserInfo):
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


def set_manager_info_screen(bot: telebot.TeleBot, users_db, user: UserInfo):
    if len(user.companies) > 0:
        users_db.set_stage(user.uid, st.ManagerStage.CHOOSING_OPTION)
        reply_mes = "Вывел общую статистику"
        keyboard = keyboards.get_manager_keyboard()

        temp_stats = ""

        for company_guid in user.companies:
            workers_list = ar.get_workers_stats(user.uid, company_guid)
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

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


def set_start_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.role == "worker":
        new_role = st.Role.WORKER
        new_stage = st.WorkerStage.GET_TEMP
        keyboard = keyboards.get_employee_keyboard()

    elif user.role == "manager":
        new_role = st.Role.MANAGER
        new_stage = st.ManagerStage.CHOOSING_OPTION
        keyboard = keyboards.get_manager_keyboard()

    else:
        bot.reply_to(user.message, "У вас нет доступа. Обратитесь к администратору.")
        return

    users_db.set_role(user.uid, new_role)
    users_db.set_stage(user.uid, new_stage)

    bot.reply_to(user.message, "Здравствуйте!", reply_markup=keyboard)


def get_choosed_company(users_db, user: UserInfo) -> list:
    companies = ar.get_companies_list(user.uid)

    if len(companies) == 0:
        users_db.set_role(user.uid, st.Role.NOBODY)
        return []

    if user.message.text in companies:
        return [user.message.text]

    elif user.message.text == "Выбрать все":
        return companies

    else:
        return []

import telebot

import api_requests as ar
import stages as st
import keyboards
from localizations.localization import Localization, Language


# TODO: Про localization уже поговорили в файлах app.py и localization.py
localization = Localization(Language.ru)


class UserInfo:
    def __init__(self, message: telebot.types.Message, users_db):
        self.message = message
        self.uid = message.from_user.id
        self.companies = []
        if users_db.stage_exist(self.uid):
            self.stage = users_db.get_stage(self.uid)
        else:
            self.stage = "no stage"
        if users_db.role_exist(self.uid):
            self.role = users_db.get_role(self.uid)
        else:
            self.role = st.Role.NOBODY

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
        bot.reply_to(user.message, localization.access_error)
        return

    users_db.set_role(user.uid, new_role)
    users_db.set_stage(user.uid, new_stage)

    bot.reply_to(user.message, localization.greeting, reply_markup=keyboard)


def get_chosen_company(users_db, user: UserInfo) -> list:
    companies = ar.get_companies_list(user.uid)

    if len(companies) == 0:
        users_db.set_role(user.uid, st.Role.NOBODY)
        return []

    if user.message.text == localization.choose_all:
        return companies

    else:
        for company in companies:
            if company["name"] == user.message.text:
                return [company]

        return []

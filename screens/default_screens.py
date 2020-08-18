import telebot

import api_requests as ar
import stages as st
import keyboards
import localizations.localization as lc


class UserInfo:
    def __init__(self, message: telebot.types.Message, users_db):
        self.message = message
        self.uid = message.from_user.id
        self.companies = []
        self.stage = users_db.get_stage(self.uid)
        self.role = users_db.get_role(self.uid)
        self.lang = users_db.get_language(self.uid)

    def set_role(self, role) -> None:
        self.role = role

    def set_companies(self, companies) -> None:
        self.companies = companies

    def set_language(self, language) -> None:
        self.lang = language


def set_changing_role_screen(bot: telebot.TeleBot, users_db, user_list: list) -> None:
    for user in user_list:
        lang = users_db.get_language(user["telegram_id"])
        tg_id = user["telegram_id"]

        if user["role"] == "worker":
            try:
                bot.send_message(tg_id, "Ваша роль была изменена", reply_markup=keyboards.get_employee_keyboard(lang))
            except telebot.apihelper.ApiException:
                print("Попытка отправить на несуществующий tg_id {}".format(tg_id))

            users_db.set_role(tg_id, st.Role.WORKER)
            users_db.set_stage(tg_id, st.WorkerStage.GET_TEMP)

        elif user["role"] == "manager":
            try:
                bot.send_message(tg_id, "Ваша роль была изменена", reply_markup=keyboards.get_manager_keyboard(lang))
            except telebot.apihelper.ApiException:
                print("Попытка отправить на несуществующий tg_id {}".format(tg_id))

            users_db.set_role(tg_id, st.Role.MANAGER)
            users_db.set_stage(tg_id, st.ManagerStage.CHOOSING_OPTION)

        if users_db.data_exist(tg_id):
            users_db.delete_data(tg_id)


def set_start_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.role == "worker":
        new_role = st.Role.WORKER
        new_stage = st.WorkerStage.GET_LANG

    elif user.role == "manager":
        new_role = st.Role.MANAGER
        new_stage = st.ManagerStage.GET_LANG

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "access_error"))
        return

    users_db.set_role(user.uid, new_role)
    users_db.set_stage(user.uid, new_stage)

    bot.reply_to(user.message, "Choose your language:", reply_markup=keyboards.get_language_keyboard())


def set_language_screen(bot: telebot.TeleBot, users_db, user: UserInfo) -> None:
    if user.role == "Role.MANAGER":
        keyboard = keyboards.get_manager_keyboard(user.lang)
        new_stage = st.ManagerStage.CHOOSING_OPTION
    else:
        keyboard = keyboards.get_employee_keyboard(user.lang)
        new_stage = st.WorkerStage.GET_TEMP

    if user.message.text == "Русский🇷🇺":
        users_db.set_language(user.uid, "ru")
        user.set_language("ru")

    elif user.message.text == "English🇬🇧":
        # need english localization
        users_db.set_language(user.uid, "ru")
        user.set_language("ru")

    else:
        bot.reply_to(user.message, lc.translate(user.lang, "missing_reply"))
        return

    bot.reply_to(user.message, lc.translate(user.lang, "accept_lang"), reply_markup=keyboard)
    bot.send_message(user.uid, lc.translate(user.lang, "greeting"))
    users_db.set_stage(user.uid, new_stage)


def set_company_context(users_db, user: UserInfo) -> None:
    users_db.set_comp_context(user.uid, "None")
    companies = ar.get_companies_list(user.uid)

    if len(companies) == 0:
        users_db.set_role(user.uid, st.Role.NOBODY)
        return

    if user.message.text == lc.translate(user.lang, "choose_all"):
        comp_context = ""
        for company in companies:
            comp_context += "%s " % company["guid"]
        users_db.set_comp_context(user.uid, comp_context)

    else:
        for company in companies:
            if company["name"] == user.message.text:
                users_db.set_comp_context(user.uid, company["guid"])
                return

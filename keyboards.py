import telebot
from localizations.localization import Localization, Language


# TODO: Про localization уже поговорили в файлах app.py и localization.py
localization = Localization(Language.ru)


def get_keyboard(buttons_text_list: list) -> telebot.types.ReplyKeyboardMarkup:
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for button_text in buttons_text_list:
        tmp_button = telebot.types.KeyboardButton(text=button_text)
        keyboard.add(tmp_button)

    return keyboard


def get_manager_keyboard():
    buttons_text_list = [localization.common_stat, localization.ask_measure]
    return get_keyboard(buttons_text_list)


def get_employee_keyboard():
    buttons_text_list = [localization.measure_temp]
    return get_keyboard(buttons_text_list)


def get_accept_keyboard():
    buttons_text_list = [localization.accept, localization.mistake]
    return get_keyboard(buttons_text_list)


def get_stat_types_keyboard():
    buttons_text_list = ["Текстом в чат", "Файлом в чат", "Файлом на почту"]
    return get_keyboard(buttons_text_list)


def get_empty_keyboard():
    return telebot.types.ReplyKeyboardRemove()


def get_emails_keyboard(emails_list: list):
    return get_keyboard(emails_list)


def get_companies_keyboard(comp_list: list):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for comp in comp_list:
        button = telebot.types.KeyboardButton(text=comp["name"])
        keyboard.add(button)

    keyboard.add(telebot.types.KeyboardButton(text=localization.choose_all))

    return keyboard

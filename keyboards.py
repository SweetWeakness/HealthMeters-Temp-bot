import telebot
from localization import Localization, Language

localization = Localization(Language.ru)


def get_admin_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    button1 = telebot.types.KeyboardButton(text=localization.add_employee)
    button2 = telebot.types.KeyboardButton(text=localization.delete_employee)

    button3 = telebot.types.KeyboardButton(text=localization.attach_employee)
    button4 = telebot.types.KeyboardButton(text=localization.list_employee)

    button5 = telebot.types.KeyboardButton(text=localization.stat)

    keyboard.add(button1, button2, button3, button4, button5)

    return keyboard


def get_main_admin_keyboard():
    keyboard = get_admin_keyboard()

    button = telebot.types.KeyboardButton(text=localization.license_info)

    keyboard.add(button)

    return keyboard


def get_manager_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    # button1 = telebot.types.KeyboardButton(text=localization.stat_employee)
    # button2 = telebot.types.KeyboardButton(text=localization.list_attach_employee)
    button3 = telebot.types.KeyboardButton(text=localization.common_stat)
    button4 = telebot.types.KeyboardButton(text=localization.ask_temp)

    keyboard.add(button4, button3)

    return keyboard


def get_employee_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    button = telebot.types.KeyboardButton(text=localization.measure_temp)

    keyboard.add(button)

    return keyboard


def get_role_choose_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    button1 = telebot.types.KeyboardButton(text=localization.role_admin)
    button2 = telebot.types.KeyboardButton(text=localization.role_manager)
    button3 = telebot.types.KeyboardButton(text=localization.role_worker)

    keyboard.add(button1, button2, button3)

    return keyboard


def get_accept_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    button1 = telebot.types.KeyboardButton(text="Все верно")
    button2 = telebot.types.KeyboardButton(text="Ошибка, щас исправлю")

    keyboard.add(button1, button2)

    return keyboard


def get_empty_keyboard():
    return telebot.types.ReplyKeyboardRemove()


def get_companies_keyboard(comp_list: list):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for comp in comp_list:
        button = telebot.types.KeyboardButton(text=comp)
        keyboard.add(button)

    keyboard.add(telebot.types.KeyboardButton(text="Выбрать все"))

    return keyboard

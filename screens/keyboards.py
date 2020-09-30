import telebot
import localizations.localization as lc


def get_keyboard(buttons_text_list: list) -> telebot.types.ReplyKeyboardMarkup:
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for button_text in buttons_text_list:
        tmp_button = telebot.types.KeyboardButton(text=button_text)
        keyboard.add(tmp_button)

    return keyboard


def get_manager_keyboard(lang: str):
    buttons_text_list = [lc.translate(lang, "common_stat"), lc.translate(lang, "ask_measure"),
                         lc.translate(lang, "measure_temp")]
    return get_keyboard(buttons_text_list)


def get_employee_keyboard(lang: str):
    buttons_text_list = [lc.translate(lang, "measure_temp")]
    return get_keyboard(buttons_text_list)


def get_accept_keyboard(lang: str):
    buttons_text_list = [lc.translate(lang, "accept"), lc.translate(lang, "mistake")]
    return get_keyboard(buttons_text_list)


def get_back_keyboard(lang: str):
    return get_keyboard([lc.translate(lang, "back")])


def get_stat_types_keyboard(lang: str):
    b1 = [lc.translate(lang, "text_in_chat"), lc.translate(lang, "file_in_chat")]
    b2 = [lc.translate(lang, "back"), lc.translate(lang, "file_on_email")]

    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.row(b1[0], b1[1])
    keyboard.row(b2[0], b2[1])

    return keyboard


def get_empty_keyboard():
    return telebot.types.ReplyKeyboardRemove()


def get_emails_keyboard(lang: str, last_email: str):
    return get_keyboard([last_email, lc.translate(lang, "back")])


def get_yes_no_keyboard(lang: str):
    return get_keyboard([lc.translate(lang, "yes"), lc.translate(lang, "no")])


def get_language_keyboard():
    return get_keyboard(["Русский🇷🇺", "English🇬🇧"])


def get_companies_keyboard(lang: str, comp_list: list):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for comp in comp_list:
        button = telebot.types.KeyboardButton(text=comp["name"])
        keyboard.add(button)

    keyboard.add(telebot.types.KeyboardButton(text=lc.translate(lang, "choose_all")))

    return keyboard

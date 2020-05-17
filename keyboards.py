import telebot


def get_main_admin_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text='Добавить сотрудника')
    button2 = telebot.types.KeyboardButton(text='Удалить сотрудника')
    button3 = telebot.types.KeyboardButton(text='Статус лицензии')

    keyboard.add(button1, button2, button3)

    return keyboard
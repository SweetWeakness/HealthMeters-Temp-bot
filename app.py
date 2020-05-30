import os
import telebot
import re
import time
from flask import Flask, request
import api_requests as ar
import localization
import keyboards


TOKEN = '1245516512:AAFAPDaDe2DwPgqTZxy4eanjSpLd5VigsUg'
bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

def pretty_date(ugly_date):
    date = time.strptime(ugly_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    return '{}.{}.{} {}:{}'.format(date.tm_mday, date.tm_mon, date.tm_year, date.tm_hour, date.tm_min)

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    role = ar.user_have_access(uid)
    print(role)
    if role == 'manager':
        bot.reply_to(message, 'Здравствуйте!', reply_markup=keyboards.get_manager_keyboard())
    elif role == 'worker':
        bot.reply_to(message, 'Здравствуйте!', reply_markup=keyboards.get_employee_keyboard())
    else:
        bot.reply_to(message, 'У вас нет доступа. Обратитесь к администратору.')

@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    bot.reply_to(message, 'Спасибо!', reply_markup=keyboards.get_employee_keyboard())

@bot.message_handler(content_types=['text'])
def text_handler(message):
    uid = message.from_user.id
    role = ar.user_have_access(uid)
    if role:
        if message.text == localization.measure_temp:
            bot.reply_to(message, 'Введите вашу температуру:')
        elif not re.match(r'^-?\d+(?:\.\d+)?$', message.text) is None:
            ar.add_worker_temp(uid, message.text)
            bot.reply_to(message, 'Сфотографируйте термометр')
        elif message.text == localization.list_attach_employee:
            e_list = ar.get_manager_list(uid)['users']
            ans = 'Список сотрудников:\n'
            for u in e_list:
                ans += u['full_name'] + ' @' + u['telegram_nick'] + '\n'
            bot.reply_to(message, ans, reply_markup=keyboards.get_manager_keyboard())
        elif message.text == localization.common_stat:
            e_stat = ar.get_manager_stat(uid)['users']
            ans = ''
            for measure in e_stat:
                p_date = ''
                if 'date' in measure:
                    p_date = pretty_date(measure['date'])
                ans += measure['full_name'] + ' ' + str(measure['last_temp']) + ' ' + p_date + '\n'
            bot.reply_to(message, ans, reply_markup=keyboards.get_manager_keyboard())
    else:
        bot.reply_to(message, 'Wrong license code!')

@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://health-meters-bot.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
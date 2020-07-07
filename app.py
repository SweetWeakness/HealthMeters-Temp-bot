import os
import telebot
import re
import time
from flask import Flask, request

import stages as st
import database as db
import api_requests as ar
import keyboards

# Todo: вынести из кода
TOKEN = '1245516512:AAFAPDaDe2DwPgqTZxy4eanjSpLd5VigsUg'
bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)


def pretty_date(ugly_date):
    date = time.strptime(ugly_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    return '{}.{}.{} {}:{}'.format(date.tm_mday, date.tm_mon, date.tm_year, date.tm_hour, date.tm_min)


def temp_validation(temp):
    return not re.match(r'^-?\d+(?:\.\d+)?$', temp) is None


@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    uid = 1488

    role = "no access"
    companies = ar.get_companies_list(uid)

    if len(companies) != 0:
        role = ar.get_role(uid, companies[0])
        if role == "worker":
            role = "Role.WORKER"
            new_session.set_role(uid, st.Role.WORKER)
            new_session.set_role_stage(uid, st.Role.WORKER, st.WorkerStage.GET_TEMP)
        elif role == "manager":
            role = "Role.MANAGER"
            new_session.set_role(uid, st.Role.MANAGER)
            new_session.set_role_stage(uid, st.Role.MANAGER, st.ManagerStage.GET_INFO)

    if role == 'Role.WORKER':
        new_session.set_role_stage(uid, st.Role.WORKER, st.WorkerStage.GET_TEMP)
        bot.reply_to(message, 'Здравствуйте!', reply_markup=keyboards.get_employee_keyboard())
    elif role == 'Role.MANAGER':
        new_session.set_role_stage(uid, st.Role.MANAGER, st.ManagerStage.GET_INFO)
        bot.reply_to(message, 'Здравствуйте!', reply_markup=keyboards.get_manager_keyboard())
    else:
        bot.reply_to(message, 'У вас нет доступа. Обратитесь к администратору.')


@bot.message_handler(content_types=['text'])
def text_handler(message):
    # ToDo: изменить на проде
    uid = message.from_user.id
    uid = 1488

    role = new_session.get_role(uid)
    stage = new_session.get_role_stage(uid, role)
    # print(role)
    # print(stage)

    if role == "Role.WORKER":

        if stage == "WorkerStage.GET_TEMP":
            if message.text == 'Измерить температуру':
                new_session.set_role_stage(uid, st.Role.WORKER, st.WorkerStage.VALIDATION_TEMP)
                bot.reply_to(message, 'Введите вашу температуру (например, 36.6):',
                             reply_markup=keyboards.get_empty_keyboard())

        elif stage == "WorkerStage.VALIDATION_TEMP":
            if temp_validation(message.text):
                temp = float(message.text)
                if 35.0 < temp < 41.0:
                    new_session.set_role_stage(uid, st.Role.WORKER, st.WorkerStage.ACCEPT_TEMP)
                    bot.reply_to(message, "Ваша температура {}, все верно?".format(temp),
                                 reply_markup=keyboards.get_accept_temp_keyboard())
                else:
                    bot.reply_to(message, 'Неправильный ввод, вы не человек, введите еще раз.',
                                 reply_markup=keyboards.get_empty_keyboard())
            else:
                bot.reply_to(message, "Неправильный ввод, мб нормально введете? Введите еще раз.",
                             reply_markup=keyboards.get_empty_keyboard())

        elif stage == "WorkerStage.ACCEPT_TEMP":
            if message.text == 'Ошибка, щас исправлю':
                new_session.set_role_stage(uid, st.Role.WORKER, st.WorkerStage.VALIDATION_TEMP)
                bot.reply_to(message, 'Хорошо, введите вашу температуру еще раз:',
                             reply_markup=keyboards.get_empty_keyboard())

            elif message.text == 'Все верно':
                new_session.set_role_stage(uid, st.Role.WORKER, st.WorkerStage.GET_PHOTO)
                bot.reply_to(message, 'Отлично, жду фотку', reply_markup=keyboards.get_empty_keyboard())

    elif role == "Role.MANAGER":

        if stage == "ManagerStage.GET_INFO":
            if message.text == 'Вывести общую статистику':
                guid = ar.get_companies_list(uid)[0]
                e_stat = ar.get_workers_stats(uid, guid)
                ans = ''
                for measure in e_stat:
                    p_date = ''
                    if 'date' in measure:
                        p_date = pretty_date(measure['date'])
                    temp = '-'
                    if not re.match(r'^-?\d+(?:\.\d+)?$', str(measure['last_temp'])) is None:
                        temp = str(measure['last_temp'])
                    ans += '_' + measure['initials'] + '_ *' + temp + '* ' + p_date + '\n'
                bot.reply_to(message, ans, reply_markup=keyboards.get_manager_keyboard(), parse_mode='markdown')

            elif message.text == 'Запросить измерения температуры':
                guid = ar.get_companies_list(uid)[0]
                e_list = ar.get_attached_workers(uid, guid)
                for u in e_list:
                    print(u['telegram_id'])
                    bot.send_message(u['telegram_id'], 'Ваш менеджер просит измерить температуру!')

    else:
        bot.reply_to(message, 'Мб зарегаетесь для начала!')


@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    bot.reply_to(message, 'Спасибо!', reply_markup=keyboards.get_employee_keyboard())


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


webhook_url = 'https://ac71985b571d.ngrok.io' + '/' + TOKEN


# webhook_url = 'https://health-meters-bot.herokuapp.com/' + TOKEN


@server.route("/")
def webhook():
    print(bot.get_webhook_info())
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    print(bot.get_webhook_info())
    return "!", 200


if __name__ == "__main__":
    print(bot.get_webhook_info())
    new_session = db.SessionsStorage()
    server.run(host="127.0.0.1", port=int(os.environ.get('PORT', 80)))

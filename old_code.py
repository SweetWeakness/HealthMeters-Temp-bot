@bot.message_handler(content_types=['text'])
def text_handler(message):
    uid = message.from_user.user_id
    if ar.user_have_access(uid):
        stage = get_stage(uid)
        if stage == MAIN:
            if message.text == localization.add_employee:
                pass
            elif message.text == localization.delete_employee:
                pass
            elif message.text == localization.attach_employee:
                pass
            elif message.text == localization.list_employee:
                pass
            elif message.text == localization.stat:
                pass
            elif message.text == localization.license_info:
                pass
            elif message.text == localization.stat_employee:
                pass
            elif message.text == localization.list_attach_employee:
                pass
            elif message.text == localization.ask_temp:
                pass
            elif message.text == localization.measure_temp:
                pass
        elif stage == AddEmployeeStage.GET_NAME:
            set_stage_data(uid, AddEmployeeStage.GET_NAME, message.text)
            set_stage(uid, AddEmployeeStage.GET_USERNAME)
            bot.reply_to(message, 'Введите ник пользователя в Telegram')
        elif stage == AddEmployeeStage.GET_USERNAME:
            set_stage_data(uid, AddEmployeeStage.GET_USERNAME, message.text)
            set_stage(uid, AddEmployeeStage.GET_POSITION)
            bot.reply_to(message, 'Выберите роль', reply_markup=keyboards.get_role_choose_keyboard())
        elif stage == AddEmployeeStage.GET_POSITION:
            pass
        elif stage == DeleteEmployeeStage.GET_USERNAME:
            pass
        elif stage == AttachEmployeeStage.GET_MANAGER_USERNAME:
            set_stage_data(uid, AttachEmployeeStage.GET_MANAGER_USERNAME, message.text)
            set_stage(uid, AttachEmployeeStage.GET_USERNAME)
            bot.reply_to(message, 'Введите ник пользователя в Telegram')
        elif stage == AttachEmployeeStage.GET_USERNAME:
            pass
        elif stage == StatEmployeeStage.GET_USERNAME:
            pass
        elif stage == MeasureTempStage.GET_TEMP:
            set_stage_data(uid, MeasureTempStage.GET_TEMP, message.text)
            set_stage(uid, MeasureTempStage.GET_PHOTO)
            bot.reply_to(message, 'Подтвердите температуру фотографией')
        elif stage == MeasureTempStage.GET_PHOTO:
            pass
    else:
        bot.reply_to(message, 'Wrong license code!')
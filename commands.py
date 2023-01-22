default_city = 'Москва'


def start_command(message):
    if message.from_user.first_name:
        user = message.from_user.first_name
    elif message.from_user.username:
        user = message.from_user.username
    else:
        user = 'User'

    mess = f'Привет, <b>{user}</b> \n' \
           f'Чтобы узнать погоду в любом городе, ' \
           f'просто введите его название в сообщение к боту!\n' \
           f'Нажмите /help, чтобы узнать больше о командах бота'
    return mess

def mycity_command():
    return default_city

def change_mycity_command(message):
    pass

def help_command():
    mess = 'Данный бот показывает актуальную погоду в выбранном городе.\n' \
           'Чтобы узнать погоду в любом городе мира, ' \
           'просто введите его название в сообщение к боту!\n\n' \
           'Команды бота: \n' \
           f'/mycity - показать погоду в городе по умолчанию (сейчас "{default_city}")\n' \
           '/change_mycity (появится позже) - изменить город по умолчанию \n' \
           '/help - помощь с командами для бота'
    return mess

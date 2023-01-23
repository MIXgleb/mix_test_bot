def start_command(message):
    if message.from_user.first_name:
        user = message.from_user.first_name
    elif message.from_user.username:
        user = message.from_user.username
    else:
        user = 'User'

    mess = f'Привет, <b>{user}</b>! \n' \
           f'Чтобы узнать погоду в любом городе, ' \
           f'просто введите его название и отправьте боту!\n\n' \
           f"Нажмите /help или 'Помощь' в нижнем меню, чтобы узнать больше о боте"
    return mess


def mycity_command(default_city):
    return default_city


def change_mycity_command(default_city):
    mess = f"Сейчас Ваш город '{default_city}'!\nВведите город, на который хотите изменить"
    return mess


def help_command(default_city):
    mess = 'Данный бот показывает актуальную погоду в указанном городе.\n' \
           'Чтобы узнать погоду в любом городе, ' \
           'просто введите его название и отправьте боту!\n\n' \
           'Команды бота: \n' \
           f'/mycity - показать погоду в городе по умолчанию (сейчас "{default_city}")\n' \
           '/change_mycity - изменить город по умолчанию \n' \
           '/help - помощь, показать команды бота'
    return mess


def other_commands(message):
    mess = f"Команда '{message.text}' не распознана"
    return mess

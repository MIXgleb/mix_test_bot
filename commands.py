class Commands:
    @staticmethod
    def start(name, username):
        if name:
            user = name
        elif username:
            user = username
        else:
            user = 'User'

        mess = f'Привет, <b>{user}</b>! \n' \
               f'Данный бот поможет узнать погоду в любом городе, ' \
               f'просто введите название интересующего Вас города и отправьте боту!\n\n' \
               f"Нажмите /help или 'Помощь' в нижнем меню, чтобы узнать больше о боте"
        return mess

    @staticmethod
    def first_change(default_city):
        mess = "Для начала укажите Ваш город проживания\n" \
               f"По умолчанию указан город <b>{default_city}</b>\n" \
               "Хотите его поменять?"
        return mess

    @staticmethod
    def mycity(default_city):
        return default_city

    @staticmethod
    def change(default_city):
        mess = f"Сейчас Ваш город <b>{default_city}</b>!\n" \
               f"Введите город, на который хотите поменять\n"
        return mess

    @staticmethod
    def help(default_city):
        mess = 'Данный бот показывает актуальную погоду в указанном городе.\n' \
               'Чтобы узнать погоду в любом городе, ' \
               'просто введите его название и отправьте боту!\n\n' \
               'Команды бота: \n' \
               f'/mycity - показать погоду в городе по умолчанию (сейчас <b>{default_city}</b>)\n' \
               '/change_mycity - изменить город по умолчанию \n' \
               '/help - помощь, показать команды бота'
        return mess

    @staticmethod
    def other(text):
        mess = f"Команда <b>{text}</b> не распознана"
        return mess

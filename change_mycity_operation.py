import telebot
from collections import defaultdict
from decouple import config
from markups import Markups
from commands import Commands
from get_city_info import get_weather


bot = telebot.TeleBot(config('telegram_token'), parse_mode='html')


class MyCity:
    users_default_cities = defaultdict(lambda: "Москва")
    check_change_mycity = False

    @classmethod
    def prepare_change_mycity(cls, chat_id, user_id):
        cls.check_change_mycity = True
        bot.send_message(chat_id=chat_id,
                         text=Commands.change(cls.users_default_cities[user_id]),
                         reply_markup=Markups.cancel())

    @classmethod
    def change_mycity(cls, message):
        city = message.text
        chat_id = message.chat.id
        user_id = message.from_user.id
        default_city = cls.users_default_cities[user_id]
        response = get_weather(city)

        if not response['status']:
            bot.send_message(chat_id=chat_id,
                             text=f"Город <b>{city}</b> не найден!\n"
                                  "Попробуйте ввести другой",
                             reply_markup=Markups.cancel())
        elif default_city == response['city']:
            bot.send_message(chat_id=chat_id,
                             text=f"Данный город уже назначен!\n"
                                  "Попробуйте ввести другой",
                             reply_markup=Markups.cancel())
        else:
            cls.users_default_cities[user_id] = city
            cls.check_change_mycity = False
            bot.send_message(chat_id=chat_id,
                             text=f"Ваш город изменен на <b>{city}</b>",
                             reply_markup=Markups.plates())

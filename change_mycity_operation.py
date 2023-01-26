import telebot
from decouple import config
from markups import Markups
from commands import Commands
from get_city_info import get_weather


bot = telebot.TeleBot(config('telegram_token'), parse_mode='html')


class MyCity:
    default_city = 'Москва'
    check_change_mycity = False

    @classmethod
    def prepare_change_mycity(cls, chat_id):
        cls.check_change_mycity = True
        bot.send_message(chat_id=chat_id,
                         text=Commands.change(cls.default_city),
                         reply_markup=Markups.cancel())

    @classmethod
    def change_mycity(cls, message):
        city = message.text
        response = get_weather(city)

        if not response['status']:
            bot.send_message(chat_id=message.chat.id,
                             text=f"Город <b>{city}</b> не найден!\n"
                                  "Попробуйте ввести другой",
                             reply_markup=Markups.cancel())
        elif cls.default_city == response['city']:
            bot.send_message(chat_id=message.chat.id,
                             text=f"Данный город уже назначен!\n"
                                  "Попробуйте ввести другой",
                             reply_markup=Markups.cancel())
        else:
            cls.default_city = city
            cls.check_change_mycity = False
            bot.send_message(chat_id=message.chat.id,
                             text=f"Ваш город изменен на <b>{cls.default_city}</b>",
                             reply_markup=Markups.plates())

import telebot
from decouple import config
from markups import *
from commands import change_mycity_command
from get_city_info import get_weather


bot = telebot.TeleBot(config('telegram_token'), parse_mode='html')


class MyCity:
    default_city = 'Москва'
    check_change_mycity = False

    @staticmethod
    def prepare_change_mycity(chat_id):
        MyCity.check_change_mycity = True
        bot.send_message(chat_id=chat_id, text=change_mycity_command(MyCity.default_city),
                         reply_markup=reply_markup_change_mycity())

    @staticmethod
    def change_mycity(message):
        city = message.text
        response = get_weather(city)

        if not response['status']:
            bot.send_message(chat_id=message.chat.id,
                             text=f"Город <b>{city}</b> не найден!\n"
                                  "Попробуйте ввести другой",
                             reply_markup=reply_markup_change_mycity())
        elif MyCity.default_city == response['city']:
            bot.send_message(chat_id=message.chat.id,
                             text=f"Данный город уже назначен!\n"
                                  "Попробуйте ввести другой",
                             reply_markup=reply_markup_change_mycity())
        else:
            MyCity.default_city = city
            MyCity.check_change_mycity = False
            bot.send_message(chat_id=message.chat.id,
                             text=f"Ваш город изменен на <b>{MyCity.default_city}</b>",
                             reply_markup=reply_markup_plates())

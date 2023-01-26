import telebot
from requests import get
from decouple import config
from markups import Markups


bot = telebot.TeleBot(config('telegram_token'), parse_mode='html')
api_key = config('api_key')
url = config('url')


def get_city(chat_id, city):
    response = get_weather(city)

    if not response['status']:
        bot.send_message(chat_id=chat_id,
                         text=f"Город <b>{response['city']}</b> не найден.\n"
                              "Попробуйте заново",
                         reply_markup=Markups.plates())
    else:
        bot.send_message(chat_id=chat_id,
                         text=f'Город: <b>{response["city"]}</b> \n'
                         f'Температура: <b>{response["temp"]}&#176;</b> \n'
                         f'Ощущается как: <b>{response["feel"]}&#176;</b> \n'
                         f'<b>{response["descr"].capitalize()}</b>',
                         reply_markup=Markups.plates())


def get_weather(city):
    response = get(url,
                   params={'q': city,
                           'APPID': api_key,
                           'units': 'metric',
                           'lang': 'ru',
                           }).json()

    if response.get('message', 'OK') != 'OK':
        city_info = {
            'status': None,
            'city': city
        }
    else:
        city_info = {
            'status': 'ok',
            'city': response['name'],
            'temp': response['main']['temp'],
            'feel': response['main']['feels_like'],
            'descr': response['weather'][0]['description'],
        }

    return city_info

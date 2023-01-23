from requests import get
from decouple import config


api_key = config('api_key')
url = config('url')


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

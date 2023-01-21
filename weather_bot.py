from get_info import get_weather
from decouple import config
import telebot


bot = telebot.TeleBot(config('telegram_token'))
default_city = 'Москва'


@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.first_name:
        user = message.from_user.first_name
    else:
        user = message.from_user.username

    mess = f'Привет, <b>{user}</b> \n' \
           f'Чтобы узнать погоду в любом городе, ' \
           f'просто введите его название в поле для ввода \n' \
           f'Чтобы узнать больше о боте введите /help'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
    mess = 'Данный бот показывает актуальную погоду в выбранном городе. \n' \
           'Чтобы узнать погоду в любом городе, ' \
           'просто введите его название в поле для ввода \n\n' \
           'Команды бота: \n' \
           f'/default - показать погоду в городе по умолчанию (сейчас "{default_city}")\n' \
           '/change_default_city (появится позже) - изменить город по умолчанию \n' \
           '/help - помощь с коммандами для бота'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=['default'])
def check_default_city(message):
    get_user_city(message)


@bot.message_handler(commands=['change_default_city'])
def change_default_city(message):
    bot.send_message(message.chat.id, 'Данная возможность появится чуть позже')


@bot.message_handler(content_types=['text'])
def get_user_city(message):
    print(message.from_user.first_name)
    if message.text == '/default':
        city = default_city
    elif message.text[0] == '/':
        bot.send_message(message.chat.id, f'Команда не распознана')
        return
    else:
        city = message.text

    mess = get_weather(city)
    # photo = f'http://openweathermap.org/img/w/{mess["icon"]}.png'

    if not mess['status']:
        bot.send_message(message.chat.id, f'Город {mess["city"]} не найден. Попробуйте заново')
    else:
        bot.send_message(message.chat.id,
                         f'Город: <b>{mess["city"]}</b> \n'
                         f'Температура: <b>{mess["temp"]}&#176;</b> \n'
                         f'Ощущается как: <b>{mess["feel"]}&#176;</b> \n'
                         f'<b>{mess["descr"].capitalize()}</b>',
                         parse_mode='html')
        # bot.send_photo(message.chat.id, photo)


bot.polling(none_stop=True)

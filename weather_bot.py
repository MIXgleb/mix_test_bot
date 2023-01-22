import telebot
from telebot import types
from get_city_info import get_weather
from commands import start_command, help_command, change_mycity_command, mycity_command
from decouple import config


bot = telebot.TeleBot(config('telegram_token'))


@bot.message_handler(commands=['start', 'help', 'mycity', 'change_mycity'])
def check_commands(message):
    text = message.text
    if text == '/start':
        bot.send_message(message.chat.id, start_command(message), parse_mode='html')
    elif text == '/help':
        bot.send_message(message.chat.id, help_command())
    elif text == '/mycity':
        get_city(message, mycity_command())
    elif text == '/change_mycity':
        # bot.send_message(message.chat.id, 'Данная возможность появится чуть позже')
        bot.reply_to(message, 'Данная возможность появится чуть позже')
    buttons(message)


@bot.message_handler(func=lambda message: message.text[0] == '/')
def other_commands(message):
    bot.reply_to(message, 'Команда не распознана')
    buttons(message)


@bot.message_handler(content_types=['text'])
def get_user_city(message):
    print(message.from_user.first_name)
    get_city(message, message.text)
    buttons(message)


def get_city(message, city):
    response = get_weather(city)

    if not response['status']:
        bot.reply_to(message, f'Город {response["city"]} не найден. Попробуйте заново')
    else:
        bot.send_message(message.chat.id,
                         f'Город: <b>{response["city"]}</b> \n'
                         f'Температура: <b>{response["temp"]}&#176;</b> \n'
                         f'Ощущается как: <b>{response["feel"]}&#176;</b> \n'
                         f'<b>{response["descr"].capitalize()}</b>',
                         parse_mode='html')


def buttons(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('/mycity', callback_data='button_default_city')
    button2 = types.InlineKeyboardButton('/help', callback_data='button_help')
    markup.add(button1, button2)

    bot.send_message(message.chat.id, 'Помощь', reply_markup=markup)


bot.infinity_polling()

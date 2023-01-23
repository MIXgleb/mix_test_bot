import telebot
from get_city_info import get_weather
from commands import *
from buttons import reply_markup
from decouple import config


bot = telebot.TeleBot(config('telegram_token'))
default_city = 'Москва'
check_change_mycity = False


@bot.message_handler(commands=['start', 'help', 'mycity', 'change_mycity'])
def check_commands(message):
    global check_change_mycity
    text = message.text
    if text == '/start':
        bot.send_message(chat_id=message.chat.id, text=start_command(message),
                         reply_markup=reply_markup(), parse_mode='html')
    elif text == '/help':
        bot.send_message(chat_id=message.chat.id, text=help_command(default_city),
                         reply_markup=reply_markup())
    elif text == '/mycity':
        bot.send_chat_action(message.chat.id, 'typing')
        get_city(message, mycity_command(default_city))
    elif text == '/change_mycity':
        check_change_mycity = True
        bot.send_message(chat_id=message.chat.id, text=change_mycity_command(default_city))


@bot.message_handler(func=lambda message: message.text[0] == '/')
def other_commands(message):
    bot.send_message(chat_id=message.chat.id, text=other_commands(message),
                     reply_markup=reply_markup())


@bot.message_handler(content_types=['text'])
def check_user_text(message):
    global check_change_mycity

    if check_change_mycity:
        check_change_mycity = False
        change_mycity(message)

    text = message.text
    if text == 'Погода в моем городе':
        bot.send_chat_action(message.chat.id, 'typing')
        get_city(message, mycity_command(default_city))
    elif text == 'Изменить мой город':
        check_change_mycity = True
        bot.send_message(chat_id=message.chat.id, text=change_mycity_command(default_city))
    elif text == 'Помощь':
        bot.send_message(chat_id=message.chat.id, text=help_command(default_city),
                         reply_markup=reply_markup())
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        get_city(message, message.text)


def get_city(message, city):
    response = get_weather(city)

    if not response['status']:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Город '{response['city']}' не найден. Попробуйте заново",
                         reply_markup=reply_markup())
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=f'Город: <b>{response["city"]}</b> \n'
                         f'Температура: <b>{response["temp"]}&#176;</b> \n'
                         f'Ощущается как: <b>{response["feel"]}&#176;</b> \n'
                         f'<b>{response["descr"].capitalize()}</b>',
                         reply_markup=reply_markup(),
                         parse_mode='html')


def change_mycity(message):
    global default_city
    default_city = message.text
    bot.send_message(chat_id=message.chat.id,
                     text=f"Ваш город изменен на {default_city}",
                     reply_markup=reply_markup())

bot.infinity_polling()

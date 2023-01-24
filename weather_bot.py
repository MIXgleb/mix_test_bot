import telebot
import get_city_info
from markups import *
from commands import *
from decouple import config


bot = telebot.TeleBot(config('telegram_token'), parse_mode='html')
default_city = 'Москва'
check_change_mycity = False


@bot.message_handler(func=lambda message: message.text[0] == '/')
def check_commands(message):
    text = message.text
    if text == '/start':
        bot.send_message(chat_id=message.chat.id, text=start_command(message),
                         reply_markup=reply_markup())
        bot.send_message(chat_id=message.chat.id, text=first_change_mycity_command(default_city),
                         reply_markup=reply_markup_first_change_mycity())
    elif text == '/help':
        bot.send_message(chat_id=message.chat.id, text=help_command(default_city),
                         reply_markup=reply_markup())
    elif text == '/mycity':
        bot.send_chat_action(message.chat.id, 'typing')
        get_city(message, mycity_command(default_city))
    elif text == '/change_mycity':
        prepare_change_mycity(message.chat.id)
    else:
        bot.send_message(chat_id=message.chat.id, text=other_commands(message.text),
                         reply_markup=reply_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global check_change_mycity

    if call.data == 'cancel':
        check_change_mycity = False
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.from_user.id, text="Изменения отменены",
                         reply_markup=reply_markup())
        # bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id-1)
        # bot.answer_callback_query(call.id, text="Изменения отменены")
    elif call.data == 'yes':
        prepare_change_mycity(call.from_user.id)
    elif call.data == 'no':
        bot.send_message(chat_id=call.from_user.id, text=f"Ваш город сохранен как <b>{default_city}</b>")


@bot.message_handler(content_types=['text'])
def check_user_text(message):
    global check_change_mycity

    if check_change_mycity:
        bot.send_chat_action(message.chat.id, 'typing')
        change_mycity(message)
        return

    text = message.text.lower()
    if text == 'погода в моем городе':
        bot.send_chat_action(message.chat.id, 'typing')
        get_city(message, mycity_command(default_city))
    elif text == 'изменить мой город':
        check_change_mycity = True
        bot.send_message(chat_id=message.chat.id, text=change_mycity_command(default_city),
                         reply_markup=reply_markup_change_mycity())
    elif text == 'помощь':
        bot.send_message(chat_id=message.chat.id, text=help_command(default_city),
                         reply_markup=reply_markup())
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        get_city(message, message.text)


def get_city(message, city):
    response = get_city_info.get_weather(city)

    if not response['status']:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Город <b>{response['city']}</b> не найден.\n"
                              "Попробуйте заново",
                         reply_markup=reply_markup())
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=f'Город: <b>{response["city"]}</b> \n'
                         f'Температура: <b>{response["temp"]}&#176;</b> \n'
                         f'Ощущается как: <b>{response["feel"]}&#176;</b> \n'
                         f'<b>{response["descr"].capitalize()}</b>',
                         reply_markup=reply_markup())


def prepare_change_mycity(chat_id):
    global check_change_mycity
    check_change_mycity = True
    bot.send_message(chat_id=chat_id, text=change_mycity_command(default_city),
                     reply_markup=reply_markup_change_mycity())


def change_mycity(message):
    global default_city, check_change_mycity
    city = message.text
    response = get_city_info.get_weather(city)

    if not response['status']:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Город <b>{city}</b> не найден!\n"
                              "Попробуйте ввести другой",
                         reply_markup=reply_markup_change_mycity())
    elif default_city == response['city']:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Данный город уже назначен!\n"
                              "Попробуйте ввести другой",
                         reply_markup=reply_markup_change_mycity())
    else:
        default_city = city
        check_change_mycity = False
        bot.send_message(chat_id=message.chat.id,
                         text=f"Ваш город изменен на <b>{default_city}</b>",
                         reply_markup=reply_markup())


bot.infinity_polling()

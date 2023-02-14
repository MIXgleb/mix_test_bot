import telebot
from get_city_info import get_city
from markups import Markups
from commands import Commands
from decouple import config
from change_mycity_operation import MyCity


bot = telebot.TeleBot(config('telegram_token'), parse_mode='html')


@bot.message_handler(func=lambda message: message.text[0] == '/')
def check_commands(message):
    text = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id

    if text == '/start':
        bot.send_message(chat_id=chat_id,
                         text=Commands.start(name=message.from_user.first_name,
                                             username=message.from_user.username),
                         reply_markup=Markups.plates())
        bot.send_message(chat_id=chat_id,
                         text=Commands.first_change(default_city=MyCity.users_default_cities[user_id]),
                         reply_markup=Markups.start_change())
    elif text == '/help':
        bot.send_message(chat_id=chat_id,
                         text=Commands.help(default_city=MyCity.users_default_cities[user_id]),
                         reply_markup=Markups.plates())
    elif text == '/mycity':
        bot.send_chat_action(chat_id=chat_id, action='typing')
        get_city(chat_id=chat_id,
                 city=MyCity.users_default_cities[user_id])
    elif text == '/change_mycity':
        MyCity.prepare_change_mycity(chat_id=chat_id,
                                     user_id=user_id)
    else:
        bot.send_message(chat_id=chat_id,
                         text=Commands.other(text=message.text),
                         reply_markup=Markups.plates())


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.from_user.id
    user_id = chat_id

    if call.data == 'cancel':
        MyCity.check_change_mycity = False
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        bot.send_message(chat_id=chat_id,
                         text="Изменения отменены",
                         reply_markup=Markups.plates())
        # bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id-1)
        # bot.answer_callback_query(call.id, text="Изменения отменены")
    elif call.data == 'yes':
        MyCity.prepare_change_mycity(chat_id=chat_id, user_id=user_id)
    elif call.data == 'no':
        bot.send_message(chat_id=chat_id,
                         text=f"Ваш город сохранен как <b>{MyCity.users_default_cities[user_id]}</b>")


@bot.message_handler(content_types=['text'])
def check_user_text(message):
    text = message.text.lower()
    chat_id = message.chat.id
    user_id = message.from_user.id
    default_city = MyCity.users_default_cities[user_id]

    if MyCity.check_change_mycity:
        bot.send_chat_action(chat_id=chat_id,
                             action='typing')
        MyCity.change_mycity(message)
        return

    if text == 'погода в моем городе':
        bot.send_chat_action(chat_id=chat_id,
                             action='typing')
        get_city(message.chat.id, Commands.mycity(default_city=default_city))
    elif text == 'изменить мой город':
        MyCity.check_change_mycity = True
        bot.send_message(chat_id=chat_id,
                         text=Commands.change(default_city=default_city),
                         reply_markup=Markups.cancel())
    elif text == 'помощь':
        bot.send_message(chat_id=chat_id,
                         text=Commands.help(default_city=default_city),
                         reply_markup=Markups.plates())
    else:
        bot.send_chat_action(chat_id=chat_id,
                             action='typing')
        get_city(chat_id=message.chat.id, city=message.text)


bot.infinity_polling()

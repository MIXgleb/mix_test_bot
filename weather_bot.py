import telebot
from get_city_info import get_city
from markups import *
from commands import *
from decouple import config
from change_mycity_operation import MyCity


bot = telebot.TeleBot(config('telegram_token'), parse_mode='html')


@bot.message_handler(func=lambda message: message.text[0] == '/')
def check_commands(message):
    text = message.text
    if text == '/start':
        bot.send_message(chat_id=message.chat.id, text=start_command(message),
                         reply_markup=reply_markup_plates())
        bot.send_message(chat_id=message.chat.id, text=first_change_mycity_command(MyCity.default_city),
                         reply_markup=reply_markup_first_change_mycity())
    elif text == '/help':
        bot.send_message(chat_id=message.chat.id, text=help_command(MyCity.default_city),
                         reply_markup=reply_markup_plates())
    elif text == '/mycity':
        bot.send_chat_action(chat_id=message.chat.id, action='typing')
        get_city(message.chat.id, mycity_command(MyCity.default_city))
    elif text == '/change_mycity':
        MyCity.prepare_change_mycity(message.chat.id)
    else:
        bot.send_message(chat_id=message.chat.id, text=other_commands(message.text),
                         reply_markup=reply_markup_plates())


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'cancel':
        MyCity.check_change_mycity = False
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.from_user.id, text="Изменения отменены",
                         reply_markup=reply_markup_plates())
        # bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id-1)
        # bot.answer_callback_query(call.id, text="Изменения отменены")
    elif call.data == 'yes':
        MyCity.prepare_change_mycity(call.from_user.id)
    elif call.data == 'no':
        bot.send_message(chat_id=call.from_user.id, text=f"Ваш город сохранен как <b>{MyCity.default_city}</b>")


@bot.message_handler(content_types=['text'])
def check_user_text(message):
    if MyCity.check_change_mycity:
        bot.send_chat_action(message.chat.id, 'typing')
        MyCity.change_mycity(message)
        return

    text = message.text.lower()
    if text == 'погода в моем городе':
        bot.send_chat_action(message.chat.id, 'typing')
        get_city(message.chat.id, mycity_command(MyCity.default_city))
    elif text == 'изменить мой город':
        MyCity.check_change_mycity = True
        bot.send_message(chat_id=message.chat.id, text=change_mycity_command(MyCity.default_city),
                         reply_markup=reply_markup_change_mycity())
    elif text == 'помощь':
        bot.send_message(chat_id=message.chat.id, text=help_command(MyCity.default_city),
                         reply_markup=reply_markup_plates())
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        get_city(message.chat.id, message.text)


bot.infinity_polling()

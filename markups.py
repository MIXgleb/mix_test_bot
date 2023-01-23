from telebot import types


def reply_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, selective=True)
    button1 = types.KeyboardButton('Погода в моем городе')
    button2 = types.KeyboardButton('Изменить мой город')
    button3 = types.KeyboardButton('Помощь')
    markup.add(button1, button2, button3)
    return markup


def reply_markup_change_mycity():
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Отменить изменение', callback_data='cancel')
    markup.add(button)
    return markup

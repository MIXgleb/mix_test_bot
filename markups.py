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
    button1 = types.InlineKeyboardButton(text='Отменить изменение', callback_data='cancel')
    markup.add(button1)
    return markup


def reply_markup_first_change_mycity():
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton(text='Да', callback_data='yes')
    button2 = types.InlineKeyboardButton(text='Нет', callback_data='no')
    markup.add(button1, button2)
    return markup

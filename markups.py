from telebot import types


def reply_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('Погода в моем городе')
    button2 = types.KeyboardButton('Изменить мой город')
    button3 = types.KeyboardButton('Помощь')
    markup.add(button1, button2, button3)
    return markup

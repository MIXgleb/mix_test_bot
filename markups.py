from telebot import types


class Markups:
    @staticmethod
    def plates():
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, selective=True)
        button1 = types.KeyboardButton('Погода в моем городе')
        button2 = types.KeyboardButton('Изменить мой город')
        button3 = types.KeyboardButton('Помощь')
        markup.add(button1, button2, button3)
        return markup

    @staticmethod
    def cancel():
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Отменить изменение', callback_data='cancel')
        markup.add(button1)
        return markup

    @staticmethod
    def start_change():
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton(text='Да', callback_data='yes')
        button2 = types.InlineKeyboardButton(text='Нет', callback_data='no')
        markup.add(button1, button2)
        return markup

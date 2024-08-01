import telebot
from telebot import types
import data


bot = telebot.TeleBot(data.token)


@bot.message_handler(commands=['start'])
def my_start(message):
    bot.reply_to(message, data.start_text)
    build_keyboard(message, data.errors_names)


@bot.message_handler(commands=['help'])
def my_help(message):
    bot.reply_to(message, data.help_text)


@bot.message_handler(content_types=['text'])
def error_manager(message):
    try:
        if message.text in data.errors_names:
            write_text(message, data.errors_text[message.text])
        else:
            write_text(message, data.hack_try)
    except Exception:
        text = 'Программа вышла из чата. Просьба призвать богов ИКТ, они помогут'
        bot.reply_to(message, text)


def build_keyboard(message, this_dict):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for key in this_dict:
        new_btn = types.KeyboardButton(key)
        markup.add(new_btn)

    bot.send_message(message.from_user.id, "Надо выбрать что-то из списка:", reply_markup=markup)


def write_text(message, string):
    f = open("log.txt", 'a')
    f.write(string + '\n')
    f.close()
    bot.send_message(message.from_user.id, string, reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    bot.polling(none_stop=True)

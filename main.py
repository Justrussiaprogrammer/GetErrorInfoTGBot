import telebot
from telebot import types
import data


bot = telebot.TeleBot(data.token)
level = 0
search_error = ""


@bot.message_handler(commands=['start'])
def my_start(message):
    write_text(message, data.start_text)


@bot.message_handler(commands=['get'])
def my_get(message):
    build_keyboard(message, data.errors_1)


@bot.message_handler(commands=['help'])
def my_help(message):
    write_text(message, data.help_text)


@bot.message_handler(commands=['reboot'])
def my_reboot(message):
    global level, search_error

    level = 0
    search_error = ""
    bot.send_message(message.from_user.id, "Поиск ошибки начат заново", reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def error_manager(message):
    global search_error, level

    try:
        match level:
            case 0:
                if message.text in data.errors_1:
                    # print('fdjkfredf')
                    write_text(message, data.errors_text[message.text][0])
                    # print(222)
                    search_error = message.text
                    if data.errors_text[message.text][1] == 0:
                        level += 1
                        build_keyboard(message, data.errors_2[message.text])
                    else:
                        level = 0
                else:
                    write_text(message, data.hack_try)
            case 1:
                if message.text in data.errors_2[search_error]:
                    write_text(message, data.errors_text[message.text][0])
                    search_error = message.text
                    if data.errors_text[message.text][1] == 0:
                        level += 1
                        build_keyboard(message, data.errors_3[message.text])
                    else:
                        level = 0
                else:
                    write_text(message, data.hack_try)
            case 2:
                if message.text in data.errors_3[search_error]:
                    write_text(message, data.errors_text[message.text][0])
                    level = 0
                    search_error = ""
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

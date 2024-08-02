import pandas as pd
import telebot
from telebot import types
import texts


bot = telebot.TeleBot(texts.token)


@bot.message_handler(commands=['start'])
def my_start(message):
    global users

    if users[users["user_id"] == message.chat.id].empty:
        new_data = pd.DataFrame({"user_id": [message.chat.id], "level": [0], "search_error": [0]})
        new_data.to_csv('data.csv', mode='a', header=False, index=False)
        users = pd.read_csv('data.csv')
        print("The end of registration")
    write_text(message, texts.start_text)
    my_reboot(message)


@bot.message_handler(commands=['get'])
def my_get(message):
    build_keyboard(message, texts.errors_list[0])


@bot.message_handler(commands=['help'])
def my_help(message):
    write_text(message, texts.help_text)


@bot.message_handler(commands=['reboot'])
def my_reboot(message):
    global users

    users.loc[users["user_id"] == message.chat.id, "search_error"] = 0
    users.loc[users["user_id"] == message.chat.id, "level"] = 0
    users.to_csv('data.csv', index=False)
    bot.send_message(message.chat.id, "Поиск ошибки начат заново", reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def error_manager(message):
    global users

    print('Start of reading function')
    user = users[users["user_id"] == message.chat.id]
    level = user["level"].values[0]
    search_error = user["search_error"].values[0]
    try:
        word = texts.name_digit[message.text]
        if word in texts.errors_list[search_error]:
            write_text(message, texts.error_text[word])
            if word in texts.errors_list:
                level += 1
                build_keyboard(message, texts.errors_list[word])
                users.loc[users["user_id"] == message.chat.id, "search_error"] = word
            else:
                users.loc[users["user_id"] == message.chat.id, "search_error"] = 0
                level = 0
            users.loc[users["user_id"] == message.chat.id, "level"] = level
            users.to_csv('data.csv', index=False)
        else:
            write_text(message, texts.hack_try)
    except Exception:
        bot.reply_to(message, texts.fatal_text)
    print("End of reading function")


def build_keyboard(message, this_dict):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for key in this_dict:
        new_btn = types.KeyboardButton(texts.digit_name[key])
        markup.add(new_btn)

    bot.send_message(message.chat.id, "Надо выбрать что-то из списка:", reply_markup=markup)


def write_text(message, string):
    f = open("log.txt", 'a')
    f.write(string + '\n')
    f.close()
    bot.send_message(message.chat.id, string, reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    users = pd.read_csv('data.csv')
    bot.polling(none_stop=True)

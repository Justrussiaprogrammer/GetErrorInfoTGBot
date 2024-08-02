import telebot
from telebot import types
import texts
import pandas as pd


bot = telebot.TeleBot(texts.token)


@bot.message_handler(commands=['start'])
def my_start(message):
    global users

    if users[users["user_id"] == message.chat.id].empty:
        new_data = pd.DataFrame({"user_id": [message.chat.id], "level": [0], "search_error": [None]})
        new_data.to_csv('data.csv', mode='a', header=False, index=False)
        users = pd.read_csv('data.csv')
        print("The end of registration")
    write_text(message, texts.start_text)
    my_reboot(message)


@bot.message_handler(commands=['get'])
def my_get(message):
    build_keyboard(message, texts.errors_1)


@bot.message_handler(commands=['help'])
def my_help(message):
    write_text(message, texts.help_text)


@bot.message_handler(commands=['reboot'])
def my_reboot(message):
    global users

    users.loc[users["user_id"] == message.chat.id, "search_error"] = None
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
        match level:
            case 0:
                if message.text in texts.errors_1:
                    write_text(message, texts.errors_text[message.text][0])

                    if texts.errors_text[message.text][1] == 0:
                        level += 1
                        build_keyboard(message, texts.errors_2[message.text])
                    else:
                        level = 0
                    users.loc[users["user_id"] == message.chat.id, "search_error"] = message.text
                    users.loc[users["user_id"] == message.chat.id, "level"] = level
                else:
                    write_text(message, texts.hack_try)
            case 1:
                if message.text in texts.errors_2[search_error]:
                    write_text(message, texts.errors_text[message.text][0])
                    if texts.errors_text[message.text][1] == 0:
                        level += 1
                        build_keyboard(message, texts.errors_3[message.text])
                        users.loc[users["user_id"] == message.chat.id, "search_error"] = message.text
                    else:
                        users.loc[users["user_id"] == message.chat.id, "search_error"] = None
                        level = 0
                    users.loc[users["user_id"] == message.chat.id, "level"] = level
                else:
                    print('see here')
                    write_text(message, texts.hack_try)
            case 2:
                if message.text in texts.errors_3[search_error]:
                    write_text(message, texts.errors_text[message.text][0])
                    if texts.errors_text[message.text][1] == 0:
                        level += 1
                        build_keyboard(message, texts.errors_3[message.text])
                        users.loc[users["user_id"] == message.chat.id, "search_error"] = message.text
                    else:
                        users.loc[users["user_id"] == message.chat.id, "search_error"] = None
                        level = 0
                    users.loc[users["user_id"] == message.chat.id, "level"] = level
                else:
                    write_text(message, texts.hack_try)
        users.to_csv('data.csv', index=False)
    except Exception:
        bot.reply_to(message, texts.fatal_text)
    print("End of reading function")


def build_keyboard(message, this_dict):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for key in this_dict:
        new_btn = types.KeyboardButton(key)
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

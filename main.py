import json
import functions
import pandas as pd
import sqlite3
import telebot
from telebot import types
import texts
import yaml


f = open("config.yaml", "r")
conf = yaml.safe_load(f)
f.close()
bot = telebot.TeleBot(conf["token"])


@bot.message_handler(commands=['start'])
def my_start(message):
    global users

    if users[users["user_id"] == message.chat.id].empty:
        new_data = pd.DataFrame({"user_id": [message.chat.id], "level": [0], "search_error": [0]})
        new_data.to_csv('data.csv', mode='a', header=False, index=False)
        users = pd.read_csv('data.csv')

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Users (user_id, level, search_error, action) VALUES (?, ?, ?, ?)',
                       (message.chat.id, 0, "0", 0))
        connection.commit()
        connection.close()
        print("The end of registration")
    write_text(message, lines.start_text)


@bot.message_handler(commands=['get'])
def my_get(message):
    build_keyboard(message, errors_list[0], lines.keyboard_text)


@bot.message_handler(commands=['help'])
def my_help(message):
    write_text(message, lines.help_text)


@bot.message_handler(commands=['fix'])
def my_fix(message):
    global local_data

    local_data = data
    users.loc[users["user_id"] == message.chat.id, "action"] = 1
    build_keyboard(message, [-2] + errors_list[0], lines.add_text)


@bot.message_handler(commands=['reboot'])
def my_reboot(message):
    global data, local_data, error_text, name_digit, digit_name, errors_list
    users.loc[users["user_id"] == message.chat.id, "search_error"] = 0
    users.loc[users["user_id"] == message.chat.id, "level"] = 0
    users.loc[users["user_id"] == message.chat.id, "action"] = 0
    users.to_csv('data.csv', index=False)
    texts.error_text = dict()

    data, local_data, error_text, name_digit, digit_name, errors_list = functions.__reboot()
    bot.send_message(message.chat.id, lines.reboot_text, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def error_manager(message):
    global users, local_data, conf

    user = users[users["user_id"] == message.chat.id]
    level = user["level"].values[0]
    search_error = user["search_error"].values[0]
    action = user["action"].values[0]
    try:
        match action:
            case 3:
                local_data["text"] = message.text
                write_text(message, lines.name_text_end)
                fd = open('info.json', 'w')
                json.dump(data, fd, ensure_ascii=False, indent=2)
                fd.close()
                my_reboot(message)
            case 2:
                if search_error == -2:
                    if level == 0:
                        local_data[message.text] = {"text": "", "status": 1, "next": {}}
                        if len(local_data) >= conf["base"]:
                            conf["base"] *= 2
                        local_data = local_data[message.text]
                    else:
                        local_data["next"][message.text] = {"text": "", "status": 1, "next": {}}
                        if len(local_data["next"]) >= conf["base"]:
                            conf["base"] *= 2
                        local_data = local_data["next"][message.text]
                    write_text(message, lines.instruction_text)
                    fd = open('test.yaml', 'w')
                    yaml.dump(conf, fd)
                    fd.close()
                    users.loc[users["user_id"] == message.chat.id, "action"] = 3
                else:
                    local_data["text"] = message.text
                    write_text(message, lines.name_text_end)
                    fd = open('info.json', 'w')
                    json.dump(data, fd, ensure_ascii=False, indent=2)
                    fd.close()
                    my_reboot(message)
            case 1:
                word = name_digit[message.text]
                if word < 0:
                    users.loc[users["user_id"] == message.chat.id, "search_error"] = word
                    users.loc[users["user_id"] == message.chat.id, "action"] = 2
                    if word == -2:
                        write_text(message, lines.name_text)
                    else:
                        write_text(message, lines.info_text)
                elif word in errors_list[search_error]:
                    if level == 0:
                        texts.local_data = local_data[message.text]
                    else:
                        texts.local_data = local_data["next"][message.text]
                    level += 1
                    users.loc[users["user_id"] == message.chat.id, "level"] = level
                    users.loc[users["user_id"] == message.chat.id, "search_error"] = word
                    if word in errors_list:
                        build_keyboard(message, [-2, -1] + errors_list[word], lines.keyboard_text)
                    else:
                        build_keyboard(message, [-2, -1], lines.keyboard_text)
                else:
                    write_text(message, lines.hack_try)
            case 0:
                word = name_digit[message.text]
                if word in errors_list[search_error]:
                    write_text(message, error_text[word])
                    if word in errors_list:
                        level += 1
                        build_keyboard(message, errors_list[word], lines.keyboard_text)
                        users.loc[users["user_id"] == message.chat.id, "search_error"] = word
                    else:
                        users.loc[users["user_id"] == message.chat.id, "search_error"] = 0
                        level = 0
                        my_get(message)
                    users.loc[users["user_id"] == message.chat.id, "level"] = level
                else:
                    write_text(message, lines.hack_try)
        users.to_csv('data.csv', index=False)
    except Exception:
        bot.reply_to(message, lines.fatal_text)


def build_keyboard(message, this_dict, string):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for key in this_dict:
        new_btn = types.KeyboardButton(digit_name[key])
        markup.add(new_btn)

    bot.send_message(message.chat.id, string, reply_markup=markup)


def write_text(message, string):
    fd = open("log.txt", 'a')
    fd.write(string + '\n')
    fd.close()
    bot.send_message(message.chat.id, string, reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    users = pd.read_csv('data.csv')
    f = open('config.yaml', 'r')
    conf = yaml.safe_load(f)
    f.close()

    lines = texts.Texts()
    data, local_data, error_text, name_digit, digit_name, errors_list = functions.__reboot()

    bot.polling(none_stop=True)

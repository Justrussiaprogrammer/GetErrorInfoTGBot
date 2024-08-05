import json
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
    build_keyboard(message, texts.errors_list[0], texts.keyboard_text)


@bot.message_handler(commands=['help'])
def my_help(message):
    write_text(message, texts.help_text)


@bot.message_handler(commands=['fix'])
def my_fix(message):
    texts.ACTION = 1
    texts.local_data = texts.data
    build_keyboard(message, [-2] + texts.errors_list[0], texts.add_text)


@bot.message_handler(commands=['reboot'])
def my_reboot(message):
    global users

    users.loc[users["user_id"] == message.chat.id, "search_error"] = 0
    users.loc[users["user_id"] == message.chat.id, "level"] = 0
    users.to_csv('data.csv', index=False)
    texts.error_text = dict()

    texts.__reboot()
    bot.send_message(message.chat.id, "Произведен ребут", reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def error_manager(message):
    global users

    # print('Start of reading function')
    user = users[users["user_id"] == message.chat.id]
    level = user["level"].values[0]
    search_error = user["search_error"].values[0]
    try:
        match texts.ACTION:
            case 3:
                texts.local_data["text"] = message.text
                write_text(message, "Описание ошибки успешно заменено")
                f = open('info.json', 'w')
                json.dump(texts.data, f, ensure_ascii=False, indent=2)
                f.close()
                my_reboot(message)
            case 2:
                if search_error == -2:
                    if level == 0:
                        texts.local_data[message.text] = {"text": "", "status": 1, "next": {}}
                        texts.local_data = texts.local_data[message.text]
                    else:
                        texts.local_data["next"][message.text] = {"text": "", "status": 1, "next": {}}
                        texts.local_data = texts.local_data["next"][message.text]
                    write_text(message, texts.instruction_text)
                    texts.ACTION = 3
                else:
                    texts.local_data["text"] = message.text
                    write_text(message, "Описание ошибки успешно заменено")
                    f = open('info.json', 'w')
                    json.dump(texts.data, f, ensure_ascii=False, indent=2)
                    f.close()
                    my_reboot(message)
            case 1:
                word = texts.name_digit[message.text]
                if word < 0:
                    texts.ACTION = 2
                    users.loc[users["user_id"] == message.chat.id, "search_error"] = word
                    write_text(message, texts.name_text)
                elif word in texts.errors_list[search_error]:
                    if level == 0:
                        texts.local_data = texts.local_data[message.text]
                    else:
                        texts.local_data = texts.local_data["next"][message.text]
                    level += 1
                    users.loc[users["user_id"] == message.chat.id, "level"] = level
                    users.loc[users["user_id"] == message.chat.id, "search_error"] = word
                    if word in texts.errors_list:
                        build_keyboard(message, [-2, -1] + texts.errors_list[word], texts.keyboard_text)
                    else:
                        build_keyboard(message, [-2, -1], texts.keyboard_text)
                else:
                    write_text(message, texts.hack_try)
            case 0:
                word = texts.name_digit[message.text]
                if word in texts.errors_list[search_error]:
                    write_text(message, texts.error_text[word])
                    if word in texts.errors_list:
                        level += 1
                        build_keyboard(message, texts.errors_list[word], texts.keyboard_text)
                        users.loc[users["user_id"] == message.chat.id, "search_error"] = word
                    else:
                        users.loc[users["user_id"] == message.chat.id, "search_error"] = 0
                        level = 0
                        my_get(message)
                    users.loc[users["user_id"] == message.chat.id, "level"] = level
                else:
                    write_text(message, texts.hack_try)
        users.to_csv('data.csv', index=False)
    except Exception:
        bot.reply_to(message, texts.fatal_text)
    # print("End of reading function")


def build_keyboard(message, this_dict, string):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for key in this_dict:
        new_btn = types.KeyboardButton(texts.digit_name[key])
        markup.add(new_btn)

    bot.send_message(message.chat.id, string, reply_markup=markup)


def write_text(message, string):
    f = open("log.txt", 'a')
    f.write(string + '\n')
    f.close()
    bot.send_message(message.chat.id, string, reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    users = pd.read_csv('data.csv')
    bot.polling(none_stop=True)

import json


def DFS(last, local_dict):
    global name_digit, digit_name, error_text, errors_list

    pos = 1
    for key in local_dict:
        name_digit[key] = BASE * name_digit[last] + pos
        digit_name[BASE * name_digit[last] + pos] = key
        error_text[name_digit[key]] = local_dict[key]["text"]
        if name_digit[last] not in errors_list:
            errors_list[name_digit[last]] = list()
        errors_list[name_digit[last]].append(name_digit[key])
        pos += 1
        for elem in local_dict[key]["next"]:
            DFS(key, elem)


NAME = 'GetErrorInfo'
TEG = 'GetErrorInfo_bot'
token = '7198556498:AAFikKiDB8ncUUkWkz4kwAbpEkkzMSw4Ne4'

start_text = ('Бот предназначен для получения данных о возможных ошибках и способах их решения\n'
              'Используйте команду /help для получения информации о работе бота\n'
              "При вызове этой команды дополнительно применятся команда /reboot\n")
help_text = ("Вот список команд бота:\n"
             "/get - начинает процесс поиска решения ошибки\n"
             "/help - выводит это сообщение\n"
             "/start - выводит стартовое сообщение и позволяет получить информацию об ошибках\n"
             "/reboot - обнуляет все процессы, вместе с файлом лога\n")
hack_try = "Вы вводите что-то не по протоколу, просьба повторить попытку в правильном порядке"
fatal_text = "Программа вышла из чата. Просьба призвать богов ИКТ, они помогут"


BASE = 10

error_text = dict()

f = open('info.json')
data = json.load(f)
f.close()

name_digit = dict()
name_digit[0] = 0
digit_name = dict()
digit_name[0] = 0
errors_list = dict()

DFS(0, data)

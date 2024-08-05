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
        DFS(key, local_dict[key]["next"])


def __reboot():
    global local_data, ACTION, error_text, data, name_digit, digit_name, errors_list

    f = open('info.json')
    data = json.load(f)
    f.close()

    local_data = dict()
    ACTION = 0
    error_text = dict()
    name_digit = dict()
    name_digit[0] = 0
    name_digit["Добавить ошибку"] = -2
    name_digit["Обновить описание"] = -1
    digit_name = dict()
    digit_name[0] = 0
    digit_name[-2] = "Добавить ошибку"
    digit_name[-1] = "Обновить описание"
    errors_list = dict()

    DFS(0, data)


BASE = 10
ACTION = 0
local_data = dict()
NAME = 'GetErrorInfo'
TEG = 'GetErrorInfo_bot'
token = '7198556498:AAFikKiDB8ncUUkWkz4kwAbpEkkzMSw4Ne4'

start_text = ('Бот предназначен для получения данных о возможных ошибках и способах их решения\n'
              'Используйте команду /help для получения информации о работе бота\n'
              "При вызове этой команды дополнительно применятся команда /reboot\n")
help_text = ("Вот список команд бота:\n"
             "/fix - меняет описания ошибок или добавляет новые\n"
             "/get - начинает процесс поиска решения ошибки\n"
             "/help - выводит это сообщение\n"
             "/start - выводит стартовое сообщение и позволяет получить информацию об ошибках\n"
             "/reboot - обнуляет все процессы, вместе с файлом лога\n")
reboot_text = "Произведен ребут"
add_text = "Выберите вариант ошибки, в категории которой вы хотите поменять текст:"
name_text = "Напишите название ошибки"
info_text = "Напишите новое введение для решения ошибки"
name_text_end = "Описание ошибки успешно заменено"
instruction_text = "Добавлена новая ошибка с пустым описанием. Напишите путь решения проблемы"
keyboard_text = "Надо выбрать что-то из списка:"
change_text = "Изменить описание ошибки"
next_text = "Выбрать подраздел текущей ошибки"
hack_try = "Вы вводите что-то не по протоколу, просьба повторить попытку в правильном порядке"
fatal_text = "Программа вышла из чата. Просьба призвать богов ИКТ, они помогут"
already_error = "В этой категории уже есть такая ошибка, введите название ещё раз"

error_text = dict()
data = dict()
name_digit = dict()
digit_name = dict()
errors_list = dict()
__reboot()

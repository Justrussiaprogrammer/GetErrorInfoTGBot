import json
import yaml


def DFS(last, base, local_dict, name_digit, digit_name, error_text, errors_list):
    pos = 1
    for key in local_dict:
        name_digit[key] = base * name_digit[last] + pos
        digit_name[base * name_digit[last] + pos] = key
        error_text[name_digit[key]] = local_dict[key]["text"]
        if name_digit[last] not in errors_list:
            errors_list[name_digit[last]] = list()
        errors_list[name_digit[last]].append(name_digit[key])
        pos += 1
        DFS(key, base, local_dict[key]["next"], name_digit, digit_name, error_text, errors_list)


def __reboot():
    fd = open('info.json')
    data = json.load(fd)
    fd.close()
    fd = open('config.yaml', 'r')
    conf = yaml.safe_load(fd)
    fd.close()

    local_data = dict()
    error_text = dict()
    name_digit = dict()
    name_digit["0"] = 0
    name_digit["Добавить ошибку"] = -2
    name_digit["Обновить описание"] = -1
    digit_name = dict()
    digit_name[0] = 0
    digit_name[-2] = "Добавить ошибку"
    digit_name[-1] = "Обновить описание"
    errors_list = dict()

    DFS("0", conf["base"], data, name_digit, digit_name, error_text, errors_list)

    return data, local_data, error_text, name_digit, digit_name, errors_list


def write_to_file(filename, local_dict, depth):
    for key in local_dict:
        fd = open(filename, 'a')
        fd.write(depth * '\t' + key + '\n')
        all_lines = local_dict[key]["text"].split('\n')
        for line in all_lines:
            if len(line) > 1:
                fd.write((depth + 1) * '\t' + line + '\n')
        fd.close()
        write_to_file(filename, local_dict[key]["next"], depth + 1)


def do_offer_text(message):
    return "Пришло сообщение от пользователя " + str(message.chat.id) + " с текстом <" + message.text + ">\n"


def get_error_text(string):
    return "Текущее описание ошибки: <" + string + ">\n"

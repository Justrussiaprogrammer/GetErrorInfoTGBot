from dataclasses import dataclass


@dataclass(frozen=True)
class Texts:
    start_text: str = ("Бот предназначен для получения данных о возможных ошибках и способах их решения\n"
                       "Используйте команду /help для получения информации о работе бота\n"
                       "При вызове этой команды дополнительно применятся команда /reboot\n")
    help_text: str = ("Вот список команд бота:\n"
                      "/fix - меняет описания ошибок или добавляет новые\n"
                      "/get - начинает процесс поиска решения ошибки\n"
                      "/help - выводит это сообщение\n"
                      "/start - выводит стартовое сообщение и позволяет получить информацию об ошибках\n"
                      "/reboot - откатывает все процессы в случае возникновения каких-либо ошибок\n")
    reboot_text: str = "Произведен откат"
    add_text: str = "Выберите вариант ошибки, в категории которой вы хотите поменять текст:"
    name_text: str = "Напишите название ошибки"
    name_end_text: str = "Описание ошибки готово"
    info_text: str = "Напишите новое введение для решения ошибки"
    instruction_text: str = "Добавлена новая ошибка с пустым описанием. Напишите путь решения проблемы"
    keyboard_text: str = "Надо выбрать что-то из списка:"
    hack_text: str = "Вы вводите что-то не по протоколу, просьба повторить попытку в правильном порядке"
    no_admin_text: str = "Чтобы выполнить это действие, вам необходимо быть администратором"
    fatal_text: str = "Программа вышла из чата. Просьба призвать богов ИКТ, они помогут"

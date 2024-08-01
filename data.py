name = 'GetErrorInfo'
teg = 'GetErrorInfo_bot'
token = '7198556498:AAFikKiDB8ncUUkWkz4kwAbpEkkzMSw4Ne4'


start_text = ('Бот предназначен для получения данных о возможных ошибках и способах их решения\n'
              'Используйте команду /help для получения информации о работе бота')
help_text = ("Вот список команд бота:\n"
             "/start - выводит стартовое сообщение и позволяет получить информацию об ошибках\n")
hack_try = "Для получения информации об ошибке необходимо нажать на соответствующую кнопку"

errors_names = list()
errors_names.append("GameCore")
errors_names.append("Видео")
errors_names.append("Страница управления")
errors_names.append("Сервер")
errors_names.append("GUI")
errors_names.append("Дроны")

# errors_names_cases = dict()
# errors_names_cases["GameCore"] = ["Нет доступа к ядру"]
# errors_names_cases["Видео"] = []
# errors_names_cases["Страница управления"] = []
# errors_names_cases["Сервер"] = []
# errors_names_cases["GUI"] = []
# errors_names_cases["Дроны"] = []

errors_text = dict()
errors_text["GameCore"] = ("1. Нет доступа к ядру\n"
                           "    - Проверить, запущен ли GameCore.\n"
                           "    - Если запущен, но все равно написано, что нет доступа к ядру, проверьте, "
                           "что в config.py (из geoscan_arena_control) правильно указан адрес GameCore.\n")

errors_text["Видео"] = ("1. Не подключается видео\n"
                        "   - Открыть консоль в браузере\n"
                        "   1.1. В консоли ошибка peer id … not found\n"
                        "       - Проверить, запущен ли на стойке вебсокет сервер для webrtc\n"
                        "       - Если запущен, то возможно дрон/робот отключен\n"
                        "       - Перезапустить вебсокет сервер на стойке\n"
                        "       - Проверить работоспособность точки доступа\n"
                        "   1.2. В консоли нет ошибки peer id … not found, есть ответы\n"
                        "   - Попробовать подключиться через другой браузер (можно использовать Chrome, Yandex и\n"
                        "     другие браузеры на движке chromium (но точно работает только на первых двух)) или\n"
                        "     перезагрузить текущий\n"
                        "   - Возможно умер внешний turn сервер. Придется искать новый и везде его менять (websend.py\n"
                        "     на роботах и video_player.js в gesocan_arena_control)\n"
                        "2. Не работают камеры тренера\n"
                        "   - На сервере ввести sudo systemctl restart ptz-server.service\n")
errors_text["Страница управления"] = ("1. При переходе на страницу управления выпадает ошибка 404\n"
                                      "    - Проверьте правильность адреса\n"
                                      "2. При переходе на страницу управления выпадает ошибка 50х\n"
                                      "    - Что-то упало (geoscan_arena_control). Нужно поднять\n")
errors_text["Сервер"] = ("1. Не удается получить доступ к сайту (превышено время ожидания)\n"
                         "    - Что-то случилось с pfSense (зовите знающего человека)\n"
                         "2. Не работает DHCP или сломался интернет\n"
                         "    - Проверить линк на 28 порту и, если никого нет в серверной, то перезагрузить сервер\n")

errors_text["GUI"] = ("1. Зависло\n"
                      "    - Убить через диспетчер задач\n"
                      "    - Запустить заново\n"
                      "    - Чтобы не отваливалось во время игры, лучше перезапускать перед каждой игрой\n")
errors_text["Дроны"] = ("1. Не взлетает\n"
                        "    - Проверить есть ли на плате оптики камера\n"
                        "    1.1. На плате оптики нет камеры\n"
                        "        - Заменить дрон\n"
                        "    1.2. На плате оптики есть камера\n"
                        "        - Заменить аккумулятор и включить дрон\n")

#
#
# errors_info["GameCore"] = "Нет доступа к ядру"
# errors_info["Видео"] = "Не подключается видео"
# errors_info["Страница управления"] = list()
# errors_info["Сервер"] = list()
# errors_info["GUI"] = list()
# errors_info["Дроны"] = list()

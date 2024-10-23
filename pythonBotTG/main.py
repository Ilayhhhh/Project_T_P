@bot.message_handler(commands=['soveti'])
def ask_for_proda(message):
    user_states[message.chat.id] = 'waiting_for_response'  # Устанавливаем состояние
    bot.reply_to(message, "Мы приготовили некоторые советы по питанию для всех наших пользователей.")
    bot.send_message(message.chat.id, "Для начала давайте уточним: \n 1-Я не исключаю из своего рациона никакой тип продуктов\n 2-Я исключаю из своего рациона мясо🍖❌\n 3-Я исключаю из своего рациона молочные продукты🥛❌\n 4-Я исключаю из своего рациона мясные и молочные продукты 🍖🥛❌\n\n Пожалуйста, введите номер вашего выбора:")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_response')
def handle_user_response(message):
    if message.text.lower() == "1":
        bot.send_message(message.chat.id, "Для людей, не исключающих ничего из своего рациона, предлагаем ознакомиться с Проверенными источниками.\n 1)Ролик с короткими советами по правильному питанию https://yandex.ru/video/preview/17504274598371715017 \n 2)Принципы здорового питания от РОСПОТРЕБНАДЗОРА https://14.rospotrebnadzor.ru/content/2090/79455/ \n 3) 1000 рецептов домашних рецептов здорового питания https://1000.menu/catalog/sbalansirovannoe-pitanie")
    elif message.text.lower() == "2":
        bot.send_message(message.chat.id, "Для людей, исключающих мясные продукты, предлагаем ознакомиться с проверенными источниками.\n 1)Ролик с советами по питанию без мяса https://youtu.be/KPO0A90XqzE \n 2)Чем заменить мясо https://rutube.ru/video/8a225add9e7d4800501e4d73e2a86756/?r=plwd \n 3)ПП блюда без мяса https://1000.menu/meals/9022-10427")
    elif message.text.lower() == "3":
        bot.send_message(message.chat.id, "Для людей, исключающих молочные продукты, предлагаем ознакомиться с проверенными источниками.\n 1)Ролик о том чем заменить молочные продукты https://yandex.ru/video/preview/13100322906635975298 \n 2) Рецепты без молочных продуктов https://www.edimdoma.ru/retsepty/tags/9056-pp-retsepty-bez-molochnyh-produktov \n 3)Рацион питания без мололчных продуктов https://dgp6-omsk.ru/ru/racion-pitanija-bez-molochnyh-produktov")
    elif message.text.lower() == "4":
        bot.send_message(message.chat.id,"Для людей, исключающих мясные и молочные продукты, предлагаем ознакомиться с проверенными источниками.\n 1) Ролик о полноценном меню на неделю https://yandex.ru/video/preview/3342349212361481234 \n 2) Как сбалансирорвать рацион https://77.rospotrebnadzor.ru/index.php/press-centr/186-press-centr/12308-vegetarianstvo-kak-sbalansirovat-ratsion-01-11-2023 \n 3) Рецепты, искалючающие мясные и молочные продукты https://1000.menu/meals/13-4717")
    user_states[message.chat.id] = None  # Сбрасываем состояние после обработки ответа

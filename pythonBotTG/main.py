@bot.message_handler(commands=['soveti'])
def ask_for_proda(message):
    user_states[message.chat.id] = 'waiting_for_response'  # Устанавливаем состояние
    bot.reply_to(message, "Мы приготовили некоторые советы по питанию для всех наших пользователей.")
    bot.send_message(message.chat.id, "Для начала давайте уточним: \n 1-Я не исключаю из своего рациона никакой тип продуктов\n 2-Я исключаю из своего рациона мясо🍖❌\n 3-Я исключаю из своего рациона молочные продукты🥛❌\n 4-Я исключаю из своего рациона мясные и молочные продукты 🍖🥛❌\n\n Пожалуйста, введите номер вашего выбора:")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_response')
def handle_user_response(message):
    ...ТУТ ВАНЕК!!
    ...
    user_states[message.chat.id] = None  # Сбрасываем состояние после обработки ответа

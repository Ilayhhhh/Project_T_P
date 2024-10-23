import telebot

API = "7797110821:AAFjgZLUAot0Gir_ke_Zml4enBUNkKe1pLg"
bot = telebot.TeleBot(API)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"Добро пожаловать, {message.from_user.first_name}. Это Telegram-бот для расчета калорий, белков, жиров и углеводов! Здесь Вы сможете легко и быстро отслеживать свое питание и достигать ваших целей в поддержании здорового образа жизни.")
#К сообщению выше добавить две конпки: информация и калькулятор. одна будет перебрасывать на info другая на calculate
@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "Представляем вашему вниманию бот в Telegram, который станет незаменимым помощником в контроле вашего питания и поддержании здорового образа жизни. Он способен автоматически рассчитывать калорийность, белки, жиры и углеводы (КБЖУ) на основе ваших индивидуальных данных, таких как вес, рост, возраст и уровень физической активности. Просто введите свои параметры, и бот обеспечит вам точные рекомендации. Интуитивно понятный интерфейс и быстрый отклик делают общение с ботом легким и приятным. Начните свой путь к гармонии с телом прямо сейчас!")

@bot.message_handler(commands=['calculate'])
def ask_for_data(message):
    bot.send_message(message.chat.id, "Пожалуйста, введите ваши данные - пол, вес, рост, возраст и уровень активности, где уровень физической активности измеряется в: \n 1( Малоподвижный образ жизни) \n 2(Умеренная активность) \n 3(Активно занимающийся спортом).\n\n Пример: ж 65 170 25 2")

@bot.message_handler(func=lambda message: len(message.text.split()) == 4)
def calculate_kbju(message):
    try:
        # Разделение сообщения на части
        data = message.text.split()
        if len(data) != 4:
            raise ValueError("Неправильный формат. Введите четыре числа: вес, рост, возраст и уровень активности.")
        ves = float(data[0])  # вес
        rost = float(data[1])  # рост
        vozr = float(data[2])  # возраст
        activity_level = int(data[3])  # уровень активности

        if ves <= 0 or rost <= 0 or vozr <= 0:
            raise ValueError("Вес, рост и возраст не могут быть отрицательными числами")

        # Базовый метаболизм (формула от Сен Жора)
        bmr = 9 * ves + 6.25 * rost - 5 * vozr + 5  # Формула для мужчин

        # Коэффициенты активности
        activity_mul = {
            1: 1.1,   # малоподвижный образ жизни
            2: 1.3,  # умеренно активный
            3: 1.5    # активно занимающийся спортом
        }

        # Проверка уровня активности
        if activity_level not in activity_mul:
            raise ValueError("Уровень активности должен быть 1, 2 или 3.")

        # Учитываем уровень активности
        tdee = bmr * activity_mul[activity_level]

        # Расчет КБЖУ (например, 40% углеводы, 30% белки, 30% жиры)
        ugl = tdee * 0.4 / 4  # углеводы
        belk = tdee * 0.3 / 5  # белки
        jir = tdee * 0.3 / 8    # жиры

        response = (f"Ваша дневная норма КБЖУ:\n"
                    f"Калории: {tdee:.2f} ккал\n"
                    f"Углеводы: {ugl:.2f} г\n"
                    f"Белки: {belk:.2f} г\n"
                    f"Жиры: {jir:.2f} г")
        bot.reply_to(message, response)

    except Exception as e:
        bot.reply_to(message, str(e))

bot.polling(none_stop=True)

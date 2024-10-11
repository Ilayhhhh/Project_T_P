import telebot

API = '7905332994:AAH5_aNNKSXRKf8-muk8I9hhm3V_wPWOT4I'
bot = telebot.TeleBot(API)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Я помогу вам рассчитать ваши КБЖУ. Введите ваш вес (кг), рост (см) и уровень активности (1 - низкий, 2 - средний, 3 - высокий) в формате:\n"
                          "вес рост уровень активности")

@bot.message_handler(func=lambda message: True)
def calculate_kbju(message):
    try:
        # Раздел сообщение на части
        data = message.text.split()
        if len(data) != 3:
            raise ValueError("Неправильный формат. Введите три числа: вес, рост и уровень активности.")

        weight = float(data[0])  # вес
        height = float(data[1])  # рост
        activity_level = int(data[2])  # активность

        #  базовый метаболизма (формула от сент жеор чет такое)
        bmr = 10 * weight + 6.25 * height - 5 * 30 + 5

        # Коэф активн
        activity_mul = {
            1: 1.2,  # малоподвижный образ жизни
            2: 1.55,  # умеренно активный
            3: 1.9   # активно занимающийся спортом
        }

        # Проверка уровня активности
        if activity_level not in activity_mul:
            raise ValueError("Уровень активности должен быть 1, 2 или 3.")

        # Учитываем уровень активности
        tdee = bmr * activity_mul[activity_level]

        # Расчет КБЖУ (например, 50% углеводы, 30% белки, 20% жиры)
        ugl = tdee * 0.5 / 4
        belk = tdee * 0.3 / 4
        jir = tdee * 0.2 / 9

        response = (f"Ваши расчеты КБЖУ:\n"
                    f"Калории: {tdee:.2f} ккал\n"
                    f"Углеводы: {ugl:.2f} г\n"
                    f"Белки: {belk:.2f} г\n"
                    f"Жиры: {jir:.2f} г")
        bot.reply_to(message, response)

    except Exception as e:
        bot.reply_to(message, str(e))

if name == 'main':
    bot.polling()
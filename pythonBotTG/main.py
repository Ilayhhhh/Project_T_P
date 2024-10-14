import telebot

API = "7797110821:AAFjgZLUAot0Gir_ke_Zml4enBUNkKe1pLg"
bot = telebot.TeleBot(API)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Я помогу вам рассчитать ваши КБЖУ. Введите ваш вес (кг), рост (см), возраст (лет) и уровень активности (1 - низкий, 2 - средний, 3 - высокий) в формате:\n"
                          "вес рост уровень активности")

@bot.message_handler(func=lambda message: True)
def calculate_kbju(message):
    try:
        # Раздел сообщение на части
        data = message.text.split()
        if len(data) != 4:
            raise ValueError("Неправильный формат. Введите три числа: вес, рост, возраст и уровень активности.")

        ves = float(data[0])  # вес
        rost = float(data[1]) # рост
        vozr = float(data[2])#возраст
        activity_level = int(data[3])  # активность
        if ves <= 0 or rost <= 0 or vozr <= 0:
            raise ValueError("Вес, рост и возраст не могут быть отрицательными числами.")

        #  базовый метаболизма (формула от сент жеор чет такое)
        bmr = 5 + (10*ves)+(6.25*rost)-(5*vozr)

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

if __name__ == '__main__':
    bot.polling()
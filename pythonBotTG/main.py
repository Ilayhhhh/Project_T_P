import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API = "7797110821:AAFjgZLUAot0Gir_ke_Zml4enBUNkKe1pLg"
bot = telebot.TeleBot(API)

# Функция для создания клавиатуры с кнопками
def create_main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Информация", callback_data="info"))
    markup.add(InlineKeyboardButton("Калькулятор", callback_data="calculate"))
    markup.add(InlineKeyboardButton("Советы", callback_data="soveti"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"Добро пожаловать, {message.from_user.first_name}. Это Telegram-бот для расчета калорий, белков, жиров и углеводов! Здесь Вы сможете легко и быстро отслеживать свое питание и достигать ваших целей в поддержании здорового образа жизни.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == "info")
def send_info(call):
    bot.answer_callback_query(call.id)  # Убирает загрузку внизу
    bot.send_message(call.message.chat.id, "Представляем вашему вниманию бот в Telegram, который станет незаменимым помощником в контроле вашего питания и поддержании здорового образа жизни. Он способен автоматически рассчитывать калорийность, белки, жиры и углеводы (КБЖУ) на основе ваших индивидуальных данных, таких как вес, рост, возраст и уровень физической активности. Просто введите свои параметры, и бот обеспечит вам точные рекомендации. Интуитивно понятный интерфейс и быстрый отклик делают общение с ботом легким и приятным. Начните свой путь к гармонии с телом прямо сейчас!")

@bot.callback_query_handler(func=lambda call: call.data == "calculate")
def ask_for_data(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Пожалуйста, введите ваши данные в формате:\n пол вес рост возраст уровень активности\n Пример: ж 65 170 25 2")

@bot.message_handler(func=lambda message: len(message.text.split()) == 5)
def calculate_kbju(message):
    try:
        # Разделение сообщения на части
        data = message.text.split()
        if len(data) != 5:
            raise ValueError("Неправильный формат. Введите пять параметров: пол, вес, рост, возраст и уровень активности.")

        sex = data[0].lower()  # пол
        ves = float(data[1])  # вес
        rost = float(data[2])  # рост
        vozr = float(data[3])  # возраст
        activity_level = int(data[4])  # уровень активности

        if ves <= 0 or rost <= 0 or vozr <= 0:
            raise ValueError("Вес, рост и возраст не могут быть отрицательными числами")

        if sex == 'м':
            bmr = 9 * ves + 6.25 * rost - 5 * vozr + 5  # Формула для мужчин
        elif sex == 'ж':
            bmr = 9 * ves + 6.25 * rost - 5 * vozr - 161  # Формула для женщин
        else:
            raise ValueError("Пол должен быть 'м' для мужчин или 'ж' для женщин.")

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

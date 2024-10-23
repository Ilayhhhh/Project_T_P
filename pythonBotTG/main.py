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
    bot.send_message(call.message.chat.id, "Пожалуйста, введите ваши данные - пол, вес, рост, возраст и уровень активности, где уровень физической активности измеряется в: \n 1( Малоподвижный образ жизни) \n 2(Умеренная активность) \n 3(Активно занимающийся спортом).\n\n Пример: ж 65 170 25 2")

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
user_states = {}  # Словарь для хранения состояния пользователей
@bot.callback_query_handler(func=lambda call: call.data == "soveti")
def ask_for_proda(call):
    user_states[call.message.chat.id] = 'waiting_for_response'  # Устанавливаем состояние
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Мы приготовили некоторые советы по питанию для всех наших пользователей.")
    bot.send_message(call.message.chat.id, "Для начала давайте уточним: \n 1-Я не исключаю из своего рациона никакой тип продуктов\n 2-Я исключаю из своего рациона мясо🍖❌\n 3-Я исключаю из своего рациона молочные продукты🥛❌\n 4-Я исключаю из своего рациона мясные и молочные продукты 🍖🥛❌\n \n Пожалуйста, введите номер вашего выбора:")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_response')
def handle_user_response(message):
    if message.text == "1":
        bot.send_message(message.chat.id, "Для людей, не исключающих ничего из своего рациона, предлагаем ознакомиться с Проверенными источниками.\n 1)Ролик с короткими советами по правильному питанию https://yandex.ru/video/preview/17504274598371715017 \n 2)Принципы здорового питания от РОСПОТРЕБНАДЗОРА https://14.rospotrebnadzor.ru/content/2090/79455/ \\n 3) 1000 рецептов домашних рецептов здорового питания https://1000.menu/catalog/sbalansirovannoe-pitanie")
    elif message.text.lower() == "2":
        bot.send_message(message.chat.id,
                         "Для людей, исключающих мясные продукты, предлагаем ознакомиться с проверенными источниками.\n 1)Ролик с советами по питанию без мяса https://youtu.be/KPO0A90XqzE \n 2)Чем заменить мясо https://rutube.ru/video/8a225add9e7d4800501e4d73e2a86756/?r=plwd \n 3)ПП блюда без мяса https://1000.menu/meals/9022-10427")
    elif message.text.lower() == "3":
        bot.send_message(message.chat.id,
                         "Для людей, исключающих молочные продукты, предлагаем ознакомиться с проверенными источниками.\n 1)Ролик о том чем заменить молочные продукты https://yandex.ru/video/preview/13100322906635975298 \n 2) Рецепты без молочных продуктов https://www.edimdoma.ru/retsepty/tags/9056-pp-retsepty-bez-molochnyh-produktov \n 3)Рацион питания без мололчных продуктов https://dgp6-omsk.ru/ru/racion-pitanija-bez-molochnyh-produktov")
    elif message.text.lower() == "4":
        bot.send_message(message.chat.id,
                         "Для людей, исключающих мясные и молочные продукты, предлагаем ознакомиться с проверенными источниками.\n 1) Ролик о полноценном меню на неделю https://yandex.ru/video/preview/3342349212361481234 \n 2) Как сбалансирорвать рацион https://77.rospotrebnadzor.ru/index.php/press-centr/186-press-centr/12308-vegetarianstvo-kak-sbalansirovat-ratsion-01-11-2023 \n 3) Рецепты, искалючающие мясные и молочные продукты https://1000.menu/meals/13-4717")
    user_states[message.chat.id] = None  # Сбрасываем состояние после обработки ответа
try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"Error:{e}")

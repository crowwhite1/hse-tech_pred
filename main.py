import telebot

import database
import path_handler
import states
import weather_handler
import keyboard as kb
import database as db
import schedule
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7938989904:AAFjCT56ScPef2ScGcxGKjge5Pehh-oT38w"

# Инициализируем бота
bot = telebot.TeleBot(TOKEN)

# Инициализируем базу данных
cursor = db.init()


def get_chat_from_message(message) -> int:
    """
    Получение id чата при получении сообщения
    :param message:Message
    :return id:int
    """
    return message.chat.id


# Обновлённая функция handle_message для работы с Markdown
# Обработка любого текста
def handle_some_message_with_default_state(message):
    if message.text in ["/start", 'Начать заново']:
        begin(message)
    elif message.text in ["/new_element", "Новый предмет"]:
        add_task_handler(message)
    elif message.text in ["/show_shopping_list", "Показать список покупок"]:
        show_tasks_handler(message)
    elif message.text in ["/delete_element", "Удалить предмет"]:
        delete_task_handler(message)
    elif message.text in ["/edit_element", "Редактировать предмет"]:
        edit_task_prompt(message)
    elif message.text in ["/help", "Помощь"]:  # Обработка команды /help
        display_help(message)
    elif message.text in ["/weather", 'Получить погоду']:
        request_location(message)
    elif message.text in ["/weather_day", "Получить погоду на день"]:
        request_location_day(message)
    elif message.text in ["/allow", "Подписаться/отписаться от рассылки"]:
        allow_send(message)
    elif message.text in ["/add_shop", "Добавить магазин"]:
        add_shop_handler(message)
    elif message.text in ["/delete_shop", "Удалить магазин"]:
        delete_shop_handler(message)
    elif message.text in ["/show_shops", "Показать список магазинов"]:
        show_shops_handler(message)
    elif message.text in ["/show_path", "Показать маршрут"]:
        request_location_path(message)
    else:
        keyboard = kb.make_keyboard()
        bot.send_message(message.chat.id, 'Привет! Я твой помощник в походах по магазинам. Выберите действие:', reply_markup=keyboard,
                         parse_mode='Markdown')


# Функция для отображения справки с использованием Markdown
help_text = ("*Доступные команды:*\n"
             "/start - Начало работы с ботом\n"
             "/new_element - Добавить новый предмет в список покупок\n"
             "/show_shopping_list - Показать ваш список покупок\n"
             "/delete_element - Удаление предмета из списка покупок\n"
             "/edit_element - Редактирование предмета из списка покупок\n"
             "/show_shops - Показать ваши выбранные магазины\n"
             "/add_shop - Добавить новый магазин в список\n"
             "/delete_shop - Удалить магазин из списка\n"
             "/show_path - Показать маршрут\n"
             "/weather - Получить погоду\n"
             "/weather_day - Получить погоду на завтра\n"
             "/help - Показать это сообщение справки\n"
             "/allow - Подписаться/отписаться от рассылки\n")
@bot.message_handler(commands=['help'])
def display_help(message):
    bot.send_message(message.chat.id, help_text, reply_markup=kb.make_keyboard())


# Функция обработчик начала работы с ботом
@bot.message_handler(commands=['start'])
def begin(message):
    database.create_user(get_chat_from_message(message))
    bot.send_message(message.chat.id,
                     'Привет! Я твой помощник в походах по магазинам. Используй команды или кнопки ниже для взаимодействия со мной.',
                     reply_markup=kb.make_keyboard())


# Функция-обработчик получения текущей погоды
@bot.message_handler(commands=['weather_day'])
def request_location_day(message):
    chat_id = get_chat_from_message(message)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    database.update_user_state(chat_id, states.GET_WEATHER_DAY)
    bot.send_message(chat_id, "Пожалуйста, отправьте ваше местоположение", reply_markup=keyboard)


# Функция-обработчик получения текущей погоды
@bot.message_handler(commands=['weather'])
def request_location(message):
    chat_id = get_chat_from_message(message)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    database.update_user_state(chat_id, states.GET_WEATHER)
    bot.send_message(chat_id, "Пожалуйста, отправьте ваше местоположение", reply_markup=keyboard)


# Функция-обработчик получения текущей погоды
@bot.message_handler(commands=['show_path'])
def request_location_path(message):
    chat_id = get_chat_from_message(message)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    database.update_user_state(chat_id, states.SHOW_PATH)
    bot.send_message(chat_id, "Пожалуйста, отправьте ваше местоположение", reply_markup=keyboard)


# Реализация получения погоды сейчас/на день
@bot.message_handler(content_types=['location'])
def location_received(message):
    lat, lon = message.location.latitude, message.location.longitude
    chat_id = get_chat_from_message(message)
    user = database.get_user_from_db(chat_id)
    if int(user[1]) == 4:
        answer = weather_handler.get_weather(lat, lon, user)
    elif int(user[1]) == 5:
        answer = weather_handler.get_weather_for_day(lat, lon, user)
    else:
        shops = list(shop[2] for shop in database.get_all_shops(int(user[0])))
        answer = path_handler.get_path(lat, lon, shops)
    bot.send_message(message.chat.id, answer)
    set_default_state(message)


# Функция установщик дефолтного состояния
def set_default_state(message):
    keyboard = kb.make_keyboard()
    database.update_user_state(get_chat_from_message(message), states.DEFAULT_STATE)
    bot.send_message(message.chat.id, 'Привет! Я твой помощник в походах по магазинам. Выберите действие:', reply_markup=keyboard,
                     parse_mode='Markdown')


# Обработка сообщений на случай, если у пользователя имеются состояния
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = get_chat_from_message(message)
    user = database.get_user_from_db(chat_id)
    if user == None:
        database.create_user(get_chat_from_message(message))
        state = states.DEFAULT_STATE
    else:
        state = int(user[1])
    if state == states.DEFAULT_STATE:
        handle_some_message_with_default_state(message)
    elif state == states.ADD_SHOP:
        add_shop_impl(message)
    elif state == states.ADD_ELEMENT:
        add_task_impl(message)
    elif state == states.DELETE_ELEMENT:
        delete_task_confirmation_impl(message)
    elif state == states.DELETE_SHOP:
        delete_shop_confirmation_impl(message)
    if state != 0:
        set_default_state(message)


# Функция-обработчик для добавления задачи
@bot.message_handler(commands=['new_element'])
def add_task_handler(message):
    chat_id = get_chat_from_message(message)
    database.update_user_state(chat_id, states.ADD_ELEMENT)
    bot.send_message(message.chat.id, 'Введите предмет:', reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['add_shop'])
def add_shop_handler(message):
    chat_id = get_chat_from_message(message)
    database.update_user_state(chat_id, states.ADD_SHOP)
    bot.send_message(message.chat.id, 'Введите Магазин:', reply_markup=types.ReplyKeyboardRemove())


# Реализация добавления задачи
def add_task_impl(message):
    chat_id = get_chat_from_message(message)
    user_tasks_count = len(database.get_all_shops(chat_id))
    text = message.text
    database_response = database.add_task(user_tasks_count + 1, chat_id, text)
    bot.send_message(chat_id, database_response)


def add_shop_impl(message):
    chat_id = get_chat_from_message(message)
    user_tasks_count = len(database.get_all_shops(chat_id))
    text = message.text
    database_response = database.add_shop(user_tasks_count + 1, chat_id, text)
    bot.send_message(chat_id, database_response)


# Функция-обработчик показа всех задач
@bot.message_handler(commands=['show_shopping_list'])
def show_tasks_handler(message):
    show_tasks_impl(message)

# Функция-обработчик показа всех задач
@bot.message_handler(commands=['show_shops'])
def show_shops_handler(message):
    show_shops_impl(message)


# Реализация показа всех задач
def show_tasks_impl(message):
    chat_id = get_chat_from_message(message)
    tasks = database.get_all_tasks(chat_id)
    if tasks is None or len(tasks) == 0:
        bot.send_message(chat_id, 'У вас пока нет предметов для покупки.', reply_markup=kb.make_keyboard())
        return
    response = "Ваш список покупок:\n"
    for task in tasks:
        response += f"{task[0]}. {task[2]}\n"
    bot.send_message(chat_id, response, reply_markup=kb.make_keyboard())

def show_shops_impl(message):
    chat_id = get_chat_from_message(message)
    tasks = database.get_all_shops(chat_id)
    if tasks is None or len(tasks) == 0:
        bot.send_message(chat_id, 'У вас пока нет магазинов.', reply_markup=kb.make_keyboard())
        return
    response = "Ваши магазины:\n"
    for task in tasks:
        response += f"{task[0]}. {task[2]}\n"
    bot.send_message(chat_id, response, reply_markup=kb.make_keyboard())

# Обработчик запуска подтверждения запуска удаления задачи
@bot.message_handler(commands=['delete_element'])
def delete_task_handler(message):
    delete_task_confirmation_impl(message)

# Обработчик запуска подтверждения запуска удаления задачи
@bot.message_handler(commands=['delete_shop'])
def delete_shop_handler(message):
    delete_shop_confirmation_impl(message)


# Функция запуска подтверждения запуска удаления задачи
def delete_task_confirmation_impl(message):
    chat_id = get_chat_from_message(message)
    msg = bot.send_message(chat_id, 'Выберите номер предмета для удаления:')
    bot.register_next_step_handler(msg,
                                   confirm_delete_task, chat_id)


# Функция запуска подтверждения запуска удаления задачи
def delete_shop_confirmation_impl(message):
    chat_id = get_chat_from_message(message)
    msg = bot.send_message(chat_id, 'Выберите номер магазина для удаления:')
    bot.register_next_step_handler(msg,
                                   confirm_delete_shop, chat_id)


# Функция для вывода списка задач для редактирования
@bot.message_handler(commands=['edit_element'])
def edit_task_prompt(message):
    chat_id = message.chat.id
    tasks_idx = {int(x[0]) for x in database.get_all_tasks(chat_id)}

    if len(tasks_idx) > 0:
        response = "Выберите номер предмета для редактирования:"
        msg = bot.send_message(chat_id, response, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, edit_task_choose, chat_id)
    else:
        bot.send_message(chat_id, 'У вас нет предметов для редактирования.', reply_markup=kb.make_keyboard())


# Функция для выбора задачи для редактирования
def edit_task_choose(message, chat_id):
    task_number = message.text
    tasks_idx = {int(x[0]) for x in database.get_all_tasks(chat_id)}
    if task_number.isdigit() and int(task_number) in tasks_idx:
        msg = bot.send_message(chat_id, 'Введите новый текст предмета:')
        bot.register_next_step_handler(msg, edit_task, chat_id, int(task_number))
    else:
        bot.send_message(chat_id, 'Некорректный номер предмета.', reply_markup=kb.make_keyboard())


# Функция для редактирования задачи
def edit_task(message, chat_id, task_index):
    database_response = database.edit_task(task_index, chat_id, message.text)
    bot.send_message(chat_id, database_response, reply_markup=kb.make_keyboard())
    set_default_state(message)


# Функция для запроса подтверждения удаления задачи
def confirm_delete_task(message, chat_id):
    user_tasks_ids = {task[0] for task in database.get_all_tasks(chat_id)}
    task_number = message.text
    if task_number.isdigit() and int(task_number) in user_tasks_ids:
        keyboard = InlineKeyboardMarkup()
        confirm_button = InlineKeyboardButton("Да", callback_data=f"delete_confirmed_{task_number}")
        cancel_button = InlineKeyboardButton("Нет", callback_data="delete_cancelled")
        keyboard.add(confirm_button, cancel_button)
        bot.send_message(chat_id, 'Вы уверены, что хотите удалить этот предмет?', reply_markup=keyboard)
    else:
        bot.send_message(chat_id, 'Некорректный номер предмета.', reply_markup=kb.make_keyboard())


# Функция для запроса подтверждения удаления задачи
def confirm_delete_shop(message, chat_id):
    user_tasks_ids = {shop[0] for shop in database.get_all_shops(chat_id)}
    task_number = message.text
    if task_number.isdigit() and int(task_number) in user_tasks_ids:
        keyboard = InlineKeyboardMarkup()
        confirm_button = InlineKeyboardButton("Да", callback_data=f"delete_shop_confirmed_{task_number}")
        cancel_button = InlineKeyboardButton("Нет", callback_data="delete_shop_cancelled")
        keyboard.add(confirm_button, cancel_button)
        bot.send_message(chat_id, 'Вы уверены, что хотите удалить этот магазин?', reply_markup=keyboard)
    else:
        bot.send_message(chat_id, 'Некорректный номер магазина.', reply_markup=kb.make_keyboard())


# Обработчик обратных вызовов от inline-кнопок
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_confirmed_'))
def handle_delete_confirmed(call):
    chat_id = get_chat_from_message(call.message)
    task_index = int(call.data.split('_')[-1])
    database_response = database.delete_task(task_index, chat_id)
    tasks = database.get_all_tasks(chat_id)
    for i in range(len(tasks)):
        database.edit_task_num(i + 1, tasks[i][0], chat_id)
    bot.answer_callback_query(call.id, database_response)
    bot.edit_message_text(database_response, chat_id, call.message.message_id)
    set_default_state(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'delete_cancelled')
def handle_delete_cancelled(call):
    bot.answer_callback_query(call.id, 'Удаление отменено.')
    bot.edit_message_text('Удаление предмета отменено.', call.message.chat.id, call.message.message_id)
    set_default_state(call.message)


# Обработчик обратных вызовов от inline-кнопок
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_shop_confirmed_'))
def handle_delete_confirmed_shop(call):
    chat_id = get_chat_from_message(call.message)
    task_index = int(call.data.split('_')[-1])
    database_response = database.delete_shop(task_index, chat_id)
    tasks = database.get_all_shops(chat_id)
    for i in range(len(tasks)):
        database.edit_shop_num(i + 1, tasks[i][0], chat_id)
    bot.answer_callback_query(call.id, database_response)
    bot.edit_message_text(database_response, chat_id, call.message.message_id)
    set_default_state(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'delete_shop_cancelled')
def handle_delete_cancelled_shop(call):
    bot.answer_callback_query(call.id, 'Удаление отменено.')
    bot.edit_message_text('Удаление магазина отменено.', call.message.chat.id, call.message.message_id)
    set_default_state(call.message)


# Функция обработчик подписки/отсылки от рассылки
@bot.message_handler(commands=['allow'])
def allow_send(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_yes = types.InlineKeyboardButton("Да", callback_data='yes')
    button_no = types.InlineKeyboardButton("Нет", callback_data='no')
    markup.add(button_yes, button_no)
    bot.send_message(message.chat.id, "Вы хотите подписаться/отписаться от рассылки прогноза погоды?",
                     reply_markup=markup)


# Функция-обработчик для изменения состояния подписки на рассылку
@bot.callback_query_handler(func=lambda call: call.data == 'yes' or call.data == 'no')
def handle_query(call):
    chat_id = call.message.chat.id
    user = database.get_user_from_db(chat_id)
    if call.data == "yes":
        new_state = True if user[-1] == False else False
        database_response = database.update_user_allow_send(chat_id, new_state)
        bot.answer_callback_query(call.id, database_response)
        bot.edit_message_text(database_response, chat_id, call.message.message_id)
    elif call.data == "no":
        bot.answer_callback_query(call.id, 'Изменение отменено.')
        bot.edit_message_text('Изменение состояния подписки отменено.', call.message.chat.id, call.message.message_id)
    set_default_state(call.message)


def send_broadcast():
    users = database.get_all_users()
    for user in users:
        if user[2] is not None and user[3]:
            try:
                bot.send_message(user[0], weather_handler.get_weather_for_day_by_code(user[2]))
            except:
                pass


schedule.every().day.at("09:00").do(send_broadcast)
schedule.run_pending()

# Зацикливаем нашего бота, чтобы он всё обрабатывал
bot.polling(none_stop=True, interval=0)

from telebot import types

def make_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    begin_button = types.KeyboardButton("Начать заново")
    new_task_button = types.KeyboardButton("Новый предмет")
    show_tasks_button = types.KeyboardButton("Показать список покупок")
    delete_task_button = types.KeyboardButton("Удалить предмет")
    edit_task_button = types.KeyboardButton("Редактировать предмет")
    help_button = types.KeyboardButton("Помощь")
    get_weather_button = types.KeyboardButton("Получить погоду")
    get_tomorrow_weather_button = types.KeyboardButton("Получить погоду на день")
    allow_send_button = types.KeyboardButton("Подписаться/отписаться от рассылки")

    new_shop_button = types.KeyboardButton("Добавить магазин")
    show_shop_button = types.KeyboardButton("Показать список магазинов")
    delete_shop_button = types.KeyboardButton("Удалить магазин")
    show_path_button = types.KeyboardButton("Показать маршрут")
    keyboard.add(begin_button, help_button)
    #keyboard.add(new_task_button, show_tasks_button)
    #keyboard.add(delete_task_button, edit_task_button)
    keyboard.add(new_shop_button, show_shop_button)
    keyboard.add(delete_shop_button, show_path_button)
    #keyboard.add(get_weather_button, get_tomorrow_weather_button)
    #keyboard.add(allow_send_button)
    return keyboard
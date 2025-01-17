# planner - бот для планирования своих задач

## Работа выполнена на 10 баллов

## Касательно опоздания по деллайну - семинарист разрешил отправить ночью

Данный бот предназначен для планирования своих задач. Помимо этого он может искать гифки, мотивировать цитатами
и сообщать погоду на текущий момент и день

Также в боте есть рассылка для получения прогноза погоды на день

Касательно оформления бота:

- Состояния пользователей вынесены в отдельный файл states.py
- quote_handler.py предназначен для работы с цитатами
- weather_handler.py предназначен для работы с погодой
- keyboards.py отвечает за работу с основными кнопками
- database.py отвечает за работу с базой данных
- giphy_handler.py предназначен для работы с гифками
- main.py отвечает за код бота и основную логику
- requirements.txt отвечает за зависимости, которые необходимо загрузить

Проект оформлен с соблюдением стандарта PEP-8, для ключевых функций добавлены разъясняющие комментарии.
Код разделен на отдельные модули и функциональности, для сохранения читабельности и возможности легко вносить правки.
Каждая функция отвечает за свою функциональность. Некоторая логика взаимодействия реализуется через inline-клавиатуру
и callback дату. В боте используется встроенная база данных для хранения информаци о пользователях, для сохранения
быстродействия

Количество функций-обработчиков - 11 (без учёта обработки callback):

1. begin - Обработчик команды start
2. request_location - Обработчик для получения геопозиции для текущей погоды
3. request_location_day - Обработчик для получения геопозиции для погоды в течении дня
4. get_quote - Обработчик получения цитаты
5. get_gif - Обработчик получения gif
6. add_task_handler - Обработчик добавления задачи
7. show_tasks_handler - Обработчик показа основный задач
8. delete_task_handler - Обработчик удаления задачи
9. edit_task_prompt - Обработчик изменения задачи
10. allow_send - Обработчик подписки на рассылку
11. display_help - Обработчик получения основной информации про команды бота

Данного бота ещё можно дорабатывать, в нём есть потенциал, а так же возможность внедрения платной подписки.
Но по большей степени данный бот предназначен для помощи людям
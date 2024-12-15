import sqlite3

def init():
    """Создание базы данных"""
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS 'user' (
    'id' INT,
    'state' INT DEFAULT 0,
    'last_geo' STRING,
    'allow_send' BOOLEAN DEFAULT FALSE,
    PRIMARY KEY ('id')
    )
    ''')
    db.commit()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS 'user_tasks' (
    'id' INT AUTO_INCREMENT,
    'user_id' INT,
    'text' TEXT NOT NULL,
    PRIMARY KEY ('id','user_id'),
    CONSTRAINT 'fk_user' FOREIGN KEY ('user_id') REFERENCES 'user'('id') ON DELETE CASCADE ON UPDATE NO ACTION
    )
    ''')
    db.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'user_shops' (
        'id' INT AUTO_INCREMENT,
        'user_id' INT,
        'name' TEXT NOT NULL,
        PRIMARY KEY ('id','user_id'),
        CONSTRAINT 'fk_user' FOREIGN KEY ('user_id') REFERENCES 'user'('id') ON DELETE CASCADE ON UPDATE NO ACTION
        )
        ''')
    db.commit()
    return cursor


def get_user_from_db(id: int):
    """
    Получение юзера из базы данных по id
    :type id: int
    :param id:int
    :return:
    """
    cursor, db = get_connection()
    cursor.execute(f"SELECT * FROM user WHERE id == {id}")
    return cursor.fetchone()


def update_user_state(user_id, state):
    """Изменение состояния пользователя"""
    cursor, db = get_connection()
    sql = 'UPDATE user SET state = ? WHERE id = ?'
    cursor.execute(sql, (state, user_id))
    db.commit()


def get_all_users():
    """Получение всех пользователей"""
    cursor, db = get_connection()
    sql = 'SELECT * FROM user'
    cursor.execute(sql, )
    return cursor.fetchall()


def update_user_allow_send(user_id, allow_send):
    """Изменение состояния подписки на рассылку"""
    try:
        cursor, db = get_connection()

        sql = 'UPDATE user SET allow_send = ? WHERE id = ?'
        cursor.execute(sql, (allow_send, user_id))
        db.commit()
        return 'Состояние подписки на рассылку изменено'
    except:
        return 'Ошибка изменения подписки'


def update_user_geo(user_id, geo):
    """Изменение последней геолокации пользователя"""
    cursor, db = get_connection()
    sql = 'UPDATE user SET last_geo = ? WHERE id = ?'
    cursor.execute(sql, (geo, user_id))
    db.commit()


def get_connection():
    """Получение основных элементов работы с бд"""
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    return cursor, db


def create_user(id):
    """Регистрация пользователя"""
    cursor, db = get_connection()
    try:
        sql = '''INSERT INTO user (id, state) VALUES (?, ?);'''
        cursor.execute(sql, (id, 0))
        db.commit()
    except:
        sql = 'UPDATE user SET state = ? WHERE id = ?'
        cursor.execute(sql, (0, id))
        db.commit()


def get_all_tasks(user_id):
    """Получение всех задач пользователя"""
    cursor, db = get_connection()
    cursor.execute(f"SELECT * FROM user_tasks WHERE user_id == {user_id}")
    return cursor.fetchall()


def add_task(id, user_id, task):
    """Добавление задачи пользователю"""
    cursor, db = get_connection()
    try:
        sql = '''INSERT INTO user_tasks (id, user_id, text) VALUES (?, ?, ?);'''
        cursor.execute(sql, (id, user_id, task))
        db.commit()
        return "Предмет добавлен в список покупок успешно"
    except:
        return "Возникла ошибка при добавлении предмета в список покупок"


def delete_task(id, user_id):
    """Удаление задачи пользователю"""
    cursor, db = get_connection()
    try:
        sql = 'DELETE FROM user_tasks WHERE id = ? AND user_id = ?'
        cursor.execute(sql, (int(id), user_id))
        db.commit()
        return "Предмет успешно удален из списка покупок"
    except:
        return "Возникла ошибка при удалении предмета из списка покупок"


def edit_task(task_index, chat_id, text):
    """Изменение задачи пользователя"""
    cursor, db = get_connection()
    try:
        sql = 'UPDATE user_tasks SET text = ? WHERE id = ? AND user_id = ?'
        cursor.execute(sql, (text, int(task_index), chat_id))
        db.commit()
        return "Предмет в списке покупок успешно обновлена"
    except:
        return "Возникла ошибка при обновлении предмета в списке покупок"


def edit_task_num(new_task_id, task_index, chat_id):
    """Изменение номера задачи пользователя"""
    cursor, db = get_connection()
    try:
        sql = 'UPDATE user_tasks SET id = ? WHERE id = ? AND user_id = ?'
        cursor.execute(sql, (new_task_id, int(task_index), chat_id))
        db.commit()
        return "Предмет в списке покупок успешно обновлен"
    except:
        return "Возникла ошибка при обновлении предмета в списке покупок"

def get_all_shops(user_id):
    """Получение всех задач пользователя"""
    cursor, db = get_connection()
    cursor.execute(f"SELECT * FROM user_shops WHERE user_id == {user_id}")
    return cursor.fetchall()

def delete_shop(id, user_id):
    """Удаление задачи пользователю"""
    cursor, db = get_connection()
    try:
        sql = 'DELETE FROM user_shops WHERE id = ? AND user_id = ?'
        cursor.execute(sql, (int(id), user_id))
        db.commit()
        return "Магазин успешно удален"
    except:
        return "Возникла ошибка при удалении магазина"

def edit_shop_num(new_task_id, task_index, chat_id):
    """Изменение номера задачи пользователя"""
    cursor, db = get_connection()
    try:
        sql = 'UPDATE user_shops SET id = ? WHERE id = ? AND user_id = ?'
        cursor.execute(sql, (new_task_id, int(task_index), chat_id))
        db.commit()
        return "Магазин успешно обновлена"
    except:
        return "Возникла ошибка при обновлении магазина"

def add_shop(id, user_id, shop):
    """Добавление задачи пользователю"""
    cursor, db = get_connection()
    try:
        sql = '''INSERT INTO user_shops (id, user_id, name) VALUES (?, ?, ?);'''
        cursor.execute(sql, (id, user_id, shop))
        db.commit()
        return "Магазин добавлен успешно"
    except:
        return "Возникла ошибка при добавлении магазина"
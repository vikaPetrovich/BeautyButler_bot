import sqlite3


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    def init_tables(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                username VARCHAR(100) NOT NULL,
                registration_date DATE DEFAULT CURRENT_DATE,
                chat_id INTEGER
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS appointments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service VARCHAR(100),
                specialist VARCHAR(100),
                date_recording DATE,
                time_recording TIME,
                confirmation_record BOOLEAN,
                chat_id INTEGER
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS service_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_service VARCHAR (100),
                price_service INTEGER
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS specialist_info(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_specialist VARCHAR,
                position_specialist VARCHAR,
                message_form_name_specialist VARCHAR
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS working_hours(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_specialist CHAR,
                date_work DATE,
                time_work TIME,
                taken_time BOOLEAN,
                day_of_week CHAR
            )
        ''')

    # проверка наличия пользователя в бд
    def get_user_count(self, username, chat_id):
        self.cur.execute("SELECT COUNT(*) FROM users WHERE username = ? AND chat_id = ?",
                         (username, chat_id))
        count = self.cur.fetchone()[0]
        return count

    # добавление нового пользователя
    def add_new_user(self, username, chat_id):
        self.cur.execute("INSERT INTO users (username, chat_id) VALUES (?, ?)", (username, chat_id))
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

    # вытаскивание информации о специалисте
    def get_specialist(self):
        self.cur.execute("SELECT name_specialist, position_specialist FROM specialist_info")
        return self.cur.fetchall()

    # вытаскивание имени в нужной форме
    def get_specialist_message_form(self, name_specialist):
        self.cur.execute("SELECT message_form_name_specialist FROM specialist_info WHERE name_specialist =?",
                         (name_specialist,))
        return self.cur.fetchone()

    # добавление новой записи
    def add_appointment(self, service, specialist, date, time, confirmation_record, chat_id):
        self.cur.execute(
            "INSERT INTO appointments (service, specialist, date_recording, time_recording, confirmation_record, chat_id) VALUES (?, ?, ?, ?, ?, ?)",
            (service, specialist, date, time, confirmation_record, chat_id))
        self.conn.commit()

    # проверка на появление новой записи в бд
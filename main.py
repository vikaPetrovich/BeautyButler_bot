import telebot
import config
from telebot import types
import calendar_module
import time_module
from db import Database
from datetime import datetime, timedelta
import specialists_module

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Главное меню', callback_data='menu')
    markup.row(btn1)
    bot.send_message(message.chat.id,
                     'Привет, я помогу тебе бысто и удобно записаться на нужные услуги.',
                     reply_markup=markup)

    db = Database(config.DB_FILE)
    db.init_tables()

    username = message.from_user.first_name
    chat_id = message.chat.id

    count = db.get_user_count(username, chat_id)

    if count == 0:
        db.add_new_user(username, chat_id)

    db.close()

'''    
@bot.message_handler(commands=['star'])
def star1(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Подтвердить', callback_data='yes')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data='no')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id,
                     'Привет, ты записана на 30 апреля в 10:00 к мастеру Ане.\nПодтведи, пожалуйста, свой визит 💌',
                     reply_markup=markup)
    bot.send_message(message.chat.id,
                     'Отлично. С нетерпением ждем тебя в нашей уютной студии 🤍')
'''

@bot.message_handler(commands=['menu'])
def menu(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Выбрать услугу')
    btn2 = types.KeyboardButton('Выбрать специалиста')
    btn3 = types.KeyboardButton('Выбрать  дату и время')
    btn4 = types.KeyboardButton('Просмотреть все мои записи')
    markup1.row(btn1)
    markup1.row(btn2)
    markup1.row(btn3)
    markup1.row(btn4)
    bot.send_message(message.chat.id, 'Ты в главном меню', reply_markup=markup1)


@bot.message_handler(commands=['calendar'])
def send_calendar_command(message):
    calendar_module.send_calendar(bot, message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'menu')
def menu(callback):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Выбрать услугу')
    btn2 = types.KeyboardButton('Выбрать специалиста')
    btn3 = types.KeyboardButton('Выбрать  дату и время')
    btn4 = types.KeyboardButton('Все мои записи')
    btn5 = types.KeyboardButton('Акции')
    markup1.row(btn1)
    markup1.row(btn2)
    markup1.row(btn3)
    markup1.row(btn4,btn5)
    bot.send_message(callback.message.chat.id, 'Отлично💕\nТы в главном меню', reply_markup=markup1)


@bot.message_handler(content_types=['text'])
def handle_messages(message):
    chat_id = message.chat.id
    if message.text == 'Выбрать услугу':

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Маникюр', callback_data='manicure')
        btn2 = types.InlineKeyboardButton('Педикюр', callback_data='pedicure')
        btn3 = types.InlineKeyboardButton('Дополнительные услуги', callback_data='additional_services')
        markup.row(btn1)
        markup.row(btn2)
        markup.row(btn3)
        bot.send_message(chat_id, 'Выберете услугу', reply_markup=markup)

    elif message.text == 'Выбрать специалиста':
        db = Database(config.DB_FILE)
        db.init_tables()
    elif message.text == 'Выбрать  дату и время':
        db = Database(config.DB_FILE)
        db.init_tables()


'''\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'''
# услуга

@bot.callback_query_handler(func=lambda callback: callback.data == 'manicure')
def manicure(callback):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Маникюр с покрытием гель-лак                    1700р.', callback_data='gel_manicure')
    btn2 = types.InlineKeyboardButton('1700р.', callback_data='ignore', row_width=2)
    btn3 = types.InlineKeyboardButton('Маникюр без покрытия                                     1500р.', callback_data='pedicure')
    markup.row(btn1)
    markup.row(btn3)
    bot.send_message(callback.message.chat.id, 'Услуги по маникюру', reply_markup=markup)

user_appointment = {}



@bot.callback_query_handler(func=lambda callback: callback.data == 'gel_manicure')
def gel_manicure(callback):
    specialists_module.send_specialists_list(bot, callback.message)
    user_appointment[callback.message.chat.id] = {'service': ''}
    user_appointment[callback.message.chat.id]['service'] = 'Маникюр с покрытием гель-лак'
    print(user_appointment)


'''\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'''
# дата
cur_year = datetime.now().year
cur_month = datetime.now().month
selected_dates = []


@bot.callback_query_handler(func=lambda call: call.data in ["PREV-MONTH", "NEXT-MONTH"])
def callback_query(callback):
    global cur_year, cur_month
    cur_year, cur_month = calendar_module.handle_month_change(bot, callback, cur_year, cur_month)


@bot.callback_query_handler(func=lambda call: call.data.startswith("DAY"))
def callback_day(callback):
    global selected_dates
    selected_dates = calendar_module.handle_date_selection(callback, cur_year, cur_month, selected_dates)


@bot.callback_query_handler(func=lambda call: call.data.startswith("done"))
def accept_day(callback):
    if not selected_dates:
        bot.answer_callback_query(callback.id, "Пожалуйста, выберите дату перед нажатием кнопки Готово'")
        return

    date_str = datetime.strptime(selected_dates[0], '%Y-%m-%d')
    english_month = date_str.strftime("%B")
    russian_month = config.MONTHS.get(english_month, english_month)
    formatted_date = f"{date_str.day} {russian_month}"

    # Преобразование даты в тип данных дата
    now = datetime.strptime(selected_dates[0], '%Y-%m-%d').date()
    print(now)
    today = datetime.now().date()
    if now < today:
        bot.answer_callback_query(callback.id, "Вы не можете выбрать прошедшую дату. Пожалуйста, выберите другую дату.")
        selected_dates.clear()
        return
    user_appointment[callback.message.chat.id]['date'] = formatted_date
    print(user_appointment)
    time_module.send_time_table(formatted_date, bot, callback.message)


'''\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'''
# время

selected_time = ''
cur_day = ''
doble_selected_days = selected_dates

@bot.callback_query_handler(func=lambda call: call.data.startswith("TIME"))
def callback_day(callback):
    global selected_time
    selected_time = time_module.handle_time_selection(callback, selected_time)


@bot.callback_query_handler(func=lambda call: call.data in ["PREV-DAY", "NEXT-DAY"])
def callback_query(callback):
    cur_day_str, cur_day = time_module.handle_day_change(bot, callback, selected_dates)
    selected_dates[0]=cur_day_str
    if cur_day !=0:
        user_appointment[callback.message.chat.id]['date'] = cur_day



@bot.callback_query_handler(func=lambda call: call.data.startswith("ok"))
def accept_day(callback):
    global selected_time

    if selected_time == '':
        bot.answer_callback_query(callback.id, "Пожалуйста, выберите время перед нажатием кнопки Готово")
        return

    user_appointment[callback.message.chat.id]['time'] = selected_time
    print(user_appointment)
    selected_time = ''
    db = Database(config.DB_FILE)
    db.init_tables()
    specialist_in_message = db.get_specialist_message_form(user_appointment[callback.message.chat.id]['specialist'])
    db.close()

    bot.send_message(callback.message.chat.id,
                     f"Вы записались на {user_appointment[callback.message.chat.id]['date']} в {user_appointment[callback.message.chat.id]['time']} к мастеру {specialist_in_message[0]}")
    uploading_to_db(user_appointment)



def uploading_to_db(user_appointment):
    db = Database(config.DB_FILE)
    db.init_tables()
    chat_id = list(user_appointment.keys())[0]
    service = user_appointment[chat_id]['service']
    specialist = user_appointment[chat_id]['specialist']

    date = user_appointment[chat_id]['date']

    day, month_name = date.split()

    # Преобразование названия месяца в номер месяца
    month_number = list(config.MONTHS.values()).index(month_name) + 1

    cur_year = datetime.now().year
    cur_month = datetime.now().month
    if month_number < cur_month:
        cur_year += 1

    # Формирование даты в формате "YYYY-MM-DD"
    formatted_date = f"{cur_year}-{month_number:02d}-{int(day):02d}"

    # Формирование времени
    time_str = user_appointment[chat_id]['time']
    time_obj = datetime.strptime(time_str, '%H:%M').time()
    time_str_formatted = time_obj.strftime('%H:%M')

    db.add_appointment(service, specialist, formatted_date, time_str_formatted, False, chat_id)

    db.close()
    user_appointment[chat_id].clear()
    selected_dates.clear()


'''\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'''
# специалист

selected_specialist = ''


@bot.callback_query_handler(func=lambda call: call.data.startswith("SPECIALIST"))
def callback_specialist(callback):
    global selected_specialist
    selected_specialist = specialists_module.handle_specialists_selection(callback, selected_specialist)

    user_appointment[callback.message.chat.id]['specialist'] = selected_specialist
    print(user_appointment)
    calendar_module.send_calendar(bot, callback.message)


bot.polling(none_stop=True, timeout=30)

from telebot import types
from db import Database
import config


def send_specialists_list(bot, message):
    bot.send_message(message.chat.id, "Выберите специалиста", reply_markup=generate_specialists_list(message))


def generate_specialists_list(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    db = Database(config.DB_FILE)
    db.init_tables()

    specialists = db.get_specialist()

    db.close()
    for el in specialists:
        keyboard.add(types.InlineKeyboardButton(el[0], callback_data="SPECIALIST"+ el[0]))

    return keyboard


def handle_specialists_selection(callback, selected_specialist):
    selected_specialist = callback.data[10:]
    return selected_specialist

from telebot import types
import config
from datetime import datetime, timedelta



def send_time_table(day, bot, message):
    bot.send_message(message.chat.id, "Выберите время", reply_markup=generate_time_table(day))


standard_time = {'Утро': ['09:00', '09:30', '10:00'],
                 'День': ['17:00', '17:30'],
                 'Вечер': ['18:00', '18:30']
                 }


def generate_time_table(day):
    keyboard = types.InlineKeyboardMarkup(row_width=3)

    # Кнопки переключения дня
    keyboard.add(
        types.InlineKeyboardButton("<", callback_data="PREV-DAY"),
        types.InlineKeyboardButton(f"{day}", callback_data="IGNORE"),
        types.InlineKeyboardButton(">", callback_data="NEXT-DAY")
    )

    for period, times in standard_time.items():
        keyboard.add(types.InlineKeyboardButton(period, callback_data="IGNORE"))
        row = []
        for el in times:
            row.append(types.InlineKeyboardButton(str(el), callback_data=f"TIME{el}"))
        keyboard.add(*row)
    keyboard.add(
        types.InlineKeyboardButton("Готово", callback_data="ok")
    )
    return keyboard


def handle_day_change(bot, callback, selected_dates):
    if callback.data == "PREV-DAY":
        print(selected_dates)
        now = datetime.strptime(selected_dates[0], '%Y-%m-%d').date()
        print(now)

        # Предыдущая дата
        prev_date = now - timedelta(days=1)
        cur_day_str = prev_date_str = prev_date.strftime('%Y-%m-%d')

        date_str = datetime.strptime(prev_date_str, '%Y-%m-%d')
        english_month = date_str.strftime("%B")
        russian_month = config.MONTHS.get(english_month, english_month)
        cur_day = f"{date_str.day} {russian_month}"
        print(cur_day)

        prev_date_dt = datetime.strptime(prev_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        if prev_date_dt < today:
            bot.answer_callback_query(callback.id,
                                      "Вы не можете выбрать прошедшую дату. Пожалуйста, выберите другую дату.")

            return selected_dates[0], 0

    elif callback.data == "NEXT-DAY":
        print(selected_dates)
        now = datetime.strptime(selected_dates[0], '%Y-%m-%d').date()
        print(now)
        # Следующая дата
        next_date = now + timedelta(days=1)

        cur_day_str = next_date_str = next_date.strftime('%Y-%m-%d')

        date_str = datetime.strptime(next_date_str, '%Y-%m-%d')
        english_month = date_str.strftime("%B")
        russian_month = config.MONTHS.get(english_month, english_month)
        cur_day = f"{date_str.day} {russian_month}"

    bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=generate_time_table(cur_day)
    )

    return cur_day_str, cur_day


def handle_time_selection(callback, selected_time):
    selected_time = callback.data[4:]
    return selected_time

from datetime import datetime
from telebot import types
import calendar


def send_calendar(bot, message):
    now = datetime.now()
    bot.send_message(message.chat.id, "Выберите дату", reply_markup=generate_calendar(now.year, now.month))


def generate_calendar(year, month):
    keyboard = types.InlineKeyboardMarkup(row_width=7)
    month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
                   "Ноябрь", "Декабрь"]

    # Кнопки переключения месяца
    keyboard.add(
        types.InlineKeyboardButton("<", callback_data="PREV-MONTH"),
        types.InlineKeyboardButton(f"{month_names[month - 1]} {str(year)}", callback_data="IGNORE"),
        types.InlineKeyboardButton(">", callback_data="NEXT-MONTH")
    )

    # Дни недели
    keyboard.add(*[types.InlineKeyboardButton(day, callback_data="IGNORE") for day in
                   ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]])

    # Даты
    for week in calendar.monthcalendar(year, month):
        row = []
        for day in week:
            if day == 0:
                row.append(types.InlineKeyboardButton(" ", callback_data="IGNORE"))
            else:
                row.append(types.InlineKeyboardButton(str(day), callback_data="DAY" + str(day)))
        keyboard.add(*row)

    keyboard.add(types.InlineKeyboardButton("Готово", callback_data="done"))
    return keyboard


def handle_month_change(bot: object, callback: object, cur_year: object, cur_month: object) -> object:
    if callback.data == "PREV-MONTH":
        cur_month -= 1
        if cur_month < 1:
            cur_month = 12
            cur_year -= 1
    elif callback.data == "NEXT-MONTH":
        cur_month += 1
        if cur_month > 12:
            cur_month = 1
            cur_year += 1

    bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=generate_calendar(cur_year, cur_month)
    )

    return cur_year, cur_month


def handle_date_selection(callback, cur_year, cur_month, selected_dates):
    date = int(callback.data[3:])
    year = cur_year
    month = cur_month
    date_dt = datetime(year, month, date)
    formatted_date = date_dt.strftime("%Y-%m-%d")
    selected_dates.append(formatted_date)
    return selected_dates


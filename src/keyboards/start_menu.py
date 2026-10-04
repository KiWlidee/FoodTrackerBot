from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Статистика"),
        KeyboardButton(text="💧 Вода")],
        [KeyboardButton(text="📊 Цели КБЖУ")],
        [KeyboardButton(text="📋 Изменить статистику")],
        [KeyboardButton(text="🆘 Поддержка")]
    ],
    resize_keyboard=True
)


stats_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⚡️ Сегодня")],
        [KeyboardButton(text="⏪ Вчера")]
    ],
    resize_keyboard=True
)
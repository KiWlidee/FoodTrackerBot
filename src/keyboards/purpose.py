from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kbzhu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💧 Воду"),
        KeyboardButton(text="🔥 Каллории")],
        [KeyboardButton(text="🥩 Белки"),
        KeyboardButton(text="🧈 Жиры")],
        [KeyboardButton(text="🍞 Углеводы"),
        KeyboardButton(text="⏪ Назад")],
    ],
    resize_keyboard=True
)


kbzhu_edit = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✏️ Изменить")],
        [KeyboardButton(text="⏪ Назад")],
    ],
    resize_keyboard=True
)



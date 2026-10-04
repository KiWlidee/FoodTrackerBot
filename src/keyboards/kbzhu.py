from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kbzhu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💧 Bоду"),
        KeyboardButton(text="🔥 Kаллории")],
        [KeyboardButton(text="🥩 Бeлки"),
        KeyboardButton(text="🧈 Жиpы")],
        [KeyboardButton(text="🍞 Углeводы"),
        KeyboardButton(text="⏪ Назад")],
    ],
    resize_keyboard=True
)
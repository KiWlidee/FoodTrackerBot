from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


support = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Написать")],
        [KeyboardButton(text="❌ Не писать")]
    ],
    resize_keyboard=True
)
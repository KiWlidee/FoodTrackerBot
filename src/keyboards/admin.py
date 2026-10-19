from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👑 Админ")],
        [KeyboardButton(text="📅 Статистика"),
        KeyboardButton(text="💧 Вода")],
        [KeyboardButton(text="📊 Цели КБЖУ")],
        [KeyboardButton(text="📋 Изменить статистику")],
        [KeyboardButton(text="🆘 Поддержка")]
    ],
    resize_keyboard=True
)


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🆘 Сообщения в саппорт"), KeyboardButton(text="🚫 Бан")],
        [KeyboardButton(text="📄 Логи + ДБ"), KeyboardButton(text="⭐ Подписка")],
        [KeyboardButton(text="⏪ Назад")]
    ],
    resize_keyboard=True
)
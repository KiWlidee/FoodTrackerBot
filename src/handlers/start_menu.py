import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import cred.users as cred_users
import keyboards.start_menu as kb


router = Router()


@router.message(Command("start"))
async def start_menu(message: Message):
    user = await cred_users.find_user_by_tg_id(message)
    if not user:
        await cred_users.add_new_user(message)
    logging.debug(f"@{message.from_user.username} нажал на start. ID: {message.from_user.id}")
    await message.answer(f"""Привет, {message.from_user.first_name}! Я помогаю вести питание.

• 🖼️ Пришли фото блюда — распознаю состав.
• 💧 Вода — запишу воду.
• 📅 Сегодня — сводка дня. 
• 🔍 Анализ — для анализа КБЖУ по вашему описанию, просто начните писать.""",
                         reply_markup=kb.start_menu)
#  • 🗂️ Меню.
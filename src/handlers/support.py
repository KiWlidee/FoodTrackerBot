from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import keyboards.start_menu as kb
from database import async_session
import keyboards.support as sup_kb


router = Router()


class Wait(StatesGroup):
    waiting_support = State()


@router.message(F.text == "🆘 Поддержка")
async def support(message: Message):
    await message.answer("Если вы нашли баг или у вас есть важные вопросы, вы можете написать в поддержку.",
                         reply_markup=sup_kb.support)


@router.message(F.text == "📝 Написать")
async def write_support(message: Message, state: FSMContext):
    await message.answer("Напишите ваше обращение",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Wait.waiting_support)


@router.message(Wait.waiting_support)
async def waiting_support(message: Message, state: FSMContext):
    if len(message.text) > 300:
        await message.answer("Превышена максимальная длина сообщения",
                             reply_markup=kb.start_menu)
        await state.clear()
        return
    user_id = message.from_user.id
    username = message.from_user.username or "нет username"
    full_name = message.from_user.full_name
    text = message.text

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"=== {timestamp} ===\n"
        f"ID: {user_id}\n"
        f"Имя: {full_name}\n"
        f"Username: @{username}\n"
        f"Сообщение: {text}\n\n"
    )

    file_path = "support_requests.txt"
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry)

    await message.answer("✅ Ваше обращение принято! Мы свяжемся с вами.",
                         reply_markup=kb.start_menu)
    await state.clear()
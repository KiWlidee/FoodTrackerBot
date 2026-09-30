import base64

from datetime import date, timedelta, datetime

import openai

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import cred.user_daily_tracking as tracking_cred
import cred.users as users_cred
import keyboards.start_menu as kb
from ai import ask_ai, ask_ai_vision
from database import async_session
import keyboards.support as sup_kb


router = Router()


class Wait(StatesGroup):
    waiting_water = State()
    waiting_support = State()

@router.message(F.text == "💧 Вода")
async def water(message: Message, state: FSMContext):
    await message.answer("Напишите, сколько мл воды добавить", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Wait.waiting_water)


@router.message(Wait.waiting_water)
async def water_add(message: Message, state: FSMContext):
    add = await tracking_cred.add_water(message)
    if not add:
        await message.answer("Пришли число, например: 500")
    else:
        await message.answer("💧 Вода добавлена!", reply_markup=kb.start_menu)
    await state.clear()


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


@router.message(F.text == "❌ Не писать")
async def write_support(message: Message, state: FSMContext):
    await message.answer("Меню...",
                                reply_markup=kb.start_menu)
    await state.clear()


@router.message(F.text == "📊 Изменить свое КБЖУ")
async def kbzhu_edit(message: Message, state: FSMContext):

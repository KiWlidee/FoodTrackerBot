import base64

from datetime import date, timedelta

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


router = Router()


class Wait(StatesGroup):
    waiting = State()


@router.message(F.text == "📅 Статистика")
async def today_stats(message: Message):
    await message.answer("Выберите статистику за сегодня/вчера", reply_markup=kb.stats_menu)


@router.message(F.text == "⚡️ Сегодня")
async def stats_today(message: Message):
    day = date.today()
    res = await tracking_cred.kbzhu_stats(message=message, day=day)
    if res:
        await message.answer(
            f"""📅 {day}
💧 Вода: {res.water_ml}
🔥 Каллории: {res.calories}
🥩 Белки: {res.protein}
🧈 Жиры: {res.fat}
🍞 Углеводы: {res.carbs}""",
            reply_markup=kb.start_menu
        )
    else:
        await message.answer("Статистика обновлена! Попробуйте еще раз.",
                             reply_markup=kb.start_menu)


@router.message(F.text == "⏪ Вчера")
async def stats_yesterday(message: Message):
    yesterday = date.today() - timedelta(days=1)
    res = await tracking_cred.kbzhu_stats(message=message, day=yesterday)
    if res:
        await message.answer(
            f"""📅 {yesterday}
💧 Вода: {res.water_ml}
🔥 Каллории: {res.calories}
🥩 Белки: {res.protein}
🧈 Жиры: {res.fat}
🍞 Углеводы: {res.carbs}""",
            reply_markup=kb.start_menu
        )
    else:
        await message.answer(
            f"""📅 {yesterday}
💧 Вода: 0.0
🔥 Каллории: 0.0
🥩 Белки: 0.0
🧈 Жиры: 0.0
🍞 Углеводы: 0.0""",
            reply_markup=kb.start_menu
        )


@router.message(F.text)
async def analysis(message: Message):
    thinking = await message.answer("⏳ Считаю...")
    answer = await ask_ai(message.text)
    await thinking.delete()
    await message.answer(answer,
                         reply_markup=kb.start_menu)


@router.message(F.photo)
async def handle_photo(message: Message):
    thinking = await message.answer("🔍 Анализирую фото...")
    try:
        photo = message.photo[-1]

        file = await message.bot.get_file(photo.file_id)
        file_bytes = await message.bot.download_file(file.file_path)
        image_bytes = file_bytes.read()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        answer = await ask_ai_vision(base64_image, "Посчитай КБЖУ этого блюда")

        await thinking.delete()
        await message.answer(answer)
    except Exception as e:
        print(e)
        await thinking.delete()
        await message.answer("Не удалось обработать фото. Попробуйте ещё раз.")
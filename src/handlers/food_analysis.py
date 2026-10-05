import logging
from datetime import date, timedelta, datetime
from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup

import cred.user_daily_tracking as tracking_cred
import cred.photo_analysis as photo_analysis
import keyboards.start_menu as kb
from ai import ask_ai
from database import async_session


router = Router()

PHOTO_DIR = Path("photos")
PHOTO_DIR.mkdir(exist_ok=True)


class Wait(StatesGroup):
    waiting = State()


@router.message(F.text == "📅 Статистика")
async def today_stats(message: Message):
    await message.answer("Выберите статистику за сегодня/вчера",
                         reply_markup=kb.stats_menu)


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
        logging.debug(
            f"{message.from_user.id} вывел статистику за сегодня (handlers.food_analysis.stats_today)"
                      )
    else:
        logging.info(
            f"{message.from_user.id} обновил свою дневную статистику за сегодня"
                     )
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
        logging.debug(
            f"{message.from_user.id} вывел статистику за вчера (handlers.food_analysis.stats_yesterday)"
                      )
    else:
        logging.info(
            f"{message.from_user.id} обновил свою дневную статистику за вчера"
                     )
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

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"=== {timestamp} ===\n"
        f"ID: {message.from_user.id}\n"
        f"Имя: {message.from_user.full_name}\n"
        f"Username: @{message.from_user.username}\n"
        f"Сообщение: {message.text}\n\n"
    )

    file_path = "food_analysis_requests.txt"
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry)

    logging.info(
        f"{message.from_user.id} Написал {message.text} в анализ еды. (handlers.food_analysis.analysis)"
    )

@router.message(F.photo)
async def analysis_photo(message: Message):
    thinking = await message.answer("🔍 Анализирую фото...")
    result = await photo_analysis.analys_photo(message)
    await thinking.delete()
    await message.answer(result)

    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = PHOTO_DIR / f"{message.from_user.id}_{photo.file_unique_id}.jpg"
    await message.bot.download_file(file.file_path, file_path)

    logging.info(
        f"{message.from_user.id} отправил фото в анализ еды. (handlers.food_analysis.analysis_photo)"
    )
    logging.info(f"Фото сохранено: {file_path}")
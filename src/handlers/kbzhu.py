import logging

from datetime import date

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import cred.user_daily_tracking as tracking_cred
import keyboards.kbzhu as kbzhu_kb

from database import async_session
from models.purpose_tracking import Purpose


router = Router()


class Wait(StatesGroup):
    change_water = State()
    change_calories = State()
    change_protein = State()
    change_fat = State()
    change_carbs = State()


@router.message(F.text == "📋 Изменить статистику")
async def stats_edit(message: Message):
    logging.debug(
        f"{message.from_user.id} нажал на: Изменить статистику (handlers.kbzhu.stats_edit)"
                  )
    await message.answer("Выберете что будете менять",
                         reply_markup=kbzhu_kb.kbzhu)


@router.message(F.text == "💧 Bоду")
async def stats_water_edit(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} нажал на: 💧 Bоду (handlers.kbzhu.stats_water_edit)"
                  )
    await message.answer(
        "Если хотите добавить значение, просто напишите число (20, 40). Если уменьшить, то значение с минусом (-20, -40)",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Wait.change_water)


@router.message(Wait.change_water)
async def stats_water_edit_waiting(message: Message, state: FSMContext):
    day = date.today()
    res = await tracking_cred.kbzhu_one_edit(message, "water", day)
    if res["status"] == "OK":
        logging.debug(
            f"{message.from_user.id} изменил: 💧 Bоду (handlers.kbzhu.stats_water_edit_waiting) на: {message.text}"
        )
        await message.answer("Готово!",
                             reply_markup=kbzhu_kb.kbzhu)
    else:
        logging.debug(
            f"{message.from_user.id} не получилось изменить: 💧 Bоду (handlers.kbzhu.stats_water_edit_waiting) на: {message.text}"
        )
        await message.answer(f"❌ Произошла ошибка ({res})... Попробуйте снова и если она не пропадет, отправьте ее в поддержку.",
                             reply_markup=kbzhu_kb.kbzhu)
    await state.clear()


@router.message(F.text == "🔥 Kаллории")
async def stats_calories_edit(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} нажал на: 🔥 Kаллории (handlers.kbzhu.stats_calories_edit)"
    )
    await message.answer(
        "Если хотите добавить значение, просто напишите число (100, 200). Если уменьшить, то значение с минусом (-100, -200)",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Wait.change_calories)


@router.message(Wait.change_calories)
async def stats_calories_edit_waiting(message: Message, state: FSMContext):
    day = date.today()
    res = await tracking_cred.kbzhu_one_edit(message, "calories", day)
    if res["status"] == "OK":
        logging.debug(
            f"{message.from_user.id} изменил: 🔥 Kаллории (handlers.kbzhu.stats_calories_edit_waiting) на: {message.text}"
        )
        await message.answer("Готово!", reply_markup=kbzhu_kb.kbzhu)
    else:
        logging.debug(
            f"{message.from_user.id} не получилось изменить: 🔥 Kаллории (handlers.kbzhu.stats_calories_edit_waiting) на: {message.text}"
        )
        await message.answer(f"❌ Произошла ошибка ({res})... Попробуйте снова и если она не пропадет, отправьте ее в поддержку.",
                             reply_markup=kbzhu_kb.kbzhu)
    await state.clear()


@router.message(F.text == "🥩 Бeлки")
async def stats_protein_edit(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} нажал на: 🥩 Бeлки (handlers.kbzhu.stats_protein_edit)"
    )
    await message.answer(
        "Если хотите добавить значение, просто напишите число (10, 20). Если уменьшить, то значение с минусом (-10, -20)",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Wait.change_protein)


@router.message(Wait.change_protein)
async def stats_protein_edit_waiting(message: Message, state: FSMContext):
    day = date.today()
    res = await tracking_cred.kbzhu_one_edit(message, "protein", day)
    if res["status"] == "OK":
        logging.debug(
            f"{message.from_user.id} изменил: 🥩 Бeлки (handlers.kbzhu.stats_protein_edit_waiting) на: {message.text}"
        )
        await message.answer("Готово!", reply_markup=kbzhu_kb.kbzhu)
    else:
        logging.debug(
            f"{message.from_user.id} не получилось изменить: 🥩 Бeлки (handlers.kbzhu.stats_protein_edit_waiting) на: {message.text}"
        )
        await message.answer(f"❌ Произошла ошибка ({res})... Попробуйте снова и если она не пропадет, отправьте ее в поддержку.",
                             reply_markup=kbzhu_kb.kbzhu)
    await state.clear()


@router.message(F.text == "🧈 Жиpы")
async def stats_fat_edit(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} нажал на: 🧈 Жиpы (handlers.kbzhu.stats_fat_edit)"
    )
    await message.answer(
        "Если хотите добавить значение, просто напишите число (10, 20). Если уменьшить, то значение с минусом (-10, -20)",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Wait.change_fat)


@router.message(Wait.change_fat)
async def stats_fat_edit_waiting(message: Message, state: FSMContext):
    day = date.today()
    res = await tracking_cred.kbzhu_one_edit(message, "fat", day)
    if res["status"] == "OK":
        logging.debug(
            f"{message.from_user.id} изменил: 🧈 Жиpы (handlers.kbzhu.stats_fat_edit_waiting) на: {message.text}"
        )
        await message.answer("Готово!", reply_markup=kbzhu_kb.kbzhu)
    else:
        logging.debug(
            f"{message.from_user.id} не получилось изменить: 🧈 Жиpы (handlers.kbzhu.stats_fat_edit_waiting) на: {message.text}"
        )
        await message.answer(f"❌ Произошла ошибка ({res})... Попробуйте снова и если она не пропадет, отправьте ее в поддержку.",
                             reply_markup=kbzhu_kb.kbzhu)
    await state.clear()


@router.message(F.text == "🍞 Углeводы")
async def stats_carbs_edit(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} нажал на: 🍞 Углeводы (handlers.kbzhu.stats_carbs_edit)"
    )
    await message.answer(
        "Если хотите добавить значение, просто напишите число (10, 20). Если уменьшить, то значение с минусом (-10, -20)",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Wait.change_carbs)


@router.message(Wait.change_carbs)
async def stats_carbs_edit_waiting(message: Message, state: FSMContext):
    day = date.today()
    res = await tracking_cred.kbzhu_one_edit(message, "carbs", day)
    if res["status"] == "OK":
        logging.debug(
            f"{message.from_user.id} изменил: 🍞 Углeводы (handlers.kbzhu.stats_carbs_edit_waiting) на: {message.text}"
        )
        await message.answer("Готово!", reply_markup=kbzhu_kb.kbzhu)
    else:
        logging.debug(
            f"{message.from_user.id} не получилось изменить: 🍞 Углeводы (handlers.kbzhu.stats_carbs_edit_waiting) на: {message.text}"
        )
        await message.answer(f"❌ Произошла ошибка ({res})... Попробуйте снова и если она не пропадет, отправьте ее в поддержку.",
                             reply_markup=kbzhu_kb.kbzhu)
    await state.clear()
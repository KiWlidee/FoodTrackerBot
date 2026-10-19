import logging

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import cred.user_daily_tracking as tracking_cred
import cred.purpose_tracking as purpose_cred
import keyboards.start_menu as kb
import keyboards.purpose as purpose_kb

from database import async_session
from models.purpose_tracking import Purpose


router = Router()


class Wait(StatesGroup):
    waiting_water = State()
    waiting_purpose = State()
    purpose_water = State()
    purpose_calories = State()
    purpose_protein = State()
    purpose_fat = State()
    purpose_carbs = State()


@router.message(F.text == "💧 Вода")
async def water(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} пробует изменить: 💧 Вода (handlers.purpose.water)"
                  )
    await message.answer("Напишите, сколько мл воды добавить", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Wait.waiting_water)


@router.message(Wait.waiting_water)
async def water_add(message: Message, state: FSMContext):
    add = await tracking_cred.add_water(message)
    if not add:
        logging.debug(
            f"{message.from_user.id} не смог изменить: 💧 Вода (handlers.purpose.water_add) на: {message.text}"
        )
        await message.answer("Пришли число, например: 500")
    else:
        logging.debug(
            f"{message.from_user.id} изменил: 💧 Вода (handlers.purpose.water_add) на: {message.text}"
        )
        await message.answer("💧 Вода добавлена!", reply_markup=kb.start_menu)
    await state.clear()


@router.message(F.text == "❌ Не писать")
async def write_support(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} нажал на: ❌ Не писать и вернулся в меню (handlers.purpose.write_support)"
    )
    await message.answer("Меню...",
                                reply_markup=kb.start_menu)
    await state.clear()


@router.message(F.text == "🎯 Цель")
async def purpose(message: Message):
    logging.debug(
        f"{message.from_user.id} Нажал на: 🎯 Цель (handlers.purpose.purpsose)"
    )
    purpose = await purpose_cred.find_purpose(message)
    if isinstance(purpose, Purpose):
        logging.debug(
            f"{message.from_user.id} вывел свои цели (handlers.purpose.purpsose)"
        )
        await message.answer(f"""🎯 Ваши цели:
💧 Вода: {purpose.water_ml}
🔥 Каллории: {purpose.calories}
🥩 Белки: {purpose.protein}
🧈 Жиры: {purpose.fat}
🍞 Углеводы: {purpose.carbs}
    """,
                             reply_markup=kb.start_menu)
    else:
        logging.debug(
            f"{message.from_user.id} не смог вывести свои цели (handlers.purpose.purpsose)"
        )
        await message.answer("❌ Цели не найдено. Попробуйте снова.",
                             reply_markup=kb.start_menu)


@router.message(F.text == "📊 Цели КБЖУ")
async def kbzhu_edit(message: Message):
    logging.debug(
        f"{message.from_user.id} Нажал на: 📊 Цели КБЖУ (handlers.purpose.kbzhu_edit)"
    )
    purpose = await purpose_cred.find_purpose(message)
    if isinstance(purpose, Purpose):
        logging.debug(
            f"{message.from_user.id} вывел свои цели по КБЖУ (handlers.purpose.kbzhu_edit)"
        )
        await message.answer(f"""🎯 Ваши цели:
💧 Вода: {purpose.water_ml}
🔥 Каллории: {purpose.calories}
🥩 Белки: {purpose.protein}
🧈 Жиры: {purpose.fat}
🍞 Углеводы: {purpose.carbs}
        """,
                             reply_markup=purpose_kb.kbzhu_edit)
    else:
        logging.debug(
            f"{message.from_user.id} не смог вывести свои цели по КБЖУ (handlers.purpose.kbzhu_edit)"
        )
        await message.answer("❌ Цели не найдено. Попробуйте снова.",
                             reply_markup=kb.start_menu)


@router.message(F.text == "✏️ Изменить")
async def purpose_edit(message: Message):
    logging.debug(
        f"{message.from_user.id} Пробует изменить свои цели (handlers.purpose.purpose_edit)"
    )
    await message.answer("Что бы вы хотели изменить?",
                         reply_markup=purpose_kb.kbzhu)


@router.message(F.text == "💧 Воду")
async def purpose_water_edit(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} Пробует изменить свою цель: 💧 Воду (handlers.purpose.purpose_water_edit)"
    )
    await message.answer("Введите цель",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Wait.purpose_water)


@router.message(Wait.purpose_water)
async def purpose_water_editing(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} Изменил свою цель: 💧 Воду (handlers.purpose.purpose_water_edit) на: {message.text}"
    )
    purpose = "water"
    res = await purpose_cred.edit_one_purpose(message, purpose)
    await message.answer("✅ Готово",
                         reply_markup=purpose_kb.kbzhu)
    await state.clear()


@router.message(F.text == "🔥 Каллории")
async def purpose_calories_edit(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} Пробует изменить свою цель: 🔥 Каллории (handlers.purpose.purpose_calories_edit)"
    )
    await message.answer("Введите цель",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Wait.purpose_calories)


@router.message(Wait.purpose_calories)
async def purpose_calories_editing(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} Изменил свою цель: 🔥 Каллории (handlers.purpose.purpose_calories_editing) на: {message.text}"
    )
    purpose = "calories"
    res = await purpose_cred.edit_one_purpose(message, purpose)
    await message.answer("✅ Готово",
                         reply_markup=purpose_kb.kbzhu)
    await state.clear()


@router.message(F.text == "🥩 Белки")
async def purpose_protein_edit(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} Пробует изменить свою цель: 🥩 Белки (handlers.purpose.purpose_protein_edit)"
    )
    await message.answer("Введите цель",
                         reply_markup=purpose_kb.kbzhu)
    await state.set_state(Wait.purpose_protein)


@router.message(Wait.purpose_protein)
async def purpose_protein_editing(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} Изменил свою цель: 🥩 Белки (handlers.purpose.purpose_protein_editing) на: {message.text}"
    )
    purpose = "protein"
    res = await purpose_cred.edit_one_purpose(message, purpose)
    await message.answer("✅ Готово",
                         reply_markup=purpose_kb.kbzhu)
    await state.clear()


@router.message(F.text == "🧈 Жиры")
async def purpose_fat_edit(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} Пробует изменить свою цель: 🧈 Жиры (handlers.purpose.purpose_fat_edit)"
    )
    await message.answer("Введите цель",
                         reply_markup=purpose_kb.kbzhu)
    await state.set_state(Wait.purpose_fat)


@router.message(Wait.purpose_fat)
async def purpose_fat_editing(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} Изменил свою цель: 🧈 Жиры (handlers.purpose.purpose_fat_editing) на: {message.text}"
    )
    purpose = "fat"
    res = await purpose_cred.edit_one_purpose(message, purpose)
    await message.answer("✅ Готово",
                         reply_markup=purpose_kb.kbzhu)
    await state.clear()


@router.message(F.text == "🍞 Углеводы")
async def purpose_carbs_edit(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} Пробует изменить свою цель: 🍞 Углеводы (handlers.purpose.purpose_carbs_edit)"
    )
    await message.answer("Введите цель",
                         reply_markup=purpose_kb.kbzhu)
    await state.set_state(Wait.purpose_carbs)


@router.message(Wait.purpose_carbs)
async def purpose_carbs_editing(message: Message, state: FSMContext):
    logging.debug(
        f"{message.from_user.id} Изменил свою цель: 🍞 Углеводы (handlers.purpose.purpose_carbs_editing) на: {message.text}"
    )
    purpose = "carbs"
    res = await purpose_cred.edit_one_purpose(message, purpose)
    await message.answer("✅ Готово",
                         reply_markup=purpose_kb.kbzhu)
    await state.clear()


@router.message(F.text == "⏪ Назад")
async def back_to_menu(message: Message):
    logging.debug(
        f"{message.from_user.id} нажал на: ⏪ Назад (handlers.purpose.back_to_menu)"
    )
    await message.answer("Возвращаю вас в меню...",
                         reply_markup=kb.start_menu)
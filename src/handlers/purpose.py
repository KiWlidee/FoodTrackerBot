from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import cred.user_daily_tracking as tracking_cred
import cred.purpose_tracking as purpose_cred
import keyboards.start_menu as kb
from database import async_session
import keyboards.purpose as purpose_kb
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


@router.message(F.text == "❌ Не писать")
async def write_support(message: Message, state: FSMContext):
    await message.answer("Меню...",
                                reply_markup=kb.start_menu)
    await state.clear()


@router.message(F.text == "🎯 Цель")
async def purpose(message: Message):
    purpose = await purpose_cred.find_purpose(message)
    if isinstance(purpose, Purpose):
        await message.answer(f"""🎯 Ваши цели:
💧 Вода: {purpose.water_ml}
🔥 Каллории: {purpose.calories}
🥩 Белки: {purpose.protein}
🧈 Жиры: {purpose.fat}
🍞 Углеводы: {purpose.carbs}
    """,
                             reply_markup=kb.start_menu)
    else:
        await message.answer("❌ Цели не найдено. Попробуйте снова.",
                             reply_markup=kb.start_menu)


@router.message(F.text == "📊 Цели КБЖУ")
async def kbzhu_edit(message: Message):
    purpose = await purpose_cred.find_purpose(message)
    if isinstance(purpose, Purpose):
        await message.answer(f"""🎯 Ваши цели:
💧 Вода: {purpose.water_ml}
🔥 Каллории: {purpose.calories}
🥩 Белки: {purpose.protein}
🧈 Жиры: {purpose.fat}
🍞 Углеводы: {purpose.carbs}
        """,
                             reply_markup=purpose_kb.kbzhu_edit)
    else:
        await message.answer("❌ Цели не найдено. Попробуйте снова.",
                             reply_markup=kb.start_menu)


@router.message(F.text == "✏️ Изменить")
async def purpose_edit(message: Message):
    await message.answer("Что бы вы хотели изменить?",
                         reply_markup=purpose_kb.kbzhu)


@router.message(F.text == "💧 Воду")
async def purpose_water_edit(message: Message, state: FSMContext):
    await message.answer("Введите цель",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Wait.purpose_water)


@router.message(Wait.purpose_water)
async def purpose_water_editing(message: Message, state: FSMContext):
    purpose = "water"
    res = await purpose_cred.edit_one_purpose(message, purpose)
    await message.answer("✅ Готово",
                         reply_markup=purpose_kb.kbzhu)
    await state.clear()


@router.message(F.text == "🔥 Каллории")
async def purpose_calories_edit(message: Message, state: FSMContext):
    await message.answer("Введите цель",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Wait.purpose_calories)


@router.message(Wait.purpose_calories)
async def purpose_calories_editing(message: Message, state: FSMContext):
    purpose = "calories"
    res = await purpose_cred.edit_one_purpose(message, purpose)
    await message.answer("✅ Готово",
                         reply_markup=purpose_kb.kbzhu)
    await state.clear()


@router.message(F.text == "🥩 Белки")
async def purpose_protein_edit(message: Message, state: FSMContext):
    await message.answer("Введите цель",
                         reply_markup=purpose_kb.kbzhu)
    await state.set_state(Wait.purpose_protein)


@router.message(Wait.purpose_protein)
async def purpose_protein_editing(message: Message, state: FSMContext):
    purpose = "protein"
    res = await purpose_cred.edit_one_purpose(message, purpose)
    await message.answer("✅ Готово",
                         reply_markup=purpose_kb.kbzhu)
    await state.clear()


@router.message(F.text == "🧈 Жиры")
async def purpose_fat_edit(message: Message, state: FSMContext):
    await message.answer("Введите цель",
                         reply_markup=purpose_kb.kbzhu)
    await state.set_state(Wait.purpose_fat)


@router.message(Wait.purpose_fat)
async def purpose_fat_editing(message: Message, state: FSMContext):
    purpose = "fat"
    res = await purpose_cred.edit_one_purpose(message, purpose)
    await message.answer("✅ Готово",
                         reply_markup=purpose_kb.kbzhu)
    await state.clear()


@router.message(F.text == "🍞 Углеводы")
async def purpose_carbs_edit(message: Message, state: FSMContext):
    await message.answer("Введите цель",
                         reply_markup=purpose_kb.kbzhu)
    await state.set_state(Wait.purpose_carbs)


@router.message(Wait.purpose_carbs)
async def purpose_carbs_editing(message: Message, state: FSMContext):
    purpose = "carbs"
    res = await purpose_cred.edit_one_purpose(message, purpose)
    await message.answer("✅ Готово",
                         reply_markup=purpose_kb.kbzhu)
    await state.clear()


@router.message(F.text == "⏪ Назад")
async def back_to_menu(message: Message):
    await message.answer("Возвращаю вас в меню...",
                         reply_markup=kb.start_menu)
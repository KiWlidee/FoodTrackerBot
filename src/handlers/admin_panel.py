import logging
import os

from datetime import date, timedelta, datetime
from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.state import State, StatesGroup

import cred.user_daily_tracking as tracking_cred
import cred.photo_analysis as photo_analysis
import keyboards.start_menu as kb
import keyboards.admin as adm_kb
import config

from ai import ask_ai
from database import async_session


router = Router()

ADMIN_ID = int(config.ADMIN_TG_ID)


@router.message(F.text == "👑 Админ")
async def today_stats(message: Message):
    if ADMIN_ID == message.from_user.id:
        await message.answer("😎 Сигма",
                             reply_markup=adm_kb.admin_menu)


@router.message(F.text == "📄 Логи + ДБ")
async def unload_db_logs(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет прав для этой команды")
        return

    try:
        if not os.path.exists("data.db"):
            await message.answer("❌ Файл базы данных не найден")
            return

        with open("data.db", "rb") as f:
            db_data = f.read()

        await message.answer_document(
            BufferedInputFile(db_data, filename="data_backup.db"),
            caption="📦 Backup базы данных"
        )
        await message.answer("✅ База данных успешно экспортирована!")

        if not os.path.exists("debug.log"):
            await message.answer("❌ Файл логов данных не найден")
            return

        with open("debug.log", "rb") as f:
            logs_data = f.read()

        await message.answer_document(
            BufferedInputFile(logs_data, filename="debug_log_backup.log"),
            caption="📦 Backup базы данных"
        )
        await message.answer("✅ Логи успешно экспортированы!")

    except Exception as e:
        await message.answer(f"❌ Ошибка при создании бэкапа: {e}")


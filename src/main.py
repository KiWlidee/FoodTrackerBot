import asyncio
import logging
from sys import stdout

from aiogram import Bot, Dispatcher

import config
from database import init_db
from __init__ import main_router


def setup_logging():
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    file_handler = logging.FileHandler("debug.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    console_handler = logging.StreamHandler(stdout)
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    aiogram_logger = logging.getLogger("aiogram")
    aiogram_logger.propagate = False
    aiogram_logger.setLevel(logging.INFO)

    aiogram_console = logging.StreamHandler(stdout)
    aiogram_console.setFormatter(formatter)
    aiogram_logger.addHandler(aiogram_console)


async def main():
    setup_logging()
    await init_db()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
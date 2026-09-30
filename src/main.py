import asyncio
import logging
from sys import stdout

from aiogram import Bot, Dispatcher

import config

from database import init_db
from __init__ import main_router


async def main():
    await init_db()
    logging.basicConfig(level=logging.INFO, encoding="utf-8",
                        handlers=[logging.FileHandler("debug.log", encoding="utf-8"),
                                  logging.StreamHandler(stdout)])
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")


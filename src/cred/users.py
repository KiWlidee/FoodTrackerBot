import logging

from aiogram.types import Message

from sqlalchemy import select

from database import async_session
from models.users import UsersOrm


async def find_user_by_tg_id(message: Message):
    async with async_session() as session:
        tg_id = message.from_user.id
        user = select(UsersOrm).where(UsersOrm.tg_id == tg_id)
        res = await session.execute(user)
        user = res.scalar_one_or_none()
        if user:
            logging.debug(f"find_user_by_tg_id - найден пользователь: {user.tg_id}")
        return user


async def add_new_user(message: Message):
    async with async_session() as session:
        username = f"@{message.from_user.username}" if message.from_user.username else None
        user = UsersOrm(tg_id=message.from_user.id, username=f"{username}")
        session.add(user)
        await session.commit()
        logging.info(f"Добавлен новый пользователь: {username}, ID: {message.from_user.id}")
        return {"status": "OK"}


async def all_users() -> list[dict]:
    async with async_session() as session:
        users = (await session.execute(select(UsersOrm))).scalars().all()
        return [
            {"id": u.id, "tg_id": u.tg_id, "username": u.username or "без username"}
            for u in users
        ]


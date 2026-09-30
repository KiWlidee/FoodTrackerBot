import logging

import datetime
from datetime import date

from aiogram.types import Message

from sqlalchemy import select

from database import async_session
from models.users import UsersOrm
from models.user_daily_tracking import Tracking


async def add_water(message: Message):
    async with async_session() as session:
        try:
            amount = int(message.text)
        except (TypeError, ValueError):
            return False

        today = datetime.datetime.now(datetime.timezone.utc).date()
        tg_id = message.from_user.id

        stmt = select(Tracking).filter_by(tg_id=tg_id, day=today)
        res = await session.execute(stmt)
        user = res.scalar_one_or_none()

        if user:
            user.water_ml += amount
        else:
            tracking = Tracking(tg_id=tg_id, day=today, water_ml=amount)
            session.add(tracking)
        await session.commit()

    return {"status": "OK"}


async def kbzhu_stats(message: Message, day: date):
    async with async_session() as session:
        stmt = select(Tracking).filter_by(tg_id=message.from_user.id, day=day)
        res = await session.execute(stmt)
        result = res.scalars().all()
        if result:
            return result[0]
        kbzhu = Tracking(tg_id=message.from_user.id, day=day, water_ml=0)
        session.add(kbzhu)
        await session.commit()
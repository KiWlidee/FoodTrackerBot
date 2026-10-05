import logging

import datetime
from datetime import date

from aiogram.types import Message

from sqlalchemy import select

from database import async_session
from models.user_daily_tracking import Tracking


async def make_new_stat(
        message: Message,
        water_ml: float= 0,
        calories: float= 0,
        protein: float= 0,
        fat: float= 0,
        carbs: float= 0,
):
    async with async_session() as session:
        try:
            stmt = Tracking(
                tg_id=message.from_user.id,
                water_ml=water_ml,
                calories=calories,
                protein=protein,
                fat=fat,
                carbs=carbs
            )
            session.add(stmt)
            await session.commit()
            logging.debug(
                f"{message.from_user.id} создал новую таблицу целей (cred.user_daily_traking.make_new_stat)")
            return {"status": "OK"}
        except Exception as e:
            logging.error(f"{e} (cred.user_daily_traking.make_new_stat)")
            return {"status": "ERROR"}


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
        try:
            stmt = select(Tracking).filter_by(tg_id=message.from_user.id, day=day)
            res = await session.execute(stmt)
            result = res.scalars().all()
            if result:
                logging.debug(
                    f"{message.from_user.id} найдена статистика по КБЖУ {result[0]} (cred.user_daily_traking.kbzhu_stats)"
                )
                return result[0]
            kbzhu = Tracking(tg_id=message.from_user.id, day=day, water_ml=0)
            session.add(kbzhu)
            await session.commit()
            logging.debug(
                f"{message.from_user.id} создана новая статистика по КБЖУ (cred.user_daily_traking.kbzhu_stats)"
            )
        except Exception as e:
            logging.error(f"{e} (cred.user_daily_traking.kbzhu_stats)")
            return {"status": "ERROR"}


async def kbzhu_one_edit(message: Message, stat: Tracking, day: date):
    user_stat = message.text
    if user_stat.isdigit() or user_stat[0] == "-" and user_stat[1:].isdigit():
        user_stat = float(user_stat)
        async with async_session() as session:
            try:
                stmt = select(Tracking).filter_by(tg_id=message.from_user.id, day=day)
                res = await session.execute(stmt)
                result = res.scalar_one_or_none()
                if result:
                    if stat == "water":
                        result.water_ml += user_stat
                    elif stat == "calories":
                        result.calories += user_stat
                    elif stat == "protein":
                        result.protein += user_stat
                    elif stat == "fat":
                        result.fat += user_stat
                    elif stat == "carbs":
                        result.carbs += user_stat
                    await session.commit()
                    logging.debug(
                        f"{message.from_user.id} добавил {user_stat} в {stat} (cred.user_daily_traking.kbzhu_one_edit)"
                                  )
                    return {"status": "OK"}
                else:
                    new_stat = await make_new_stat(
                        message,
                        water_ml=0,
                        calories=0,
                        protein=0,
                        fat=0,
                        carbs=0
                    )
                    logging.debug(
                        f"{message.from_user.id} создал новую таблицу целей (cred.user_daily_traking.kbzhu_one_edit)")
                    return {"status": "New Purpose"}
            except Exception as e:
                logging.error(f"{e} (cred.user_daily_traking.kbzhu_one_edit)")
                return {"status": "ERROR"}
    return {"status": "Не соответствие стандарту"}
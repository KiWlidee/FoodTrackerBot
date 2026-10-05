import logging

from aiogram.types import Message

from sqlalchemy import select

from database import async_session
from models.user_daily_tracking import Tracking
from models.purpose_tracking import Purpose


async def make_purpose(
        message: Message,
        water_ml: float= 0,
        calories: float= 0,
        protein: float= 0,
        fat: float= 0,
        carbs: float= 0,
):
    async with async_session() as session:
        try:
            stmt = Purpose(
                tg_id=message.from_user.id,
                water_ml=water_ml,
                calories=calories,
                protein=protein,
                fat=fat,
                carbs=carbs
            )
            session.add(stmt)
            await session.commit()
            logging.debug(f"{message.from_user.id} новая таблица цели (cred.purpose_traking.make_purpose)")
            return {"status": "OK"}
        except Exception as e:
            logging.error(f"{e} (cred.purpose_traking.make_purpose)")
            return {"status": "ERROR"}


async def find_purpose(message: Message):
    async with async_session() as session:
        try:
            stmt = select(Purpose).filter_by(tg_id=message.from_user.id)
            res = await session.execute(stmt)
            result = res.scalar_one_or_none()
            if result:
                logging.debug(f"{message.from_user.id} найдена цель {result} (cred.purpose_traking.find_purpose)")
                return result
            else:
                new_purpose = await make_purpose(message)
                logging.debug(f"{message.from_user.id} цель не найдена (cred.purpose_traking.find_purpose)")
                return {"status": "Not Found"}
        except Exception as e:
            logging.error(f"{e} (cred.purpose_traking.make_purpose)")
            return {"status": "ERROR"}


async def edit_one_purpose(message: Message, purpose: Purpose):
    user_purpose = message.text
    if user_purpose.isdigit():
        async with async_session() as session:
            try:
                stmt = select(Purpose).filter_by(tg_id=message.from_user.id)
                res = await session.execute(stmt)
                result = res.scalar_one_or_none()
                if result:
                    if purpose == "water":
                        result.water_ml = user_purpose
                    elif purpose == "calories":
                        result.calories = user_purpose
                    elif purpose == "protein":
                        result.protein = user_purpose
                    elif purpose == "fat":
                        result.fat = user_purpose
                    elif purpose == "carbs":
                        result.carbs = user_purpose
                    await session.commit()
                    logging.debug(f"{message.from_user.id} изменил свою цель ({user_purpose}) (cred.purpose_traking.edit_one_purpose)")
                    return {"status": "OK"}
                else:
                    new_purpose = await make_purpose(
                        message,
                        water_ml=0,
                        calories=0,
                        protein=0,
                        fat=0,
                        carbs=0
                    )
                    logging.debug(f"{message.from_user.id} создал новую таблицу целей (cred.purpose_traking.edit_one_purpose)")
                    return {"status": "New Purpose"}
            except Exception as e:
                logging.error(f"{e} (cred.purpose_traking.edit_one_purpose)")
                return {"status": "ERROR"}
    return {"status": "Не соответствие стандарту"}

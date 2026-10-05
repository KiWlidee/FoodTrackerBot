import base64
import logging

from aiogram.types import Message

from ai import ask_ai_vision


async def analys_photo(message: Message):
    try:
        photo = message.photo[-1]

        file = await message.bot.get_file(photo.file_id)
        file_bytes = await message.bot.download_file(file.file_path)
        image_bytes = file_bytes.read()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        answer = await ask_ai_vision(base64_image, "Посчитай КБЖУ этого блюда")

        return answer
    except Exception as e:
        logging.error(
            f"{e}, {message.from_user.id} не удалось обработать фото. (cred.photo_analysis.analys_photo)"
        )
        return "Не удалось обработать фото. Попробуйте ещё раз."
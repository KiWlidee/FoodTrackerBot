import logging

import httpx
from openai import AsyncOpenAI

import config
import promts


ai_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=config.API_KEY,
    http_client=httpx.AsyncClient(
        proxy=None,
        trust_env=False,
    ),
)


async def ask_ai(user_text: str) -> str:
    try:
        response = await ai_client.chat.completions.create(
            model="google/gemini-2.5-flash",
            messages=[
                {"role": "system", "content": promts.SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            temperature=0.3,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.exception("Ошибка при запросе к OpenRouter")
        return "Извините, не смог обработать запрос. Попробуйте позже."


async def ask_ai_vision(base64_image: str, user_text: str) -> str:
    try:
        response = await ai_client.chat.completions.create(
            model="google/gemini-2.5-flash",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{promts.SYSTEM_PROMPT_VISION}\n\n{user_text}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1024,
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        import logging
        logging.exception("Ошибка при анализе фото")
        return "Не удалось проанализировать фото."
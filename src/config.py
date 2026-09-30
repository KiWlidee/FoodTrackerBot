import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str | None = os.getenv("BOT_TOKEN")
API_KEY: str | None = os.getenv("API_KEY")
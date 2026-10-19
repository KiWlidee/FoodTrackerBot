import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str | None = os.getenv("BOT_TOKEN")
API_KEY: str | None = os.getenv("API_KEY")
ADMIN_TG_ID: str | None = os.getenv("ADMIN_TG_ID")
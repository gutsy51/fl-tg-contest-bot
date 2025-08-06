import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from src.bot_commands import router as main_router


# Logging and environment variables.
load_dotenv('config/.env')
logging.basicConfig(
    filename=getenv('LOGS_PATH'),
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Bot object.
bot = Bot(token=getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()
dp.include_router(main_router)


async def main():
    """Start the bot."""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
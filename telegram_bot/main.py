import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram_dialog import DialogManager
from telegram_bot.dialogs import main_menu_dialog, add_task_dialog, start_handler
from aiogram import types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

dp.message.register(start_handler, Command(commands=["start", "help"]))
dp.include_router(main_menu_dialog)
dp.include_router(add_task_dialog)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
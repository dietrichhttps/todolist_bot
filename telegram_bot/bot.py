import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import StartMode

API_URL = os.environ.get('API_URL', 'http://web:8000/api')

async def send_telegram_notification(chat_id, message):
    bot = Bot(token=os.environ.get('TELEGRAM_BOT_TOKEN', 'your-bot-token'))
    try:
        await bot.send_message(chat_id, message)
    except Exception as e:
        print(f"Error sending notification: {e}")
    finally:
        await bot.session.close()
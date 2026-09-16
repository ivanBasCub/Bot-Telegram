from core.constants.env import TG_BOT_CLIENT_CHAT_ID, TG_BOT_TOKEN
from telegram import Bot
import os

async def notify_client(message: str):
    bot = Bot(token=TG_BOT_TOKEN)
    async with bot:
        await bot.send_message(chat_id=TG_BOT_CLIENT_CHAT_ID, text=message)
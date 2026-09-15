from core.constants.env import TG_API_ID, TG_API_HASH, TG_SESSION_NAME, TG_PHONE
from core.constants.paths import BD_FILE_PATH
from telethon import TelegramClient, events
import json
import os

client = TelegramClient(TG_SESSION_NAME, TG_API_ID, TG_API_HASH)


def _load_channels() -> list[int | str]:
    config_path = BD_FILE_PATH

    if not os.path.exists(config_path):
        return []

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    return config.get("channels", [])


async def connect_client():
    if not client.is_connected():
        await client.start(phone= TG_PHONE)

async def disconnect_client():
    if client.is_connected():
        await client.disconnect()

async def start_listener():
    channels = _load_channels()

    @client.on(events.NewMessage(chats=channels))
    async def handler(event):
        text = event.message.message
        canal_id = event.chat_id

        print(f"[{canal_id}] {text}")

    await client.run_until_disconnected()
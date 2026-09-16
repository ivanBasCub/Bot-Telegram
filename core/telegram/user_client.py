from core.constants.env import TG_API_ID, TG_API_HASH, TG_SESSION_NAME, TG_PHONE
from core.constants.paths import BD_FILE_PATH

from middleware.telegram.messages import check_msg_job_application

from ui.dialogs.login import ask_code, ask_password

from telethon import TelegramClient, events
import asyncio
import json
import os

client = TelegramClient(
    TG_SESSION_NAME,
    TG_API_ID,
    TG_API_HASH
)

_listener_task: asyncio.Task | None = None
_handler = None


def _make_handler():
    async def handler(event):
        await check_msg_job_application(event.message)

    return handler


def _load_channels() -> list[int | str]:
    config_path = BD_FILE_PATH

    if not os.path.exists(config_path):
        return []

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    return config.get("channels", [])


async def connect_client(parent=None):
    if not client.is_connected():
        await client.start(
            phone=TG_PHONE,
            code_callback=lambda: ask_code(parent),
            password=lambda: ask_password(parent)
        )


async def disconnect_client():
    if client.is_connected():
        await client.disconnect()


async def start_listener():
    global _handler
    channels = _load_channels()
    _handler = _make_handler()

    client.add_event_handler( _handler, events.NewMessage(chats=channels))

    try:
        await client.run_until_disconnected()

    finally:
        # Asegurarnos de quitar el handler cuando termine
        if _handler is not None:
            client.remove_event_handler(_handler)
            _handler = None


def start_listener_task() -> asyncio.Task | None:
    global _listener_task

    if _listener_task is not None and not _listener_task.done():
        return _listener_task

    _listener_task = asyncio.create_task(
        start_listener()
    )

    return _listener_task

async def stop_listener():
    global _handler, _listener_task

    if _handler is not None:
        client.remove_event_handler(_handler)
        _handler = None

    if client.is_connected():
        await client.disconnect()

    if _listener_task is not None:
        try:
            await _listener_task
        except Exception:
            pass
        _listener_task = None

def is_listener_running() -> bool:
    return (
        _listener_task is not None
        and not _listener_task.done()
    )


async def restart_listener():
    if is_listener_running():
        await stop_listener()

    await connect_client()
    start_listener_task()
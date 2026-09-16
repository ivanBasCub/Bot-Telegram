from telethon.errors import ChannelPrivateError, UsernameNotOccupiedError, UsernameInvalidError
from core.config_bd import load_bd, save_bd
from telethon import TelegramClient

async def channel_exists(client: TelegramClient, channel) -> bool:
    try:
        await client.get_entity(channel)
        return True
    except (ChannelPrivateError, UsernameNotOccupiedError, UsernameInvalidError, ValueError):
        return False


async def _validate_channels(client: TelegramClient, channels: list) -> dict:
    valid = []
    invalids = []

    for channel in channels:
        if await channel_exists(client, channel):
            valid.append(channel)
        else:
            invalids.append(channel)

    return {
        "valid": valid,
        "invalids": invalids
    }


async def save_valid_channels(client: TelegramClient, channels: list) -> dict:
    result = await _validate_channels(client, channels)
    bd = load_bd()
    bd["channels"] = result["valid"]
    save_bd(bd)
    return result
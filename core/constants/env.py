from dotenv import load_dotenv
import sys
import os

load_dotenv(".env")

def _require_str(key: str, min_length: int = 1) -> str:
    value = os.getenv(key)

    if not value or len(value.strip()) < min_length:
        print(f"[FATAL] Variable de entorno '{key}' no definida o demasiado corta (minimo {min_length} caracteres)")
        sys.exit(1)

    return value.strip()

def _require_int(key: str, default: int | None = None) -> int:
    value = os.getenv(key)

    if value is None and default is not None:
        return default

    try:
        return int(value)
    except (TypeError, ValueError):
        print(f"[FATAL] Variable de entorno '{key}' debe ser un número entero válido, valor recibido: {value}")
        sys.exit(1)

#   TELEGRAM USER
TG_API_ID =         _require_int("TG_API_ID")
TG_API_HASH =       _require_str("TG_API_HASH")
TG_PHONE=           _require_str("TG_PHONE")
TG_SESSION_NAME=    _require_str("TG_SESSION_NAME")

#   TELEGRAM BOT
TG_BOT_TOKEN=           _require_str("TG_BOT_TOKEN")
TG_BOT_CLIENT_CHAT_ID=  _require_int("TG_BOT_CLIENT_CHAT_ID")

#   EMAIL
SMTP_HOST=      _require_str("SMTP_HOST")
SMTP_PORT=      _require_int("SMTP_PORT", 587)
SMTP_USER=      _require_str("SMTP_USER")
SMTP_PASSWORD=  _require_str("SMTP_PASSWORD")
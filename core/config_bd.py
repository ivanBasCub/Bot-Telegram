from core.constants.paths import BD_FILE_PATH
import json
import os


def load_bd() -> dict:
    if not os.path.exists(BD_FILE_PATH) or os.path.getsize(BD_FILE_PATH) == 0:
        return {}

    with open(BD_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_bd(bd: dict) -> None:
    os.makedirs(os.path.dirname(BD_FILE_PATH), exist_ok=True)

    with open(BD_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(bd, f, indent=2, ensure_ascii=False)

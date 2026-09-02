import os
from dataclasses import dataclass

import dotenv

dotenv.load_dotenv()


@dataclass(frozen=True)
class Settings:
    vk_wall_token: str
    vk_messages_token: str
    db_path: str


def load_settings() -> Settings:
    wall_token = os.getenv("VK_TOKEN")
    messages_token = os.getenv("VK_MESSAGES_TOKEN")
    db_path = os.getenv("DB_PATH", "database.db")

    missing = [
        name for name, value in [
            ("VK_TOKEN", wall_token),
            ("VK_MESSAGES_TOKEN", messages_token),
        ] if not value
    ]
    if missing:
        raise RuntimeError(f"Не заданы обязательные переменные окружения: {', '.join(missing)}")

    return Settings(vk_wall_token=wall_token, vk_messages_token=messages_token, db_path=db_path)


settings = load_settings()
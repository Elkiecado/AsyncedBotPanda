import aiosqlite

from config import settings

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    vk_id TEXT PRIMARY KEY,
    username TEXT,
    chat_id INTEGER NOT NULL
)
"""


async def init_db():
    async with aiosqlite.connect(settings.db_path) as db:
        await db.execute(CREATE_USERS_TABLE)
        await db.commit()


async def user_exists(vk_id: str) -> bool:
    async with aiosqlite.connect(settings.db_path) as db:
        cursor = await db.execute("SELECT 1 FROM users WHERE vk_id = ?", (vk_id,))
        return await cursor.fetchone() is not None


async def add_user(vk_id: str, username: str, chat_id: int) -> bool:
    if await user_exists(vk_id):
        return False
    async with aiosqlite.connect(settings.db_path) as db:
        await db.execute(
            "INSERT INTO users (vk_id, username, chat_id) VALUES (?, ?, ?)",
            (vk_id, username, chat_id),
        )
        await db.commit()
    return True


async def update_username(vk_id: str, username: str):
    async with aiosqlite.connect(settings.db_path) as db:
        await db.execute("UPDATE users SET username = ? WHERE vk_id = ?", (username, vk_id))
        await db.commit()


async def get_user_by_mention(mention: str) -> dict | None:
    async with aiosqlite.connect(settings.db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM users WHERE vk_id = ? OR username = ?", (mention, mention)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None


async def get_all_users() -> list[dict]:
    async with aiosqlite.connect(settings.db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM users")
        return [dict(r) for r in await cursor.fetchall()]
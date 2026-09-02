import asyncio
import logging

from common.logging import setup_logging
from common.database import init_db
from services.wall_listener.bot import wall_bot
from services.message_sender.bot import message_bot

logger = logging.getLogger(__name__)


async def run_safely(run_coro_factory, name: str):
    """Перезапускает бота, если он упал, вместо того чтобы утаскивать за собой второго."""
    while True:
        try:
            await run_coro_factory()
        except Exception:
            logger.exception("%s упал, перезапуск через 5 секунд", name)
            await asyncio.sleep(5)


async def main():
    setup_logging(level="DEBUG")
    await init_db()

    logger.info("Запуск ботов...")
    await asyncio.gather(
        run_safely(wall_bot.run_polling, "wall_bot"),
        run_safely(message_bot.run_polling, "message_bot"),
    )


if __name__ == "__main__":
    asyncio.run(main())
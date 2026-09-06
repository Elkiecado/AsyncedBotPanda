import asyncio
import logging
import signal


from common.logging import setup_logging
from common.database import init_db
from services.wall_listener.bot import wall_bot
from services.message_sender.bot import message_bot

logger = logging.getLogger(__name__)

HEARTBEAT_PATH = "/app/data/heartbeat"


async def run_safely(run_coro_factory, name: str):
    """Перезапускает бота, если он упал, вместо того чтобы утаскивать за собой второго."""
    while True:
        try:
            await run_coro_factory()
        except Exception:
            logger.exception("%s упал, перезапуск через 5 секунд", name)
            await asyncio.sleep(5)

async def heartbeat_task():
    while True:
        with open(HEARTBEAT_PATH, "w") as f:
            f.write("ok")
        await asyncio.sleep(20)


async def main():
    setup_logging()
    await init_db()

    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def handle_sigterm():
        logger.info("Получен сигнал остановки, завершаю работу...")
        stop_event.set()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, handle_sigterm)

    logger.info("Запуск ботов...")
    tasks = [
        asyncio.create_task(run_safely(wall_bot.run_polling, "wall_bot")),
        asyncio.create_task(run_safely(message_bot.run_polling, "message_bot")),
        asyncio.create_task(heartbeat_task()),
    ]

    await stop_event.wait()

    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    logger.info("Все задачи остановлены")


if __name__ == "__main__":
    asyncio.run(main())
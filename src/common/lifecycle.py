import logging

logger = logging.getLogger(__name__)


def make_readiness_hook(bot_name: str):
    async def readiness():
        logger.info("%s запущен и готов принимать события", bot_name)
    return readiness


def make_shutdown_hook(bot_name: str):
    async def shutdown():
        logger.info("%s остановлен", bot_name)
    return shutdown
import logging

from vkbottle import Bot, GroupEventType, GroupTypes

from config import settings
from domain.post_parser import extract_info
from domain.schemas import MessageInfo
from services.message_sender.service import process_notification

logger = logging.getLogger(__name__)

wall_bot = Bot(settings.vk_wall_token)


@wall_bot.on.raw_event(GroupEventType.WALL_POST_NEW, dataclass=GroupTypes.WallPostNew)
async def handler(event: GroupTypes.WallPostNew):
    data = MessageInfo(**extract_info(event))

    try:
        report = await process_notification(data)
    except Exception:
        logger.exception("Ошибка при обработке поста %s", data.post_link)
        return

    logger.info("Пост %s обработан: %s", data.post_link, report)
import logging
import random

from domain.templates import TEMPLATES
from domain.schemas import MessageInfo
from common.database import get_user_by_mention
from services.message_sender.bot import message_bot

logger = logging.getLogger(__name__)


async def send_message(chat_id: int, text: str) -> None:
    await message_bot.api.messages.send(
        peer_id=chat_id,
        message=text,
        random_id=random.randint(1, 2**31 - 1),
    )


async def process_notification(data: MessageInfo) -> dict:
    if not data.mentions:
        logger.info("В посте %s нет упоминаний", data.post_link)
        return {"sent_to": [], "not_found": [], "reason": "no_mentions"}

    template = TEMPLATES.get(data.post_type)
    if template is None:
        logger.warning("Неизвестный тип поста %r для %s", data.post_type, data.post_link)
        return {"sent_to": [], "not_found": list(data.mentions.keys()), "reason": "unknown_post_type"}

    sent_to, not_found = [], []
    for mention, lines in data.mentions.items():
        user = await get_user_by_mention(mention)
        if user is None:
            not_found.append(mention)
            continue

        text = template.format(
            post_url=str(data.post_link),
            payment_info_line=data.payment_info_line or "",
            datetime_deadline=data.deadline,
            user_line="\n".join(lines),
        )
        await send_message(user["chat_id"], text)
        sent_to.append(mention)

    if not_found:
        logger.warning("Не найдены в базе (пост %s): %s", data.post_link, not_found)

    return {"sent_to": sent_to, "not_found": not_found}
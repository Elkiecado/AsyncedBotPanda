import logging

from vkbottle import Bot, GroupEventType, GroupTypes

from config import settings
from common.database import user_exists, add_user

logger = logging.getLogger(__name__)

message_bot = Bot(settings.vk_messages_token)


@message_bot.on.raw_event(GroupEventType.MESSAGE_NEW, dataclass=GroupTypes.MessageNew)
async def on_new_message(event: GroupTypes.MessageNew):
    from_id = event.object.message.from_id
    vk_id = f"id{from_id}"

    if await user_exists(vk_id):
        return

    users_info = await message_bot.api.users.get(user_ids=[from_id], fields=["screen_name"])
    screen_name = users_info[0].screen_name if users_info else None
    username = screen_name or vk_id

    await add_user(vk_id=vk_id, username=username, chat_id=from_id)
    logger.info("Зарегистрирован новый пользователь: %s (%s)", username, from_id)
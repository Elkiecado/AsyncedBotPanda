import os
import dotenv
import asyncio
from utils.processing import extract_info
from vkbottle import Bot, GroupEventType, GroupTypes

dotenv.load_dotenv()
TOKEN = os.getenv("VK_TOKEN")
api = Bot(TOKEN)

@api.on.raw_event(GroupEventType.WALL_POST_NEW, dataclass=GroupTypes.WallPostNew)
async def handler(event:GroupTypes.WallPostNew):
    json = extract_info(event)
api.run_forever()


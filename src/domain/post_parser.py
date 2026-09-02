import re
import logging
from collections import defaultdict

from vkbottle import GroupTypes

from domain.post_classifier import extract_post_type
logger = logging.getLogger(__name__)

def extract_info(event: GroupTypes.WallPostNew) -> dict:
    text = event.object.text
    logger.debug("RAW TEXT: %r", text)  # временно, для проверки формата
    post_type, payment_info_line = extract_post_type(text)
    return {
        "post_link": post_link_make(event),
        "post_type": post_type,
        "payment_info_line": payment_info_line,
        "mentions": extract_vk_mentions(text),
        "deadline": extract_combined_datetime(text),
    }


def post_link_make(event: GroupTypes.WallPostNew) -> str:
    return f"https://vk.com/wall{event.object.from_id}_{event.object.id}"


def extract_combined_datetime(text: str) -> str:
    pattern = r"\b(?P<day>\d{2})\.(?P<month>\d{2})\b(?:\s+(?P<time>\d{2}:\d{2}))?"
    match = re.search(pattern, text)
    if match:
        day, month, time_str = match.group("day"), match.group("month"), match.group("time")
        return f"{day}.{month} {time_str}" if time_str else f"{day}.{month}"
    return "[Срок не указан]"


def extract_vk_mentions(text: str) -> dict[str, list[str]]:
    mentions = defaultdict(list)
    vk_mention_pattern = r"\[(id\d+|club\d+|[a-zA-Z0-9_.]+)\|[^\]]+\]"
    vk_mentions = set(re.findall(vk_mention_pattern, text))

    for username in vk_mentions:
        for line in text.split("\n"):
            if username in line:
                mentions[username].append(line)
    return dict(mentions)
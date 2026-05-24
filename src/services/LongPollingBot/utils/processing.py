import re

from vkbottle import GroupTypes
from collections import defaultdict

def extract_info(event: GroupTypes.WallPostNew):
    text = event.object.text
    data = {
        "postlink": post_link_make(event),
        "posttype": extract_post_type(text),
        "mentions": extract_vk_mentions(text),
        "deadline": extract_combined_datetime(text)
    }
    return data
    
"""
1. Ссылка на пост
2. Информация о типе поста(ег. пришедшее, оплата)
3. Упоминания в самом посте + строка
4. дедлайн
"""

def extract_post_type(text: str):
    """Отдаёт типа поста + 1 первую строку"""
    text_lower = text.lower()
    pass

def post_link_make(event: dict):
    """Создаёт ссылку на пост"""
    return f"https://vk.com/wall{event.object.from_id}_{event.object.id}"

def extract_combined_datetime(text: str) -> str:
    """Ищет временные рамки для дедлайна"""
    pattern = r"\b(?P<day>\d{2})\.(?P<month>\d{2})\b(?:\s+(?P<time>\d{2}:\d{2}))?"
    match = re.search(pattern, text)
    if match:
        day, month, time_str = match.group("day"), match.group("month"), match.group("time")
        return f"{day}.{month} {time_str}" if time_str else f"{day}.{month}"
    return "[Срок не указан]"

def extract_vk_mentions(text: str) -> list:
    """Ищет все отметки пользователя внутри поста"""
    mentions = defaultdict(list)
    vk_mention_pattern = r"\[(id\d+|club\d+|[a-zA-Z0-9_.]+)\|[^\]]+\]"
    vk_mentions = set(re.findall(vk_mention_pattern, text))

    for username in vk_mentions:
        for line in text.split("\n"):
            if username in line:
                mentions[username].append(line)
    return mentions
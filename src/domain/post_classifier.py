import re
import logging

logger = logging.getLogger(__name__)


def extract_post_type(text: str) -> tuple[str | None, str]:
    """Отдаёт тип поста + первую строку текста."""
    first_line = text.split("\n")[0].strip()
    first_line_lower = first_line.lower()

    hashtags = re.findall(r"#([a-zа-яё_0-9]+)", first_line_lower)

    if any("пришед" in tag for tag in hashtags):
        return "arrived", first_line

    if any("коробк" in tag for tag in hashtags):
        return "box_payment", first_line

    if "оплата" in first_line_lower and "разбор" in first_line_lower:
        return "regular_payment", first_line

    logger.warning("Не удалось определить тип поста по первой строке: %r", first_line)
    return None, first_line
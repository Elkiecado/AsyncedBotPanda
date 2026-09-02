from pydantic import BaseModel, HttpUrl


class MessageInfo(BaseModel):
    post_link: HttpUrl
    post_type: str | None = None
    payment_info_line: str | None = None
    mentions: dict[str, list[str]] | None = None
    deadline: str
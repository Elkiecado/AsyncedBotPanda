TEMPLATE_REGULAR_PAYMENT = (
    "Вас упомянули в посте с оплатой разбора:\n"
    "{post_url}\n\n"
    "{payment_info_line}\n\n"
    "⤷ Дедлайн : {datetime_deadline} по МСК\n\n"
    "{user_line}"
)

TEMPLATE_BOX_PAYMENT = (
    "Вас упомянули в посте с оплатой коробки:\n"
    "{post_url}\n\n"
    "{payment_info_line}\n\n"
    "⤷ Дедлайн : {datetime_deadline} по МСК\n\n"
    "{user_line}"
)

TEMPLATE_ARRIVED = (
    "Вас упомянули в посте с пришедшим стаффом:\n"
    "{post_url}\n\n"
    "{payment_info_line}\n\n"
    "{user_line}"
)

TEMPLATES = {
    "regular_payment": TEMPLATE_REGULAR_PAYMENT,
    "box_payment": TEMPLATE_BOX_PAYMENT,
    "arrived": TEMPLATE_ARRIVED,
}
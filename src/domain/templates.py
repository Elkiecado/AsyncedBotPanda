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

WELCOME_MESSAGE = (
    "ᯓ★ вы успешно подписались на бот для получения уведомлений об отметках в 'яблочной панде'🍎\n\n"
    "здесь вам будут приходить уведомления о новых постах с оплатой разборов и коробок, чтобы ничего не пропустить!\n\n"
    "пожалуйста, обратите внимание, что иногда возможны небольшие задержки в отправке сообщений\n\n"
    "желаем вам хорошего времяпрепровождения в нашем уголке и приятных покупок! 𐔌՞ .ˬ.ܸ՞𐦯 💓"
)
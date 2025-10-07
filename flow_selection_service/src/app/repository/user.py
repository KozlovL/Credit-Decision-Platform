from app.constants import (
    PIONEER_FLOW_TYPE,
    REPEATER_FLOW_TYPE,
)

# База данных номеров
USERS_PHONES = [
    '71111111111',
    '72222222222',
    '73333333333',
    '74444444444',
    '75555555555',
    '76666666666',
    '77777777777',
    '78888888888',
    '79999999999',
]


def add_user(phone: str) -> None:
    """Функция добавления пользователя в базу данных."""
    USERS_PHONES.append(phone)


# база данных типов флоу
FLOW_TYPES = (PIONEER_FLOW_TYPE, REPEATER_FLOW_TYPE)

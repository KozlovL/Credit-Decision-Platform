from common.repository.user import get_users


def is_repeater(phone: str) -> bool:
    """Функция, возвращающая True, если пользователь повторник."""
    return any(user.phone == phone for user in get_users())

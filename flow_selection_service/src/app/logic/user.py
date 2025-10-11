from common.repository.user import get_users


def is_repeater(phone: str) -> bool:
    """Функция, возвращающая True, если пользователь повторник."""
    for user in get_users():
        if user.phone == phone:
            return True
    return False

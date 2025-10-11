from app.constants import (
    MICROLOAN_STR, QUICK_MONEY_STR, CONSUMER_LOAN_STR,
    LOYALTY_LOAN_STR, PRIME_CREDIT_STR, ADVANTAGE_PLUS_STR,
)

# Словари с названиями продуктов и соответствующими им оценками
PIONEER_PRODUCTS_WITH_SCORE = {
    MICROLOAN_STR: 5,
    QUICK_MONEY_STR: 7,
    CONSUMER_LOAN_STR: 9
}

REPEATER_PRODUCTS_WITH_SCORE = {
    LOYALTY_LOAN_STR: 6,
    ADVANTAGE_PLUS_STR: 8,
    PRIME_CREDIT_STR: 10
}


def get_available_pioneer_product_names() -> list[str]:
    """Получение всех доступных первичнику продуктов."""
    return list(PIONEER_PRODUCTS_WITH_SCORE.keys())


def get_available_repeater_product_names() -> list[str]:
    """Получение всех доступных повторнику продуктов."""
    return list(REPEATER_PRODUCTS_WITH_SCORE.keys())


def get_available_pioneer_products_with_score() -> dict[str, int]:
    """Получение всех доступных первичнику продуктов с оценкой."""
    return PIONEER_PRODUCTS_WITH_SCORE


def get_available_repeater_products_with_score() -> dict[str, int]:
    """Получение всех доступных повторнику продуктов с оценкой."""
    return REPEATER_PRODUCTS_WITH_SCORE

from datetime import date, timedelta

from common.constants import (
    CreditStatus, EXISTING_USER_DATA, EXISTING_USER_PRODUCT_DATA,
    EmploymentType,
)
from common.schemas.product import ProductWrite
from common.schemas.user import (
    UserDataPhoneWrite, ProfileWrite,
)


class CreditHistory:
    """Класс кредитной истории."""

    def __init__(
            self,
            product_data: ProductWrite
    ) -> None:
        self.loan_id: str = ''
        self.product_name = product_data.name
        self.amount = product_data.max_amount
        self.issue_date = date.today()
        self.term_days = product_data.term_days
        self.status: CreditStatus = CreditStatus.OPEN
        self.close_date: date | None = None


class User:
    """Класс пользователя."""

    def __init__(
            self,
            user_data: UserDataPhoneWrite,
    ) -> None:
        self.phone: str = user_data.phone
        self.age: int = user_data.age
        self.monthly_income: int = user_data.monthly_income
        self.employment_type: str = user_data.employment_type
        self.has_property: bool = user_data.has_property
        # Создаем пустую кредитную историю
        self.credit_history: list[CreditHistory] = []

    def add_credit_note(self, product_data: ProductWrite) -> None:
        """Метод добавления записи в кредитную историю."""
        credit_note = CreditHistory(
            product_data=product_data
        )
        self.credit_history.append(credit_note)

    def add_existing_credit_note(self, credit_note: CreditHistory) -> None:
        """Метод добавления существующей записи в кредитную историю."""
        self.credit_history.append(credit_note)

    def get_profile(self):
        """Метод получения профиля пользователя."""
        return ProfileWrite(
            age=self.age,
            monthly_income=self.monthly_income,
            employment_type=EmploymentType(self.employment_type),
            has_property=self.has_property,
        )


# "БД" пользователей
USERS: list[User] = []


def add_user(user_data: UserDataPhoneWrite) -> User:
    """Функция добавления пользователя в базу данных."""
    user = User(user_data=user_data)
    USERS.append(user)
    return user


def get_users() -> list[User]:
    """Функция получения всех пользователей в БД."""
    return USERS


def get_user_by_phone(phone: str) -> User | None:
    """Функция получения пользователя по его данным."""
    for user in USERS:
        if user.phone == phone:
            return user
    return None


def update_user(user: User, new_user_data: UserDataPhoneWrite) -> User:
    """Функция обновления данных о пользователе."""
    user.age = new_user_data.age
    user.monthly_income = new_user_data.monthly_income
    user.employment_type = new_user_data.employment_type
    user.has_property = new_user_data.has_property
    return user


# Создадим первого пользователя
first_user: User = User(
        user_data=UserDataPhoneWrite(**EXISTING_USER_DATA)
    )
# Добавим первому пользователю кредитную историю
first_user.credit_history = [CreditHistory(
    product_data=ProductWrite(**EXISTING_USER_PRODUCT_DATA)
)]
# Сделаем пользователю просроченный кредит
first_user.credit_history[0].issue_date = date.today() - timedelta(days=999)
# Добавим пользователя в БД
USERS.append(first_user)

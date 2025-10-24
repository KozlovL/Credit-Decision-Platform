from datetime import UTC, date, datetime

from common.constants import CreditStatus
from common.schemas.user import (
    ProfileWrite, UserPhoneWrite, CreditHistoryRead,
    ValidateStatusAndCloseDateMixin,
)
from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)


class UserDataRead(UserPhoneWrite):
    """Схема данных пользователя для чтения."""

    profile: ProfileWrite
    history: list[CreditHistoryRead]


class LoanCreate(CreditHistoryRead):
    """Схема для создания записи в кредитной истории."""

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')

    @field_validator('issue_date', 'close_date')
    def validate_dates(cls, value: date) -> date:
        """Валидация дат: дата не может быть в будущем."""
        if value is not None and value > datetime.now(UTC).date():
            raise ValueError('Несуществующая дата.')
        return value


class LoanUpdate(
    BaseModel,
    ValidateStatusAndCloseDateMixin,
):
    """Схема для обновления записи в кредитной истории."""

    loan_id: str
    status: CreditStatus
    close_date: date | None

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')

    @field_validator('close_date')
    def validate_dates(cls, value: date) -> date:
        """Валидация дат: дата не может быть в будущем."""
        if value is not None and value > datetime.now(UTC).date():
            raise ValueError('Несуществующая дата.')
        return value

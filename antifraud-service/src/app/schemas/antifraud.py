
from common.schemas.user import ProfileWrite, UserDataPhoneWrite, UserPhoneWrite
from pydantic import BaseModel, ConfigDict

from app.constants import DecisionType


class AntifraudRead(BaseModel):
    """Схема вывода решения антифрода для чтения."""

    decision: DecisionType
    reasons: list[str]


class PioneerAntifraudWrite(BaseModel):
    """Схема данных повторника для записи."""

    user_data: UserDataPhoneWrite

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')


class RepeaterAntifraudWrite(UserPhoneWrite):
    """Схема данных повторника для записи."""

    current_profile: ProfileWrite

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')

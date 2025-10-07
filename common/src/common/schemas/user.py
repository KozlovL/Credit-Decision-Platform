from http import HTTPStatus

from pydantic import ConfigDict, field_validator, BaseModel

from src.common.constants.user import PHONE_REGEX


class UserPhoneWrite(BaseModel):
    """Схема клиента для записи при выборе флоу."""
    phone: str

    @field_validator('phone')
    def validate_phone(cls, phone: str) -> str | None:
        if not PHONE_REGEX.match(phone):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=(
                    'Номер телефона должен быть строкой из 11 цифр и '
                    'начинаться на 7'
                    )
            )
        return phone

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')

from datetime import date
from http import HTTPStatus

from common.schemas.user import UserPhoneWrite
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import AVAILABLE_PRODUCTS
from app.models import User
from app.repository.user_data import user_data_crud
from app.schemas.user_data import LoanCreate, LoanUpdate


async def get_user_or_404_by_phone(phone: str, session: AsyncSession) -> User:
    """Функция, возвращающая пользователя по номеру телефона или ошибку 404."""
    user = await user_data_crud.get_user_data(session=session, phone=phone)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Пользователь не существует.'
        )
    return user


def check_products_exists(
    product: str
) -> None:
    """Функция, проверяющая существует ли переданный продукт."""
    if product not in AVAILABLE_PRODUCTS:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Продукт не существует.'
        )


def validate_phone(phone: str) -> None:
    """Валидация номера телефона."""
    try:
        # Валидируем номер телефона через схему
        UserPhoneWrite(phone=phone)
    except ValidationError as error:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=(
                'Номер телефона должен быть строкой из 11 цифр и '
                'начинаться на 7'
            )
        ) from error


def validate_loan_update_data(loan_data: LoanUpdate) -> LoanUpdate:
    """Валидация обновления данных о записи в кредитной истории."""
    try:
        loan_data = LoanUpdate(**loan_data.model_dump())
    except ValidationError as error:
        # Преобразуем все даты и сложные объекты в строки
        errors = error.errors()
        for e in errors:
            if isinstance(e.get('input'), date):
                e['input'] = e['input'].isoformat()
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=errors
        ) from error
    return loan_data


def validate_loan_create_data(loan_data: LoanCreate) -> LoanCreate:
    """Валидация создания данных о записи в кредитной истории."""
    try:
        loan_data = LoanCreate(**loan_data.model_dump())
    except ValidationError as error:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=error.errors()
        ) from error
    return loan_data

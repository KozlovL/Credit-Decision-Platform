import json
from http import HTTPStatus
from typing import Annotated

from common.schemas.user import CreditHistoryRead, ProfileWrite
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from app.api.validators import (
    check_products_exists,
    get_user_or_404_by_phone,
    validate_loan_create_data,
    validate_loan_update_data,
    validate_phone,
)
from app.constants import USER_DATA_PREFIX, USER_DATA_TAG
from app.core.db import get_session
from app.repository.user_data import user_data_crud
from app.schemas.user_data import LoanCreate, LoanUpdate, UserDataRead

router = APIRouter(prefix=USER_DATA_PREFIX, tags=[USER_DATA_TAG])


@router.get(
    '',
    response_model=UserDataRead,
    summary='Получение данных о пользователе по номеру телефона'
)
async def get_user_data(
        phone: str = Query(...),
        session: AsyncSession = Depends(get_session)
) -> UserDataRead:
    # Валидируем номер телефона
    validate_phone(phone=phone)

    # Ищем пользователя в БД
    user = await get_user_or_404_by_phone(session=session, phone=phone)

    user_data = jsonable_encoder(user)
    user_data.pop('id')
    credit_history = user_data.pop('credit_notes')
    phone = user_data.pop('phone')

    # Собираем профиль
    profile = ProfileWrite(
        **user_data
    )

    # Собираем кредитную историю
    history = [
        CreditHistoryRead(
            **credit_note
        )
        for credit_note in credit_history
    ]

    return UserDataRead(phone=phone, profile=profile, history=history)


@router.put(
    '',
    summary=(
            'Создание и обновление профиля. Добавление и изменение записи в '
            'кредитной истории. Комбинированное обновление.'
    )
)
async def update_user_data(
        phone: str = Body(...),
        profile: ProfileWrite | None = None,
        loan_entry: Annotated[LoanCreate | LoanUpdate, Body()] | None = None,
        session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    # Достаем телефон из схемы
    validate_phone(phone=phone)

    # Флаг для определения статус-кода в ответе
    created = None

    # Сценарий создания или обновления профиля
    if profile is not None:
        # Ищем пользователя в БД
        user = await user_data_crud.get_user_data(session=session, phone=phone)
        # Если пользователь существует, то обновляем его данные
        if user is not None:
            user = await user_data_crud.update_user_profile(
                session=session,
                user=user,
                new_profile=profile,
            )

            created = False
        # Иначе создаем
        else:
            user = await user_data_crud.create_user_profile(
                session=session,
                phone=phone,
                profile=profile,
            )

            created = True

    # Сценарии добавления и обновления записи в кредитной истории
    if loan_entry is not None:
        # Проверяем наличие пользователя в БД
        user = await get_user_or_404_by_phone(session=session, phone=phone)

        # Ищем запись в кредитной истории
        for credit_note in user.credit_notes:
            # Если нашли
            if loan_entry.loan_id == credit_note.loan_id:
                # Валидируем данные
                loan_data = validate_loan_update_data(
                    loan_data=loan_entry  # type: ignore[arg-type]
                )

                # Обновляем запись в кредитной истории
                await user_data_crud.update_credit_note(
                    session=session,
                    credit_note=credit_note,
                    loan_data=loan_data,
                )

                created = False
                break
        else:
            # Валидируем данные
            loan_data = validate_loan_create_data(  # type: ignore[assignment]
                loan_data=loan_entry  # type: ignore[arg-type]
            )

            # Проверяем продукт на существование
            check_products_exists(
                product=loan_data.product_name  # type: ignore[attr-defined]
            )

            # Создаем запись
            await user_data_crud.create_credit_note(
                session=session,
                loan_data=loan_data,  # type: ignore[arg-type]
                user=user
            )

            created = False

    if created is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нужно ввести либо profile, либо loan_entry'
        )

    user = await user_data_crud.get_user_data(
        session=session,
        phone=phone
    )

    user_data = jsonable_encoder(user)
    user_data.pop('id')
    credit_history = user_data.pop('credit_notes')
    phone = user_data.pop('phone')

    # Собираем профиль
    profile = ProfileWrite(
        **user_data
    )

    # Собираем кредитную историю
    history = [
        CreditHistoryRead(
            **credit_note
        )
        for credit_note in credit_history
    ]

    # Формируем ответ
    response_data = UserDataRead(
        phone=phone,
        profile=profile,
        history=history
    )

    return JSONResponse(
        content=json.loads(response_data.model_dump_json()),
        status_code=status.HTTP_201_CREATED if created else status.HTTP_200_OK
    )

import json
from typing import Annotated

from common.constants import EmploymentType
from common.repository.user import (
    get_user_by_phone, update_user, add_user,
)
from common.schemas.user import ProfileWrite, UserDataPhoneWrite
from fastapi import APIRouter, Query, Body
from starlette import status
from starlette.responses import JSONResponse

from app.api.validators import (
    get_user_or_404_by_phone, check_products_exists,
    validate_phone, validate_loan_update_data, validate_loan_create_data,
)
from app.constants import USER_DATA_PREFIX, USER_DATA_TAG
from app.repository.user_data import (
    update_credit_note,
    create_existing_credit_note, get_credit_history,
)
from app.schemas.user_data import (
    UserDataRead, LoanCreateOrUpdate, LoanCreate, LoanUpdate,
)

router = APIRouter(prefix=USER_DATA_PREFIX, tags=[USER_DATA_TAG])


@router.get(
    '',
    response_model=UserDataRead,
    summary='Получение данных о пользователе по номеру телефона'
)
def get_user_data(
        phone: str = Query(...),
) -> UserDataRead:
    # Валидируем номер телефона
    validate_phone(phone=phone)

    # Ищем пользователя в БД
    user = get_user_or_404_by_phone(phone=phone)

    # Собираем профиль
    profile = ProfileWrite(
        age=user.age,
        monthly_income=user.monthly_income,
        employment_type=EmploymentType(user.employment_type),
        has_property=user.has_property,
    )

    # Собираем кредитную историю
    history = get_credit_history(user=user)

    return UserDataRead(phone=phone, profile=profile, history=history)


@router.put(
    '',
    summary=(
            'Создание и обновление профиля. Добавление и изменение записи в '
            'кредитной истории. Комбинированное обновление.'
    )
)
def update_user_data(
        phone: str = Body(...),
        profile: ProfileWrite | None = None,
        loan_entry: Annotated[LoanCreate | LoanUpdate, Body()] | None = None,
) -> JSONResponse:
    # Достаем телефон из схемы
    validate_phone(phone=phone)
    user = None
    created = False

    # Сценарий создания или обновления профиля
    if profile is not None:
        # Ищем пользователя в БД
        user = get_user_by_phone(phone=phone)
        # Если пользователь существует, то обновляем его данные
        if user is not None:
            update_user(
                user=user,
                new_user_data=UserDataPhoneWrite(
                    phone=phone,
                    **profile.model_dump()
                ),
            )
        # Иначе создаем
        else:
            user = add_user(
                user_data=UserDataPhoneWrite(
                    phone=phone,
                    **profile.model_dump()
                )
            )
            created = True

    # Сценарии добавления и обновления записи в кредитной истории
    if loan_entry is not None:
        # Проверяем наличие пользователя в БД
        user = get_user_or_404_by_phone(phone=phone)

        # Ищем запись в кредитной истории
        for credit_note in user.credit_history:
            # Если нашли
            if loan_entry.loan_id == credit_note.loan_id:
                # Валидируем данные
                loan_data = validate_loan_update_data(loan_data=loan_entry)

                # Обновляем запись в кредитной истории
                update_credit_note(
                    credit_note=credit_note,
                    loan_data=loan_data,
                )
                break
        else:
            # Валидируем данные
            loan_data = validate_loan_create_data(loan_data=loan_entry)

            # Проверяем продукт на существование
            check_products_exists(
                product=loan_data.product_name
            )

            # Создаем запись
            new_credit_note = create_existing_credit_note(
                loan_entry=loan_data,
            )
            # Добавляем запись в кредитную историю
            user.add_existing_credit_note(
                credit_note=new_credit_note
            )

    # Формируем ответ
    response_data = UserDataRead(
        phone=phone,
        profile=user.get_profile(),
        history=get_credit_history(user=user)
    )

    return JSONResponse(
        content=json.loads(response_data.model_dump_json()),
        status_code=status.HTTP_201_CREATED if created else status.HTTP_200_OK
    )

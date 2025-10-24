import time
from datetime import datetime, UTC

import pytest
from common.constants import EmploymentType, CreditStatus
from common.repository.user import USERS, add_user
from common.schemas.user import UserDataPhoneWrite
from fastapi.testclient import TestClient

from app.repository.user_data import create_existing_credit_note
from app.schemas.user_data import LoanCreate
from app.service import app


@pytest.fixture(scope='session')
def client():
    """Тестовый клиент FastAPI."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    """Очищает USERS между тестами."""
    USERS.clear()
    yield
    USERS.clear()


def generate_loan_id(phone: str) -> str:
    """Генерация корректного loan_id в формате loan_{phone}_{timestamp}."""
    # Делаем паузу для гарантии уникальности
    time.sleep(1)
    timestamp = datetime.now(UTC).strftime('%Y%m%d%H%M%S')
    return f'loan_{phone}_{timestamp}'


@pytest.fixture
def existing_user():
    """Существующий пользователь с кредитной историей."""
    user = add_user(UserDataPhoneWrite(
        phone='79123456789',
        age=30,
        monthly_income=50000,
        employment_type=EmploymentType.FULL_TIME,
        has_property=True
    ))

    # Создаём кредит через create_existing_credit_note
    credit_note = create_existing_credit_note(
        loan_entry=LoanCreate(
            loan_id=generate_loan_id(user.phone),
            product_name='PrimeCredit',
            amount=15000000,
            issue_date=datetime.now(UTC).date(),
            term_days=180,
            status=CreditStatus.OPEN,
            close_date=None,
        ),
    )

    user.credit_history.append(credit_note)
    return user


@pytest.fixture
def new_user_payload():
    """Payload для создания нового пользователя."""
    return {
        'phone': '79999990001',
        'profile': {
            'age': 25,
            'monthly_income': 30000,
            'employment_type': EmploymentType.FULL_TIME,
            'has_property': False
        }
    }


@pytest.fixture
def update_profile_payload(existing_user):
    """Payload для обновления профиля существующего пользователя."""
    return {
        'phone': existing_user.phone,
        'profile': {
            'age': 35,
            'monthly_income': 55000,
            'employment_type': EmploymentType.FULL_TIME,
            'has_property': True
        }
    }


@pytest.fixture
def new_loan_entry_payload(existing_user):
    """Payload для добавления новой записи в кредитную историю."""
    return {
        'phone': existing_user.phone,
        'loan_entry': {
            'loan_id': generate_loan_id(existing_user.phone),
            'product_name': 'AdvantagePlus',
            'amount': 1000000,
            'issue_date': str(datetime.now(UTC).date()),
            'term_days': 120,
            'status': CreditStatus.OPEN,
            'close_date': None
        }
    }


@pytest.fixture
def update_loan_status_payload(existing_user):
    """Payload для обновления статуса существующей записи."""
    existing_loan_id = existing_user.credit_history[0].loan_id
    return {
        'phone': existing_user.phone,
        'loan_entry': {
            'loan_id': existing_loan_id,
            'status': CreditStatus.CLOSED,
            'close_date': str(datetime.now(UTC).date())
        }
    }


@pytest.fixture
def combined_update_payload():
    """Payload для обновления профиля и добавления новой записи."""
    phone = '79999990002'
    return {
        'phone': phone,
        'profile': {
            'age': 40,
            'monthly_income': 60000,
            'employment_type': EmploymentType.FREELANCE,
            'has_property': True
        },
        'loan_entry': {
            'loan_id': generate_loan_id(phone),
            'product_name': 'PrimeCredit',
            'amount': 150000,
            'issue_date': str(datetime.now(UTC).date()),
            'term_days': 180,
            'status': CreditStatus.OPEN,
            'close_date': None
        }
    }


@pytest.fixture
def invalid_product_payload(existing_user):
    """Payload с несуществующим названием продукта."""
    return {
        'phone': existing_user.phone,
        'loan_entry': {
            'loan_id': generate_loan_id(existing_user.phone),
            'product_name': 'InvalidProduct',
            'amount': 5000000,
            'issue_date': str(datetime.now(UTC).date()),
            'term_days': 60,
            'status': CreditStatus.OPEN,
            'close_date': None
        }
    }


@pytest.fixture
def invalid_date_payload(existing_user):
    """Payload с некорректной датой."""
    return {
        'phone': existing_user.phone,
        'loan_entry': {
            'loan_id': generate_loan_id(existing_user.phone),
            'product_name': 'PrimeCredit',
            'amount': 150000,
            'issue_date': '2030-02-30',  # несуществующая дата
            'term_days': 180,
            'status': CreditStatus.OPEN,
            'close_date': None
        }
    }


@pytest.fixture
def duplicate_loan_id_payload(existing_user):
    """Payload с уже существующим loan_id."""
    existing_loan_id = existing_user.credit_history[0].loan_id
    return {
        'phone': existing_user.phone,
        'loan_entry': {
            'loan_id': existing_loan_id,
            'product_name': 'PrimeCredit',
            'amount': 150000,
            'issue_date': str(datetime.now(UTC).date()),
            'term_days': 180,
            'status': CreditStatus.OPEN,
            'close_date': None
        }
    }

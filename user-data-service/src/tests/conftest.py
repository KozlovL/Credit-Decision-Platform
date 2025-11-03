from datetime import UTC, date, datetime, timedelta
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from common.constants import CreditStatus, EmploymentType
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import selectinload
from app.constants import TEST_DATABASE_URL
try:
    from app.core.db import Base, get_session
except Exception:
    pass
from app.models.user_data import CreditNote, User
from app.service import app


# Асинхронный движок
engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False
)


# Перезапись зависимости FastAPI
async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


app.dependency_overrides[get_session] = override_get_session



@pytest_asyncio.fixture(scope='function')
async def client() -> AsyncGenerator[AsyncClient, None]:
    """HTTP клиент с собственной БД для каждого теста"""
    # Подготавливаем БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        yield client
    
    # Очищаем БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture
async def existing_user(client) -> User:
    """Создание тестового пользователя - зависит от клиента"""
    # Ждем пока клиент подготовит БД
    async with AsyncSessionLocal() as session:
        user = User(
            phone='79123456789',
            age=30,
            monthly_income=50000,
            employment_type=EmploymentType.FULL_TIME,
            has_property=True,
        )
        session.add(user)
        await session.flush()

        loan = CreditNote(
            loan_id=f'loan_{user.phone}_{datetime.now(UTC).strftime("%Y%m%d%H%M%S")}',
            product_name='PrimeCredit',
            amount=15000000,
            issue_date=date.today(),
            term_days=180,
            status=CreditStatus.OPEN,
            close_date=None,
            user_id=user.id,
        )
        session.add(loan)

        await session.commit()
        
        return user


@pytest.fixture
def new_user_payload():
    return {
        'phone': '79999990001',
        'profile': {
            'age': 25,
            'monthly_income': 30000,
            'employment_type': EmploymentType.FULL_TIME,
            'has_property': False,
        },
    }

@pytest.fixture
def update_profile_payload(existing_user):
    return {
        'phone': existing_user.phone,
        'profile': {
            'age': 35,
            'monthly_income': 55000,
            'employment_type': EmploymentType.FULL_TIME,
            'has_property': True,
        },
    }

@pytest.fixture
def new_loan_entry_payload(existing_user):
    timestamp = datetime.now(UTC) + timedelta(seconds=1)
    loan_id = f'loan_{existing_user.phone}_{timestamp.strftime("%Y%m%d%H%M%S")}'
    return {
        'phone': existing_user.phone,
        'loan_entry': {
            'loan_id': loan_id,
            'product_name': 'AdvantagePlus',
            'amount': 1000000,
            'issue_date': str(date.today()),
            'term_days': 120,
            'status': CreditStatus.OPEN,
            'close_date': None,
        },
    }

@pytest_asyncio.fixture
async def update_loan_status_payload(existing_user):
    async with AsyncSessionLocal() as session:
        # Загружаем пользователя с кредитными записями в новой сессии
        user = await session.get(
            User, existing_user.id, options=[selectinload(User.credit_notes)]
        )
        existing_loan_id = user.credit_notes[0].loan_id  #type: ignore[union-attr]
        
        return {
            'phone': user.phone,  #type: ignore[union-attr]
            'loan_entry': {
                'loan_id': existing_loan_id,
                'status': CreditStatus.CLOSED,
                'close_date': str(date.today()),
            },
        }

@pytest.fixture
def combined_update_payload():
    phone = '79999990002'
    timestamp = datetime.now(UTC) + timedelta(seconds=1)
    loan_id = f'loan_{phone}_{timestamp.strftime("%Y%m%d%H%M%S")}'
    return {
        'phone': phone,
        'profile': {
            'age': 40,
            'monthly_income': 6000000,
            'employment_type': EmploymentType.FREELANCE,
            'has_property': True,
        },
        'loan_entry': {
            'loan_id': loan_id,
            'product_name': 'PrimeCredit',
            'amount': 15000000,
            'issue_date': str(date.today()),
            'term_days': 180,
            'status': CreditStatus.OPEN,
            'close_date': None,
        },
    }

@pytest.fixture
def invalid_product_payload(existing_user):
    timestamp = datetime.now(UTC) + timedelta(seconds=1)
    loan_id = f'loan_{existing_user.phone}_{timestamp.strftime("%Y%m%d%H%M%S")}'
    return {
        'phone': existing_user.phone,
        'loan_entry': {
            'loan_id': loan_id,
            'product_name': 'InvalidProduct',
            'amount': 5000000,
            'issue_date': str(date.today()),
            'term_days': 60,
            'status': CreditStatus.OPEN,
            'close_date': None,
        },
    }

@pytest.fixture
def invalid_date_payload(existing_user):
    timestamp = datetime.now(UTC) + timedelta(seconds=1)
    loan_id = f'loan_{existing_user.phone}_{timestamp.strftime("%Y%m%d%H%M%S")}'
    return {
        'phone': existing_user.phone,
        'loan_entry': {
            'loan_id': loan_id,
            'product_name': 'PrimeCredit',
            'amount': 150000,
            'issue_date': '2030-02-30',  # несуществующая дата
            'term_days': 180,
            'status': CreditStatus.OPEN,
            'close_date': None,
        },
    }

@pytest_asyncio.fixture
async def duplicate_loan_id_payload(existing_user):
    async with AsyncSessionLocal() as session:
        # Загружаем пользователя с кредитными записями в новой сессии
        user = await session.get(
            User, existing_user.id, options=[selectinload(User.credit_notes)]
        )
        existing_loan_id = user.credit_notes[0].loan_id  #type: ignore[union-attr]
        
        return {
            'phone': user.phone,  #type: ignore[union-attr]
            'loan_entry': {
                'loan_id': existing_loan_id,
                'product_name': 'PrimeCredit',
                'amount': 150000,
                'issue_date': str(date.today()),
                'term_days': 180,
                'status': CreditStatus.OPEN,
                'close_date': None,
            },
        }

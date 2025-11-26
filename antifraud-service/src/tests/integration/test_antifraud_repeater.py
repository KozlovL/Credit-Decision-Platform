import pytest
from starlette import status
from common.constants import CreditStatus


@pytest.mark.asyncio
async def test_check_repeater_passed(client, mock_data_service_client):
    """Интеграционный тест Repeater: успешная проверка."""
    phone = '79998887777'
    mock_data_service_client.get_user_data.return_value = {
        'phone': phone,
        'history': [
            {
                'loan_id': 'loan_72222222222_20251103123000',
                'product_name': 'MicroLoan',
                'amount': 100_000,
                'issue_date': '2023-01-01',  # добавлена запись
                'term_days': 90,
                'status': CreditStatus.CLOSED,          # закрытый кредит
                'close_date': '2023-04-01'
            }
        ],
        'profile': {
            'age': 30,
            'monthly_income': 5000000,
            'employment_type': 'full_time',
            'has_property': False
        }
    }

    payload = {
        'phone': phone,
        'current_profile': {
            'age': 30,
            'monthly_income': 5000000,
            'employment_type': 'full_time',
            'has_property': False
        }
    }

    response = client.post('/api/antifraud/repeater/check', json=payload)
    data = response.json()


    assert response.status_code == status.HTTP_200_OK
    assert data['decision'] == 'passed'
    assert data['reasons'] == []


@pytest.mark.asyncio
async def test_check_repeater_rejected(client, mock_data_service_client):
    """Интеграционный тест Repeater: срабатывание правил."""
    phone = '79998887777'
    mock_data_service_client.get_user_data.return_value = {
        'phone': phone,
        'history': [
            {
                'loan_id': 'loan_72222222222_20251103123000',
                'product_name': 'MicroLoan',
                'amount': 100_000,
                'issue_date': '2020-01-01',
                'term_days': 90,
                'status': CreditStatus.OPEN,
                'close_date': None
            }
        ],
        'profile': {
            'age': 30,
            'monthly_income': 5000000,
            'employment_type': 'full_time',
            'has_property': False
        }
    }

    payload = {
        'phone': phone,
        'current_profile': {
            'age': 30,
            'monthly_income': 10_000_00 - 1,
            'employment_type': 'full_time',
            'has_property': False
        }
    }

    response = client.post('/api/antifraud/repeater/check', json=payload)
    data = response.json()


    assert response.status_code == status.HTTP_200_OK
    assert data['decision'] == 'rejected'
    assert any('Monthly income is below minimum threshold' in r or
               'Account has overdue payments' in r for r in data['reasons'])
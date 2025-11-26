import pytest
from starlette import status


@pytest.mark.asyncio
async def test_check_pioneer_passed(client):
    """Интеграционный тест Pioneer: успешная проверка."""
    payload = {
        'user_data': {
            'phone': '79998887766',
            'age': 30,
            'monthly_income': 5000000,
            'employment_type': 'full_time',
            'has_property': False
        }
    }

    response = client.post('api/antifraud/pioneer/check', json=payload)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['decision'] == 'passed'
    assert data['reasons'] == []


@pytest.mark.asyncio
async def test_check_pioneer_rejected(client):
    """Интеграционный тест Pioneer: срабатывание правил."""
    payload = {
        'user_data': {
            'phone': '79998887766',
            'age': 16,
            'monthly_income': 5000_00,
            'employment_type': 'unemployed',
            'has_property': True
        }
    }

    response = client.post('api/antifraud/pioneer/check', json=payload)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['decision'] == 'rejected'
    assert len(data['reasons']) >= 1
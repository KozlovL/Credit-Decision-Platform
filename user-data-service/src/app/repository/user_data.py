from common.repository.user import CreditHistory, User

from app.schemas.user_data import (
    CreditHistoryRead,
    LoanCreate,
    LoanUpdate,
)


def update_credit_note(
        credit_note: CreditHistory,
        loan_data: LoanUpdate,
) -> CreditHistory:
    """Функция обновления записи в кредитной истории."""
    credit_note.status = loan_data.status
    credit_note.close_date = loan_data.close_date
    return credit_note


def create_existing_credit_note(
        loan_entry: LoanCreate
) -> CreditHistory:
    """Добавляет уже существующую запись в кредитную историю."""
    credit = CreditHistory.__new__(CreditHistory)  # обходим __init__
    credit.loan_id = loan_entry.loan_id
    credit.product_name = loan_entry.product_name
    credit.amount = loan_entry.amount
    credit.issue_date = loan_entry.issue_date
    credit.term_days = loan_entry.term_days
    credit.status = loan_entry.status
    credit.close_date = loan_entry.close_date
    return credit


def get_credit_history(user: User) -> list[CreditHistoryRead]:
    """Функция получения кредитной истории пользователя по схеме."""
    return [
        CreditHistoryRead(
            loan_id=credit_note.loan_id,
            product_name=credit_note.product_name,
            amount=credit_note.amount,
            issue_date=credit_note.issue_date,
            term_days=credit_note.term_days,
            status=credit_note.status,
            close_date=credit_note.close_date,
        )
        for credit_note in user.credit_history
    ]

from common.schemas.user import ProfileWrite
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import CreditNote, User
from app.schemas.user_data import LoanCreate, LoanUpdate


class UserDataCRUD:
    """Класс, реализующий CRUD операции с данными пользователя."""

    async def get_user_data(
            self,
            session: AsyncSession,
            phone: str
    ) -> User | None:
        """Метод, возвращающий данные пользователя по номеру телефона."""
        db_object = await session.execute(
            select(User).where(
                User.phone == phone
            ).options(
                selectinload(User.credit_notes)
            )
        )

        return db_object.scalars().first()

    async def update_user_profile(
            self,
            session: AsyncSession,
            user: User,
            new_profile: ProfileWrite
    ) -> User:
        """Метод, обновляющий профиль пользователя."""
        user_data = jsonable_encoder(user)
        new_profile_data = new_profile.model_dump(exclude_unset=True)

        for field in user_data:
            if field in new_profile_data:
                setattr(user, field, new_profile_data[field])

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    async def create_user_profile(
            self,
            session: AsyncSession,
            phone: str,
            profile: ProfileWrite
    ) -> User:
        """Метод, создающий пользователя."""
        profile_data = profile.model_dump()

        user = User(phone=phone, **profile_data)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    async def update_credit_note(
            self,
            session: AsyncSession,
            credit_note: CreditNote,
            loan_data: LoanUpdate
    ) -> CreditNote:
        """Метод, обновляющий запись в кредитной истории."""
        credit_note_data = jsonable_encoder(credit_note)
        loan_data_dict = loan_data.model_dump(exclude_unset=True)

        for field in credit_note_data:
            if field in loan_data_dict:
                setattr(credit_note, field, loan_data_dict[field])

        session.add(credit_note)
        await session.commit()
        await session.refresh(credit_note)

        return credit_note

    async def create_credit_note(
            self,
            session: AsyncSession,
            loan_data: LoanCreate,
            user: User
    ) -> CreditNote:
        """Метод, создающий запись в кредитной истории."""
        loan_data_dict = loan_data.model_dump()

        credit_note = CreditNote(user=user, **loan_data_dict)

        session.add(credit_note)
        await session.commit()
        await session.refresh(credit_note)

        return credit_note


user_data_crud = UserDataCRUD()

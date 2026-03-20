from models.user import User
from db.db_service import get_db_session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from email_validator import EmailNotValidError, validate_email


class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


async def save_user_to_db(user: User):
    async with get_db_session() as session:
        session.add(user)
        try:
            await session.commit()
            await session.refresh(user)
        except IntegrityError as e:
            await session.rollback()
            print(e)
            raise UserAlreadyExistsError()


async def get_user(username_or_email: str) -> User:
    async with get_db_session() as session:
        try:
            validate_email(username_or_email)
            query_filter = User.email
        except EmailNotValidError:
            query_filter = User.username
        stmt = select(User).where(query_filter == username_or_email)

        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise UserNotFoundError()
        return user

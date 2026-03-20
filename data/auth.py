from models.user import User
from db.db_service import get_db_session
from sqlalchemy.exc import IntegrityError


class UserAlreadyExistsError(Exception):
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

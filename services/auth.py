from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from models.user import User, Role
from services.db_service import get_db_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def add_user(
    username: str, password: str, email: str, role: Role = Role.user
) -> User | None:
    hashed_password = pwd_context.hash(password)

    async with get_db_session() as session:
        db_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role=role,
        )
        session.add(db_user)
        try:
            await session.commit()
            await session.refresh(db_user)
        except IntegrityError:
            await session.rollback()
            return
        return db_user

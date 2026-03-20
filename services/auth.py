from passlib.context import CryptContext
from models.user import User, Role
from data.auth import save_user_to_db, UserAlreadyExistsError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def add_user(
    username: str, password: str, email: str, role: Role = Role.user
) -> User:
    hashed_password = pwd_context.hash(password)
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role,
    )

    await save_user_to_db(db_user)
    return db_user

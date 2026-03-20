from passlib.context import CryptContext
from models.user import User, Role
from data.auth import (
    UserNotFoundError,
    get_user,
    save_user_to_db,
    UserAlreadyExistsError,
)
from jose import JWTError, jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UnauthorizedError(Exception):
    pass


class ForbiddenError(Exception):
    pass


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


async def authenticate_user(
    username_or_email: str,
    password: str,
) -> User:
    user = await get_user(username_or_email=username_or_email)

    if not pwd_context.verify(password, user.hashed_password):
        raise UserNotFoundError
    return user


SECRET_KEY = "a_very_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    # expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_access_token(
    token: str,
) -> User | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
    except JWTError:
        return
    if not username:
        return
    user = await get_user(username)
    return user


async def authorize_user(token: str, roles: list[Role]) -> User:
    user = await decode_access_token(token)

    if not user:
        raise UnauthorizedError("Unauthorized")

    if user.role not in roles:
        raise ForbiddenError("Forbidden")

    return user

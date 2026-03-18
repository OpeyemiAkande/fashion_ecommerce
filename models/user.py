from pydantic import BaseModel, Field, EmailStr
from typing import List, Annotated
from enum import Enum

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class Role(str, Enum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    role: Mapped[Role] = mapped_column(default=Role.user)
    totp_secret: Mapped[str] = mapped_column(nullable=True)


class UserCreateRequest(BaseModel):
    email: str = Field(description="The email of the user")
    username: str = Field(description="The username of the user")
    password: str = Field(description="The password for the user")


class UserCreateResponse(BaseModel):
    username: str
    email: EmailStr


class ResponseCreateUser(BaseModel):
    message: Annotated[str, Field(default="user created")]
    user: UserCreateResponse

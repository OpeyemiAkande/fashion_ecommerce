from pydantic import BaseModel, Field, EmailStr
from typing import List, Annotated, Optional
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
    customer = "customer"
    vendor = "vendor"
    admin = "admin"
    superadmin = "superadmin"


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


class UserLoginRequest(BaseModel):
    username_or_email: str = Field(
        description="The registered username or email of the user"
    )
    password: str = Field(description="Registered password of the user")


class ResponseCreateUser(BaseModel):
    message: Annotated[str, Field(default="user created")]
    user: UserCreateResponse


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []

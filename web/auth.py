from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import (
    UserCreateRequest,
    UserCreateResponse,
    ResponseCreateUser,
    Token,
)
import services.auth as service
from data.auth import UserAlreadyExistsError, UserNotFoundError

router = APIRouter(prefix="/auth")


@router.post("/register", status_code=201, response_model=ResponseCreateUser)
async def register_user(
    request: UserCreateRequest,
) -> ResponseCreateUser:
    try:

        user = await service.add_user(**request.model_dump())
        user_response = UserCreateResponse(username=user.username, email=user.email)

        return ResponseCreateUser(message="user created", user=user_response)
    except UserAlreadyExistsError:
        raise HTTPException(status_code=409, detail="username or email already exists")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/token", status_code=201, response_model=Token)
async def get_user_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    try:
        user = await service.authenticate_user(form_data.username, form_data.password)
    except UserNotFoundError:
        raise HTTPException(status_code=401, detail="Incorrect username or Password")

    access_token = service.create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.get(
    "/users/me",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "User not authorized"},
        status.HTTP_200_OK: {"description": "username authorized"},
    },
)
async def read_user_me(token: str = Depends(oauth2_scheme)):
    user = await service.decode_access_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
        )
    return {"description": f"{user.username} authorized"}

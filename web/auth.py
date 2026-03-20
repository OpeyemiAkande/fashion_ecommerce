from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import (
    Role,
    User,
    UserCreateRequest,
    UserCreateResponse,
    ResponseCreateUser,
    Token,
)
import services.auth as service
from services.email.email_service import EmailService
from data.auth import UserAlreadyExistsError, UserNotFoundError


router = APIRouter(prefix="/auth")
email_service = EmailService()


async def get_authorized_user(token: str, roles: list[Role]) -> User:
    try:
        user = await service.authorize_user(token, roles)
    except service.UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except service.ForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))
    return user


@router.post("/register", status_code=201, response_model=ResponseCreateUser)
async def register_user(
    request: UserCreateRequest, background_tasks: BackgroundTasks
) -> ResponseCreateUser:
    try:

        user = await service.add_user(**request.model_dump())
        user_response = UserCreateResponse(username=user.username, email=user.email)
        background_tasks.add_task(
            email_service.send_welcome_email, user.email, user.username
        )

        return ResponseCreateUser(message="user created", user=user_response)
    except UserAlreadyExistsError:
        raise HTTPException(status_code=409, detail="username or email already exists")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/register/vendor", status_code=201, response_model=ResponseCreateUser)
async def register_vendor(
    request: UserCreateRequest,
) -> ResponseCreateUser:
    try:
        role = Role.vendor
        user = await service.add_user(**request.model_dump(), role=Role.vendor)
        user_response = UserCreateResponse(username=user.username, email=user.email)

        return ResponseCreateUser(message="Vendor created", user=user_response)
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
        status.HTTP_401_UNAUTHORIZED: {"descriptiomn": "User not authorized"},
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


@router.get("/admin/dashboard")
async def admin_dashboard(token: str = Depends(oauth2_scheme)):
    user = await get_authorized_user(token=token, roles=[Role.admin])

    return {"message": f"Welcome {user.username}"}

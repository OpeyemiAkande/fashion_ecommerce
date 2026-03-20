from fastapi import APIRouter, HTTPException, status
from models.user import UserCreateRequest, UserCreateResponse, ResponseCreateUser
import services.auth as service
from data.auth import UserAlreadyExistsError

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

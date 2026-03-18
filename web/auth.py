from fastapi import APIRouter, HTTPException, status
from models.user import UserCreateRequest, UserCreateResponse, ResponseCreateUser
import services.auth as service

router = APIRouter(prefix="/auth")


@router.post("/register", status_code=201, response_model=ResponseCreateUser)
async def register_user(
    request: UserCreateRequest,
) -> dict[str, UserCreateResponse | str]:
    try:

        user = await service.add_user(**request.model_dump())
        if not user:
            raise HTTPException(
                status.HTTP_409_CONFLICT, "username or email already exists"
            )
        user_response = UserCreateResponse(username=user.username, email=user.email)
        return {"message": "user created", "user": user_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

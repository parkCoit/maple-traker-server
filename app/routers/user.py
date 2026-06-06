from fastapi import APIRouter

from app.schemas.user import AutoLoginRequest, LoginRequest, LogoutRequest
from app.services.user import UserService

router = APIRouter()


@router.post("/login")
def login(payload: LoginRequest):
    return UserService.login_process(
        nickname=payload.nickname,
        password=payload.password,
        auto_login=payload.auto_login,
    )


@router.post("/auto-login")
def auto_login(payload: AutoLoginRequest):
    return UserService.auto_login_process(session_token=payload.session_token)


@router.post("/logout")
def logout(payload: LogoutRequest):
    return UserService.logout_process(session_token=payload.session_token)

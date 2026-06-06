from pydantic import BaseModel


class LoginRequest(BaseModel):
    nickname: str
    password: str
    auto_login: bool = False


class AutoLoginRequest(BaseModel):
    session_token: str


class LogoutRequest(BaseModel):
    session_token: str
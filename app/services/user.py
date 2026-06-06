from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import create_token, verify_token
from app.cruds.user import UserCrud
from app.services.farming_service import FarmingService
from app.core.supabase import supabase


class UserService:

    @staticmethod
    def get_character_info(nickname: str) -> dict:
        if not hasattr(settings, "MAPLE_API_KEY") or not settings.MAPLE_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="서버 설정 오류: 메이플 API 키가 없습니다.",
            )

        headers = {"x-nxopen-api-key": settings.MAPLE_API_KEY}

        try:
            id_url = f"https://open.api.nexon.com/maplestory/v1/id?character_name={nickname}"
            import requests
            id_res = requests.get(id_url, headers=headers, timeout=5)

            if id_res.status_code == 503:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="넥슨 서버 점검 중입니다.",
                )
            if id_res.status_code != 200:
                return None

            ocid = id_res.json().get("ocid")
            if not ocid:
                return None

            basic_url = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid}"
            basic_res = requests.get(basic_url, headers=headers, timeout=5)

            if basic_res.status_code == 503:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="넥슨 서버 점검 중입니다.",
                )
            if basic_res.status_code != 200:
                return None

            basic_info = basic_res.json()

            return {
                "ocid": ocid,
                "character_name": basic_info.get("character_name"),
                "world_name": basic_info.get("world_name"),
                "character_class": basic_info.get("character_class"),
                "character_level": basic_info.get("character_level"),
                "character_exp": basic_info.get("character_exp_rate"),
                "character_image": basic_info.get("character_image"),
            }

        except requests.exceptions.RequestException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="넥슨 서버 응답 시간 초과(타임아웃).",
            )

    @classmethod
    def login_process(cls, nickname: str, password: str, auto_login: bool):
        if password != settings.ACCESS_PASSWORD:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="비밀번호가 틀렸습니다.",
            )

        maple_data = cls.get_character_info(nickname)
        if not maple_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="메이플 아이디를 확인하세요.",
            )

        user_crud = UserCrud(supabase_client=supabase)
        try:
            user_crud.read_user_by_nickname(nickname)
        except HTTPException as e:
            if e.status_code == status.HTTP_404_NOT_FOUND:
                user_crud.create_user(nickname)
            else:
                raise e

        session_token = create_token(data={"sub": nickname})
        farming = FarmingService.get_logs(nickname)
        summary = FarmingService.build_farming_summary(farming)

        return {
            "nickname": nickname,
            "session_token": session_token,
            "maple": maple_data,
            "summary": summary,
            "farming": farming,
        }

    @classmethod
    def auto_login_process(cls, session_token: str):
        payload = verify_token(session_token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="자동 로그인 세션이 만료되었거나 올바르지 않습니다.",
            )

        fixed_nickname = payload.get("sub")
        if not fixed_nickname:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="잘못된 토큰 서식입니다.",
            )

        maple_data = cls.get_character_info(fixed_nickname)
        farming = FarmingService.get_logs(fixed_nickname)
        summary = FarmingService.build_farming_summary(farming)

        return {
            "nickname": fixed_nickname,
            "session_token": session_token,
            "maple": maple_data,
            "summary": summary,
            "farming": farming,
        }

    @classmethod
    def logout_process(cls, session_token: str):
        payload = verify_token(session_token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 세션 토큰입니다.",
            )

        return {"detail": "Logout successful"}

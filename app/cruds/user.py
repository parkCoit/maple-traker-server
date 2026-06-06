from abc import ABC
from fastapi import HTTPException, status
from postgrest import APIResponse

from app.bases.user import UserBase


class UserCrud(UserBase, ABC):

    def __init__(self, supabase_client):
        self.client = supabase_client
        self.table = self.client.table("users")

    def create_user(self, nickname: str) -> dict:
        res: APIResponse = self.table.insert({"nickname": nickname}).execute()
        if not res.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Supabase 유저 기록 생성에 실패했습니다.",
            )
        return res.data[0]

    def read_user_by_nickname(self, nickname: str) -> dict:
        res: APIResponse = (
            self.table.select("*").eq("nickname", nickname).execute()
        )
        if not res.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="등록되지 않은 유저닉네임입니다.",
            )
        return res.data[0]
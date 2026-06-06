from fastapi import APIRouter
from app.services.farming_service import FarmingService

router = APIRouter()


@router.get("/{nickname}")
def get_logs(nickname: str):
    return FarmingService.get_logs(nickname)


@router.post("/log")
def add_log(data: dict):
    return FarmingService.create_log(data)
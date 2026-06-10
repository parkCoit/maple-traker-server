from fastapi import APIRouter, Query
from typing import Optional
from app.services.farming_service import FarmingService
from app.schemas.farming import FarmingResponse

router = APIRouter()


@router.get("/{nickname}", response_model=FarmingResponse)
def get_logs(nickname: str, year: Optional[int] = Query(None), month: Optional[int] = Query(None)):
    logs = FarmingService.get_logs(nickname) or []

    if year is not None and month is not None:
        filtered = []
        from datetime import datetime

        for log in logs:
            try:
                dt = datetime.strptime(log.get("date", ""), "%Y-%m-%d")
            except Exception:
                continue
            if dt.year == year and dt.month == month:
                filtered.append(log)
        logs = filtered

    summary = FarmingService.build_farming_summary(logs)

    return {
        "nickname": nickname,
        "summary": summary,
        "farming": logs,
    }



@router.post("/log")
def add_log(data: dict):
    return FarmingService.create_log(data)
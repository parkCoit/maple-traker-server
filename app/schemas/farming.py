from pydantic import BaseModel
from datetime import date
from typing import List


class FarmingLog(BaseModel):
    nickname: str
    date: date
    stuff: int
    meso_man: int
    frags: int
    gems: int
    f_price: int
    g_price: int
    level: int | None = None
    exp_pct: float | None = None
    # computed fields (raw meso units)
    meso: int | None = None
    total_meso: int | None = None


class FarmingSummary(BaseModel):
    today_total: int
    week_total: int
    month_total: int


class FarmingResponse(BaseModel):
    nickname: str
    summary: FarmingSummary
    farming: List[FarmingLog]
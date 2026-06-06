from pydantic import BaseModel
from datetime import date


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
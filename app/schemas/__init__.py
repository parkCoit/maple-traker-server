from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FarmingLogCreate(BaseModel):
    """사냥 기록 생성 스키마"""
    nickname: str
    date: str  # YYYY-MM-DD
    level: int
    exp_pct: float
    material: int
    meso: float
    fragments: int
    gems: int
    fragment_price: float
    gem_price: float


class FarmingLogUpdate(BaseModel):
    """사냥 기록 수정 스키마"""
    material: Optional[int] = None
    meso: Optional[float] = None
    fragments: Optional[int] = None
    gems: Optional[int] = None
    fragment_price: Optional[float] = None
    gem_price: Optional[float] = None


class FarmingLogResponse(BaseModel):
    """사냥 기록 응답 스키마"""
    id: int
    nickname: str
    date: str
    level: int
    exp_pct: float
    material: int
    meso: float
    fragments: int
    gems: int
    fragment_price: float
    gem_price: float
    total_revenue: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BossLogCreate(BaseModel):
    """보스 기록 생성 스키마"""
    nickname: str
    boss_name: str
    difficulty: str
    price: float
    date: str  # YYYY-MM-DD


class BossLogUpdate(BaseModel):
    """보스 기록 수정 스키마"""
    boss_name: Optional[str] = None
    difficulty: Optional[str] = None
    price: Optional[float] = None


class BossLogResponse(BaseModel):
    """보스 기록 응답 스키마"""
    id: int
    nickname: str
    boss_name: str
    difficulty: str
    price: float
    date: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AuthVerify(BaseModel):
    """인증 확인 요청"""
    nickname: str
    password: str


class AuthVerifyResponse(BaseModel):
    """인증 확인 응답"""
    valid: bool
    message: str = "Access granted"

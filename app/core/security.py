from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from zoneinfo import ZoneInfo
from app.core.config import settings

JWT_SECRET = settings.JWT_SECRET
ALGORITHM = settings.ALGORITHM
KST = ZoneInfo("Asia/Seoul")


def create_token(data: dict):
    payload = data.copy()

    expire = datetime.now(KST) + timedelta(days=7)
    payload.update({"exp": int(expire.timestamp())})

    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except JWTError:
        return None
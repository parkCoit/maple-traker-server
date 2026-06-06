# Maple Tracker - Server (FastAPI)

FastAPI + SQLAlchemy 기반의 Maple Tracker 백엔드 서버입니다.

## 프로젝트 구조

```
server/
├── app/
│   ├── api/                 # API 엔드포인트
│   │   ├── auth.py         # 인증 API
│   │   ├── farming.py      # 사냥 기록 API
│   │   └── boss.py         # 보스 기록 API
│   ├── models/             # SQLAlchemy 모델
│   ├── schemas/            # Pydantic 스키마
│   ├── db/                 # 데이터베이스 설정
│   └── utils/              # 유틸리티 함수
├── main.py                 # FastAPI 앱 진입점
├── requirements.txt        # 파이썬 패키지
├── .env                    # 환경 변수
└── venv/                   # 가상 환경
```

## 설치 및 실행

### 1. 가상 환경 설정

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정 (.env)

```env
DATABASE_URL=sqlite:///./maple_tracker.db
DEBUG=True
ACCESS_PASSWORD=도류도  # 접속 암호
MAPLE_API_KEY=your_api_key_here
```

### 4. 서버 실행

```bash
uvicorn main:app --reload
```

서버가 `http://localhost:8000`에서 실행됩니다.

## API 문서

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 주요 API 엔드포인트

### 인증

- `POST /api/auth/verify` - 접속 암호 확인
- `GET /api/auth/user/{nickname}` - 사용자 정보 조회

### 사냥 기록

- `POST /api/farming` - 사냥 기록 생성
- `GET /api/farming/{nickname}` - 사냥 기록 조회
- `GET /api/farming/{nickname}/{date}` - 특정 날짜 기록 조회
- `PUT /api/farming/{log_id}` - 사냥 기록 수정
- `DELETE /api/farming/{log_id}` - 사냥 기록 삭제
- `GET /api/farming/{nickname}/stats/{year}/{month}` - 월간 통계

### 보스 기록

- `POST /api/boss` - 보스 기록 생성
- `GET /api/boss/{nickname}` - 보스 기록 조회
- `GET /api/boss/{nickname}/weekly/{start_date}` - 주간 기록 조회
- `PUT /api/boss/{log_id}` - 보스 기록 수정
- `DELETE /api/boss/{log_id}` - 보스 기록 삭제
- `GET /api/boss/{nickname}/stats/{year}/{month}` - 월간 통계

## 데이터베이스

SQLite를 기본으로 사용합니다. 프로덕션 환경에서는 PostgreSQL 등의 데이터베이스로 변경 권장합니다.

### 테이블 구조

**farming_logs** - 사냥 기록

- id, nickname, date, level, exp_pct, material, meso, fragments, gems, fragment_price, gem_price, total_revenue

**boss_logs** - 보스 기록

- id, nickname, boss_name, difficulty, price, date

**user_accounts** - 사용자 계정

- id, nickname, password, is_active

## 개발 가이드

### 새로운 모델 추가

1. `app/models/__init__.py`에 SQLAlchemy 모델 정의
2. `app/schemas/__init__.py`에 Pydantic 스키마 정의
3. `app/api/` 폴더에 새 라우터 파일 생성
4. `app/api/__init__.py`에 라우터 등록

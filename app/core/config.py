from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # Password
    ACCESS_PASSWORD: str

    # Api key
    MAPLE_API_KEY: str

    # Jwt
    ALGORITHM: str
    JWT_SECRET: str

    # Url
    ID_URL: str
    BASIC_URL: str
    STAT_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
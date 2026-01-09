from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "auth-service"
    port: int = 8001

    jwt_secret: str = "super-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 60

    database_url: str = "sqlite:///./auth.db"

    class Config:
        env_file = ".env"


settings = Settings()

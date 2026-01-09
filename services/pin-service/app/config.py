from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "pin-service"
    port: int = 8002

    # local dev fallback
    database_url: str = "sqlite:///./pins.db"

    class Config:
        env_file = ".env"


settings = Settings()

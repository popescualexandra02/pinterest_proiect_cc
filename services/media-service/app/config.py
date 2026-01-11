from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "media-service"
    port: int = 8005
    upload_dir: str = "uploads"

    class Config:
        env_file = ".env"


settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "board-service"
    port: int = 8003
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()

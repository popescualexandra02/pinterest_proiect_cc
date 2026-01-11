from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "user-service"
    port: int = 8004
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()

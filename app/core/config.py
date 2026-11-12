from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CloudOps Task Manager"
    environment: str = "development"

    database_url: str = (
        "postgresql+psycopg://postgres:1234567890"
        "@localhost:5432/cloudops_db"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
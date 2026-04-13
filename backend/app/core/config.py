from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Apriori Engine API"
    app_env: str = "development"
    debug: bool = False
    # Default dev: SQLite agar backend bisa langsung jalan tanpa setup PostgreSQL.
    # Untuk production/real DB, override via .env.
    database_url: str = "sqlite:///./apriori_local.db"
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

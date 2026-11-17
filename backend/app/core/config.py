from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "DataPulse"
    environment: str = "development"
    secret_key: str = "local-development-only-change-me"
    database_url: str = "sqlite:///./datapulse.db"
    cors_origins: str = "http://localhost:5173"
    data_dir: str = "./data"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

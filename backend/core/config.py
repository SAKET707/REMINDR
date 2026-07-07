from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GROQ_API_KEY: str 
    TELEGRAM_BOT_TOKEN: str 
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    APP_NAME: str = "REMINDR"
    ENVIRONMENT: str = "development"
    FRONTEND_URL: str
    FERNET_KEY: str
    GMAIL_TOPIC: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
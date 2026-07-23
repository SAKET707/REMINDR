from pydantic_settings import BaseSettings, SettingsConfigDict

# configuration is centralised at one place no need to read env again n agian give type conversions
# validate reqd variable and fails fast if config is missing
# basesetting helps pydantic read from render secrets, env file , defaults 

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
    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore", #ignore extra things in .env if any 
    )


settings = Settings()

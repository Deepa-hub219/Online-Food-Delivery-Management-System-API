from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ===========================
    # APPLICATION
    # ===========================
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    # ===========================
    # DATABASE
    # ===========================
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # ===========================
    # JWT
    # ===========================
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
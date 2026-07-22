from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    secret_key: str
    algorithm: str

    ACCESS_TOKEN_EXPIRE_HOURS: int = 24

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    def get_database_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    GITHUB_TOKEN: str
    OPENAI_API_KEY: str
    
    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "CodeReviewAI"
    
    # Додаємо змінну середовища
    ENVIRONMENT: str = "development"
    
    # Налаштування залежно від середовища
    @property
    def redis_url(self) -> str:
        if self.ENVIRONMENT == "production":
            return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
        return "redis://localhost:6379"
    
    model_config = ConfigDict(env_file=".env")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
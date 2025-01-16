from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, constr, field_validator
from app.models.review import Review
from app.services.github_service import GitHubService
from app.services.openai_service import OpenAIService
from app.services.redis_service import RedisService
import re
import logging

router = APIRouter()

# Ініціалізація сервісів
github_service = GitHubService()
openai_service = OpenAIService()
redis_service = RedisService()

# Налаштування логування
logging.basicConfig(level=logging.INFO)

class ReviewRequest(BaseModel):
    assignment_description: constr(min_length=1)
    github_repo_url: str
    candidate_level: str

    @field_validator('candidate_level')
    @classmethod
    def validate_candidate_level(cls, v):
        if v not in ['Junior', 'Middle', 'Senior']:
            raise ValueError('Invalid candidate level. Must be Junior, Middle, or Senior.')
        return v

    @field_validator('github_repo_url')
    @classmethod
    def validate_github_url(cls, v):
        regex = r'^(https?://)?(www\.)?(github\.com/)([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)$'
        if not re.match(regex, v):
            raise ValueError('Invalid GitHub repository URL')
        return v

@router.post("/review")
async def review_code(request: ReviewRequest):
    try:
        # Спробувати отримати результат з кешу
        cache_key = f"review:{request.github_repo_url}:{request.candidate_level}"
        await redis_service.connect()  # Додано підключення до Redis
        cached_result = await redis_service.get(cache_key)
        
        if cached_result:
            await redis_service.disconnect()  # Закриваємо з'єднання
            return Review(content=cached_result)
        
        # Якщо немає в кеші, виконати аналіз
        contents = github_service.get_repo_contents(request.github_repo_url)
        code = "\n".join([content.decoded_content.decode() for content in contents if content.type == "file"])
        review_result = await openai_service.analyze_code(code, request.assignment_description, request.candidate_level)
        
        # Зберегти результат в кеші
        await redis_service.set(cache_key, review_result, expire=3600)  # кешувати на 1 годину
        await redis_service.disconnect()  # Закриваємо з'єднання
        
        return Review(content=review_result)
    except Exception as e:
        logging.error(f"Error processing review request: {str(e)}")
        if redis_service:
            await redis_service.disconnect()  # Закриваємо з'єднання у випадку помилки
        raise HTTPException(status_code=500, detail="Internal server error")

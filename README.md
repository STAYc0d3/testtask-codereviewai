# CodeReviewAI

AI-powered code review tool for analyzing GitHub repositories.

## Features
- Automated code review using OpenAI GPT
- GitHub repository analysis
- Redis caching for improved performance
- Support for different candidate levels (Junior, Middle, Senior)

## Installation
1. Clone the repository
2. Install dependencies: `poetry install`
3. Create `.env` file with required environment variables
4. Run Redis: `docker-compose up -d`
5. Start the server: `poetry run uvicorn app.main:app --reload`

## Usage
Send POST request to `/api/v1/review` with:
- assignment_description: string
- github_repo_url: string
- candidate_level: string (Junior/Middle/Senior)

## Testing
Run tests with: `poetry run pytest`

## Scaling Challenges and Solutions

Як масштабувати систему для обробки великої кількості запитів та великих репозиторіїв? Ось моє бачення:

**Архітектура зараз**:
- Клієнт -> FastAPI -> GitHub API/OpenAI API -> Redis (кеш)

**Архітектура для масштабування**:
- Клієнт -> Nginx (балансувальник) -> Кілька FastAPI серверів -> RabbitMQ -> Celery воркери -> Redis

### 1. Обробка багатьох запитів (100+ на хвилину)
- **Кешування результатів**: Використовуємо Redis для зберігання результатів аналізу. Якщо хтось запитує аналіз того самого репозиторію, то беремо готовий результат з кешу.
- **Черга завдань**: Замість обробки всіх запитів одразу, складаємо їх у чергу (наприклад, RabbitMQ).
- **Кілька серверів**: Запускаємо копії застосунку на різних серверах, щоб розподілити навантаження.

### 2. Робота з великими репозиторіями (100+ файлів)
- **Розумне кешування**: Зберігаємо вміст репозиторію в кеші на деякий час, щоб не завантажувати його знову при повторних запитах.
- **Поетапний аналіз**: Розбиваємо великі репозиторії на частини і аналізуємо їх поступово.
- **Обмеження розміру**: Можемо встановити розумні обмеження на розмір репозиторію або кількість файлів для аналізу.

### 3. Робота з API лімітами
- **GitHub API**: 
  - Кешуємо результати запитів
  - Використовуємо кілька токенів доступу
  - Додаємо затримки між запитами при досягненні лімітів

- **OpenAI API**:
  - Оптимізуємо запити для економії токенів
  - Кешуємо часто запитувані аналізи
  - Встановлюємо ліміти на кількість запитів
from openai import AsyncOpenAI
from app.core.config import get_settings
import logging
from fastapi import HTTPException

class OpenAIService:
    def __init__(self):
        self.settings = get_settings()
        self.client = AsyncOpenAI(api_key=self.settings.OPENAI_API_KEY)

    async def analyze_code(self, code: str, description: str, candidate_level: str):
        prompt = f"""
        Evaluate the following code for a {candidate_level} level candidate. Focus on code quality, best practices, maintainability, performance, readability, and use of relevant technologies.

        Assignment Description: 
        {description}

        Code: 
        {code}

        Provide your analysis in this format:
        1. **Files Analyzed**: List files and their apparent purpose.
        2. **Strengths**: Key positives, such as clean structure, good practices, or effective use of tools.
        3. **Downsides**: Issues like bugs, inefficiencies, poor design, or lack of documentation.
        4. **Suggestions**: Specific recommendations to address issues or improve the code.
        5. **Rating**: Score out of 10 based on {candidate_level} expectations.
        6. **Conclusion**: Summarize performance, strengths, and areas for growth.

        Keep the response detailed, actionable, and constructive.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"OpenAI API error: {str(e)}")
            raise HTTPException(status_code=503, detail="AI service temporarily unavailable")

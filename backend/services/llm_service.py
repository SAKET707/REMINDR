from groq import Groq

from core.config import settings


class LLMService:

    _client = Groq(
        api_key=settings.GROQ_API_KEY
    )

    @staticmethod
    def chat(
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float = 0,
    ) -> str:

        response = LLMService._client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        content = response.choices[0].message.content.strip()

        if content.startswith("```json"):
            content = content[len("```json"):].strip()

        if content.startswith("```"):
            content = content[len("```"):].strip()

        if content.endswith("```"):
            content = content[:-3].strip()

        return content
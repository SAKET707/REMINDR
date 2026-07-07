import json

from prompts.filter import FILTER_SYSTEM_PROMPT
from services.llm_service import LLMService


class FilterService:

    MODEL = "llama-3.1-8b-instant"

    @staticmethod
    def should_continue(
        subject: str,
        body: str,
    ) -> bool:

        user_prompt = f"""
        Subject:
        {subject}

        Body:
        {body}
        """

        try:

            response = LLMService.chat(
                system_prompt=FILTER_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                model=FilterService.MODEL,
                temperature=0,
            )

            result = json.loads(response)

            return bool(
                result.get(
                    "continue_processing",
                    True,
                )
            )

        except Exception as e:

            print(f"FilterService Error: {e}")

            # Fail safe.
            # Never ignore an email because the model failed.
            return True
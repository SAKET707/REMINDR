import json
from datetime import datetime

from prompts.analysis import ANALYSIS_SYSTEM_PROMPT
from services.llm_service import LLMService


class AnalysisService:

    MODEL = "llama-3.3-70b-versatile"

    @staticmethod
    def analyze(
        subject: str,
        body: str,
        received_at: datetime,
        likely_spam: bool,
    ) -> dict:

        user_prompt = f"""
        Email Received At (UTC):
        {received_at.isoformat()}

        Subject:
        {subject}

        Body:
        {body}

        Traditional ML Spam Classifier

        Likely Spam:
        {likely_spam}

        This is only a supporting weak signal.
        Do not rely on it exclusively.
        """

        response = LLMService.chat(
            system_prompt=ANALYSIS_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            model=AnalysisService.MODEL,
            temperature=0,
        )

        return json.loads(response)
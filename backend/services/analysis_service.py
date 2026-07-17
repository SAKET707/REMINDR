import json
from datetime import datetime

from prompts.analysis import ANALYSIS_SYSTEM_PROMPT
from services.llm_service import LLMService
# this converts raw email to structured data

class AnalysisService:

    MODEL = "llama-3.3-70b-versatile" # this task requires reasoning and summarising and understanding time related things like deadlines, reminder time etc so need good model

    @staticmethod
    def analyze(
        subject: str,
        body: str,
        received_at: datetime, # if mail says relatively like tommorrow, or 5 days later, model calculates the deadline or action date
    ) -> dict:
        
        # iso 8601 is universal 2026-07-15T10:20:00+00:00 easy for llm and unambiguous
        user_prompt = f"""
        Email Received At (UTC):
        {received_at.isoformat()} 

        Subject:
        {subject}

        Body:
        {body}
        """

        response = LLMService.chat(
            system_prompt=ANALYSIS_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            model=AnalysisService.MODEL,
            temperature=0,
        )

        return json.loads(response)
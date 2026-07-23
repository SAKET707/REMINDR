from langgraph.prebuilt import create_react_agent

from prompts.preparation import PREPARATION_SYSTEM_PROMPT
from services.llm_service import LLMService
from tools.preparation_tools import get_existing_tasks_tool


class PreparationAgent:

    MODEL="gemini-2.5-flash"

    @staticmethod
    def build(db):
        llm = LLMService.get_gemini_llm(
            model=PreparationAgent.MODEL,
            temperature=0,
        )

        tools = [
            get_existing_tasks_tool(db),
        ]

        return create_react_agent(
            model=llm,
            tools=tools,
            prompt=PREPARATION_SYSTEM_PROMPT,
        )
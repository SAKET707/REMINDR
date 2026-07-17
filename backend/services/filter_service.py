import json
# the job of this file is to filter non worthy emails to reach the analysis service becos these are not supposed to make a reminder for user
# that would be waste of tokens , money, latency 
# it decides then either continue or ignore
from prompts.filter import FILTER_SYSTEM_PROMPT
from services.llm_service import LLMService


class FilterService:

    MODEL = "llama-3.1-8b-instant" # easy task no huge model reqd for binary decision

    @staticmethod
    def should_continue(
        subject: str,
        body: str,
        likely_spam: bool,
    ) -> bool:

        user_prompt = f"""
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

        try:

            response = LLMService.chat( # we made this so that filterservice dont need to know how to talk to llms & returns str
                system_prompt=FILTER_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                model=FilterService.MODEL,
                temperature=0,
            )

            result = json.loads(response) # parse and get dict

            return bool(
                result.get(
                    "continue_processing",
                    True,
                ) # if llm forgot to put this key , then default is True , no crash
            )

        except Exception as e:

            print(f"FilterService Error: {e}")

            # Fail safe design.
            # Never ignore an email because the model failed.
            return True
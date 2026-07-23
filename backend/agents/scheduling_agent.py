import json
from datetime import datetime, timezone
from tools.scheduling_tools import TOOLS, AVAILABLE_TOOLS
from prompts.scheduling import SCHEDULING_SYSTEM_PROMPT
from services.llm_service import LLMService

import logging
logger = logging.getLogger(__name__)


class SchedulingAgent:

    MODEL = "llama-3.3-70b-versatile"

    @staticmethod
    def run(db, email) -> datetime:
        """
        Decides the best reminder time for an email.
        Returns a Python datetime.
        """
        current_time = datetime.now(timezone.utc)
        messages = [
            {
                "role": "system",
                "content": SCHEDULING_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": (
                    f"Current UTC Time: {current_time.isoformat()}\n"
                    f"User ID: {email.user_id}\n"
                    f"Summary: {email.summary}\n"
                    f"Deadline: "
                    f"{email.deadline.isoformat() if email.deadline else 'None'}"
                ),
            },
        ]

        logger.info(
            "Scheduling reminder for email_id=%d",
            email.id,
        )

        try:

            # Maximum two reasoning iterations
            for _ in range(2):

                response = LLMService.complete(
                    messages=messages,
                    model=SchedulingAgent.MODEL,
                    temperature=0,
                    tools=TOOLS,
                )

                message = response.choices[0].message

                # Final answer
                if not message.tool_calls:

                    result = json.loads(message.content)

                    scheduled_for = datetime.fromisoformat(
                        result["scheduled_for"]
                    )

                    logger.info(
                        "Scheduling agent selected %s (reason=%r)",
                        scheduled_for.isoformat(),
                        result.get("reason", ""),
                    )

                    return scheduled_for

                # Save assistant response containing tool call
                messages.append(message)

                # Execute every requested tool
                for tool_call in message.tool_calls:

                    function_name = tool_call.function.name

                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                    logger.info(
                        "Scheduling agent called tool %s",
                        function_name,
                    )

                    tool = AVAILABLE_TOOLS.get(function_name)

                    if tool is None:
                        raise ValueError(
                            f"Unknown tool requested: {function_name}"
                        )

                    tool_result = tool(
                        db=db,
                        **arguments,
                    )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_result,
                        }
                    )
                    messages.append(
                        {
                            "role": "system",
                            "content": (
                                "You have now received all the information required "
                                "to make the scheduling decision. "
                                "Do not call any more tools. "
                                "Return only the final JSON response."
                            ),
                        }
                    )

            raise RuntimeError(
                "Scheduling agent exceeded maximum tool iterations."
            )

        except Exception:
            logger.exception(
                "Scheduling agent failed for email_id=%d",
                email.id,
            )
            raise
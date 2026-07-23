from agents.preparation_agent import PreparationAgent


class PreparationAIService:

    @staticmethod
    def generate(
        db,
        reminder_id: int,
        subject: str,
        summary: str,
        deadline,
    ) -> list[str]:

        agent = PreparationAgent.build(db)

        user_prompt = f"""
        Reminder Subject:
        {subject}

        Reminder Summary:
        {summary}

        Reminder Deadline:
        {deadline if deadline else "Not specified"}

        Reminder ID:
        {reminder_id}
        """

        response = agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        user_prompt,
                    )
                ]
            }
        )

        content = response["messages"][-1].content

        return [
            line.lstrip("-•* ").strip()
            for line in content.splitlines()
            if line.strip()
        ]
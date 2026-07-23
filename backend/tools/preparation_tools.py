from langchain.tools import tool


def get_existing_tasks_tool(db):

    @tool
    def get_existing_tasks(reminder_id: int) -> list[str]:
        """
       Return all existing preparation task titles for a reminder.
        """

        from models.preparation_task import PreparationTask

        reminder_id = int(reminder_id)

        tasks = (
            db.query(PreparationTask)
            .filter(PreparationTask.reminder_id == reminder_id)
            .order_by(PreparationTask.position)
            .all()
        )

        return [task.title for task in tasks]

    return get_existing_tasks
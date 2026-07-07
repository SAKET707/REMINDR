from models.email import Email


class EmailService:

    @staticmethod
    def create(
        db,
        user_id: int,
        parsed_email: dict,
        analysis: dict,
    ) -> Email:

        # Check if email already exists
        existing = (
            db.query(Email)
            .filter_by(
                gmail_message_id=parsed_email["gmail_message_id"]
            )
            .first()
        )

        if existing:
            return existing

        # Create new email
        email = Email(
            user_id=user_id,
            gmail_message_id=parsed_email["gmail_message_id"],
            thread_id=parsed_email["thread_id"],
            sender=parsed_email["sender"],
            subject=parsed_email["subject"],
            summary=analysis["summary"],
            deadline=analysis["deadline"],
            received_at=parsed_email["received_at"],
        )

        db.add(email)
        db.flush()
        db.refresh(email)

        return email
from models.email import Email
# convert python dictionary which has summary deadlien etc to postgresql row and push it there in emails table
# it needs to create rows in email table so it needs that model

class EmailService:

    @staticmethod
    def create(
        db, # this is the sqlalchemy session that every request gets a sesion
        user_id: int,
        parsed_email: dict,
        analysis: dict,
    ) -> Email:

        # Check if email already exists
        existing = (
            db.query(Email)
            .filter_by( # for equality comparisons
                gmail_message_id=parsed_email["gmail_message_id"]
            )
            .first()
        )

        if existing:
            return existing # here the service uses idempotency 
        # an operation is idempotent if performing it multiple times produces the same final result as performing it once

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

        db.add(email) # tells sqlalchemy to track this obj as we intend to insert it. It doesnt insert to postgresql
        db.flush() # we do flush not commit here becos, the obj lives in the session only and primary key may still be null like id becos postgresql will generate that only after flush 
                   # now postgresql generates the id and sqlalchemy update it instantly. 
                   # since it is not commited yet the transaction is still open therfore nothing is permanant yet
                   # Synchronize the SQLAlchemy Session with the database without ending the transaction.
                   # We use flush because later services immediately need email.id before the transaction is committed.
        db.refresh(email) # immediately requeries the database to update the attributes of a specific ORM object with its latest database persisted state 
                        # Give me the latest version of this row. Now Python and PostgreSQL are synchronized.
        return email # return the sqlalchemy orm object
    
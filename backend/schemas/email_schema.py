from pydantic import BaseModel, ConfigDict
# BaseModel is Pydantic's base class.
# It validates request/response data, performs type conversion,
# serializes objects to JSON and automatically generates OpenAPI docs.
# if there are no schemas but we return objects directly that may expose sensitive info 

class EmailSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) # SQLAlchemy queries return ORM objects, not dictionaries.
                                                    # from_attributes=True tells Pydantic to read object attributes
                                                    # (user.id, user.email, ...) instead of expecting a dict.
                                        # tells pydantic to read values from obj attributes instead of expecting a dictionary

    id: int
    sender: str
    subject: str
    summary: str



# SQLAlchemy Models-> Describe how data is stored in the database.
# Pydantic Schemas -> Describe how data enters and leaves the API.
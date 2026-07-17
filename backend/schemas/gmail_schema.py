from pydantic import BaseModel

# Represents the response returned by the Gmail Watch API.
# Provides validation, type safety and a structured API response.
class GmailWatchResponse(BaseModel): # we use this for validation, type safety. google returns a json of these 2 attributes
    history_id: str
    expiration: int
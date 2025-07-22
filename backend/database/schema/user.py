from pydantic import BaseModel

class UserSchema(BaseModel):
    """Model representing a user in the database."""
    _id: str  # Unique identifier for the user
    name: str  # Name of the user
from pydantic import BaseModel

class NewUser(BaseModel):
    username: str
    password: str
    name: str
    role: str = "user"  # Default role is 'user'
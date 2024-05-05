from pydantic import BaseModel


class User(BaseModel):
    id: int
    role: str
    email: str
    password: str
    name: str

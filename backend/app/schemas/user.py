from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    name: str | None
    is_superuser: bool


class UserCreateRequest(BaseModel):
    email: str
    name: str
    password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserUpdateRequest(BaseModel):
    email: str | None = None
    name: str | None = None

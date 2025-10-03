from typing import Optional
from pydantic import BaseModel

class UserCreateRequest(BaseModel):
    email: str
    username: str
    password: str

class UserUpdateRequest(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: int
    updated_at: int

from pydantic import BaseModel
from typing import Optional

# Schemas NOTE
class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteSchema(NoteBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

class NoteUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]

# Schemas USER
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int
    class Config:
        from_attributes = True

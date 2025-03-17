from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    document_type: Optional[str] = None
    document_number: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
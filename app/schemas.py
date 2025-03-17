from pydantic import BaseModel
from datetime import date
from typing import Optional, Any

class Response(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

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
    status: Optional[int] = 1

    model_config = {
        "from_attributes": True
    }

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
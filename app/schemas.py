from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    bith_date: str = None
    phone: str = None
    country: str = None
    city: str = None
    document_type: str = None
    document_number: str = None

    class Config:
        orm_mode = True
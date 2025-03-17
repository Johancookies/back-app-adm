from sqlalchemy import Column, Integer, String, Date, JSON, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OnboardingUsers(Base):
    __tablename__ = "onboarding_users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    birth_date = Column(Date)
    phone = Column(String(20))
    country = Column(String(100))
    city = Column(String(100))
    document_type = Column(String(50))
    document_number = Column(String(50))
    metadata = Column(JSON) 
    status = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
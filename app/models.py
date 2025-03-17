from sqlalchemy import Column, Integer, String, Date, JSON, TIMESTAMP, Float, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Onboarding(Base):
    __tablename__ = "onboardings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    status = Column(Integer, default=1)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    x_metadata = Column(JSON)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class OnboardingQuestions(Base):
    __tablename__ = "onboarding_questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)  # Changed from TEXT to String(255)
    type = Column(String(50))
    onboarding_id = Column(Integer, ForeignKey("onboardings.id"), nullable=False)
    x_metadata = Column(JSON)
    status = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class OnboardingOptions(Base):
    __tablename__ = "onboarding_options"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)  # Changed from TEXT to String(255)
    status = Column(Integer, default=1)
    question_id = Column(Integer, ForeignKey("onboarding_questions.id"), nullable=False)
    x_metadata = Column(JSON)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

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
    x_metadata = Column(JSON)
    status = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class OnboardingAnswers(Base):
    __tablename__ = "onboarding_answers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("onboarding_users.id"), nullable=False)
    onboarding_id = Column(Integer, ForeignKey("onboardings.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("onboarding_questions.id"), nullable=False)
    option_id = Column(Integer)
    answer_text = Column(String(255), nullable=False) 
    x_metadata = Column(JSON)
    status = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class OnboardingTransactions(Base):
    __tablename__ = "onboarding_transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("onboarding_users.id"), nullable=False)
    onboarding_id = Column(Integer, ForeignKey("onboardings.id"))
    plan_name = Column(String(50))
    total = Column(Float, nullable=False)
    payment_reference = Column(String(50))
    payment_status = Column(String(50))
    bank_name = Column(String(50))
    gateway_name = Column(String(100))
    gateway_response = Column(String(255))
    tokenization_id = Column(Integer, nullable=False)
    tokenization_source = Column(String(100))
    x_metadata = Column(JSON)
    status = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
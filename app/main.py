from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

# Configuración de la Base de Datos (¡IMPORTANTE: Ajusta esto con tu configuración real!)
# Asegúrate de haber instalado el conector de MySQL: pip install mysql-connector-python
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definición de los Modelos de la Base de Datos (Mapeo Objeto-Relacional)
class Onboarding(Base):
    __tablename__ = "onboardings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    status = Column(Boolean)
    title = Column(String(255))
    description = Column(Text)
    activation_type_id = Column(Integer)  # ForeignKey("activation_types.id") # Descomentar si tienes la tabla activation_types
    color_config = Column(String(255))
    allow_text_color_change = Column(Boolean)
    allow_popups = Column(Boolean)
    target_user_type_id = Column(Integer)  # ForeignKey("user_types.id") # Descomentar si tienes la tabla user_types

    questions = relationship("Question", back_populates="onboarding")  #  Relación con Question


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    type = Column(String(50))
    status = Column(Boolean)
    onboarding_id = Column(Integer, ForeignKey("onboardings.id"))  #  Clave foránea a Onboarding

    onboarding = relationship("Onboarding", back_populates="questions")  #  Relación con Onboarding
    options = relationship("QuestionOption", back_populates="question")


class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(Text)
    status = Column(Boolean)
    question_id = Column(Integer, ForeignKey("questions.id"))

    question = relationship("Question", back_populates="options")


#  Crear las tablas en la base de datos (Ejecutar solo una vez o cuando haya cambios en los modelos)
Base.metadata.create_all(bind=engine)

#  Modelos Pydantic para la validación de datos
class QuestionOptionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: str
    question_id: int


class QuestionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    type: str
    onboarding_id: Optional[int] = None  #  Agregamos onboarding_id


# Endpoint para obtener un Onboarding por ID
@app.get("/onboardings/{onboarding_id}")
async def get_onboarding(onboarding_id: int):
    db = SessionLocal()
    onboarding = db.query(Onboarding).filter(Onboarding.id == onboarding_id).first()

    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding not found")

    #  Las questions se cargan automáticamente gracias a la relación
    db.close()
    return onboarding  # FastAPI convertirá esto a JSON automáticamente


# Endpoint para crear una nueva opción de pregunta
@app.post("/question_options/")
async def create_question_option(question_option: QuestionOptionCreate):
    db = SessionLocal()

    # Verificar si la pregunta existe
    question = db.query(Question).filter(Question.id == question_option.question_id).first()
    if not question:
        db.close()
        raise HTTPException(status_code=400, detail="Question not found")

    #  Usa model_dump() en lugar de dict()
    db_question_option = QuestionOption(**question_option.model_dump())
    db.add(db_question_option)
    db.commit()
    db.refresh(db_question_option)  # Recargar para obtener el ID generado por la base de datos
    db.close()
    return db_question_option


# Endpoint para crear una nueva pregunta
@app.post("/questions/")
async def create_question(question: QuestionCreate):
    db = SessionLocal()

    #  Usa model_dump()
    db_question = Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    db.close()
    return db_question


# Endpoint para obtener una Question por ID con sus QuestionOptions
@app.get("/questions/{question_id}")
async def get_question_with_options(question_id: int):
    db = SessionLocal()
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    #  Las options se cargan automáticamente gracias a la relación
    db.close()
    return question
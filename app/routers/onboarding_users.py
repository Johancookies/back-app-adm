from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()

@router.get("/users/")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.OnboardingUser).all()
    return users
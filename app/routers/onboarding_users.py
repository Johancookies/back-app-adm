from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/user/", response_model=schemas.User)
def add_user(user: schemas.User, db: Session = Depends(get_db)):
    user = models.OnboardingUser(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/users/", response_model=list[schemas.User])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.OnboardingUser).all()
    return users
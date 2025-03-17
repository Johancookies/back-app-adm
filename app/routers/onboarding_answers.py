from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/answert/", response_model=schemas.Response)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = models.OnboardingUsers(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return schemas.Response(success=True, data=schemas.User.model_validate(db_user))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
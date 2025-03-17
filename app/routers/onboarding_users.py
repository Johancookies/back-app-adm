from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/users/", response_model=schemas.Response)
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

@router.get("/users/", response_model=schemas.Response)
def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(models.OnboardingUsers).all()
        return schemas.Response(success=True, data=[schemas.User.model_validate(user) for user in users]) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}", response_model=schemas.Response)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.OnboardingUsers).filter(models.OnboardingUsers.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return schemas.Response(success=True, data=schemas.User.model_validate(db_user)) 
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/users/{user_id}", response_model=schemas.Response)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.OnboardingUsers).filter(models.OnboardingUsers.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return schemas.Response(success=True, data=schemas.User.model_validate(db_user)) 
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/users/{user_id}", response_model=schemas.Response)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.OnboardingUsers).filter(models.OnboardingUsers.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        setattr(db_user, models.OnboardingUsers.status, 0)
        db.commit()
        return schemas.Response(success=True, data={"message": "User deleted"})
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
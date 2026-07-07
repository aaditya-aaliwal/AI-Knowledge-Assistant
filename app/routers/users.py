from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.post("", response_model=UserResponse)
def create_user(user: UserCreate , db: Session = Depends(get_db)):
    db_user = User(
    name=user.name,
    email=user.email,
    password=user.password
)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

    
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int , db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
        status_code=404,
        detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int ,updated_user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
        status_code=404,
        detail="User not found")

    db_user.name = updated_user.name
    db_user.email = updated_user.email
    db_user.password = updated_user.password

    db.commit()
    db.refresh(db_user)
    return db_user
        

@router.delete("/{user_id}")
def delete_user(user_id: int , db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
            raise HTTPException(
            status_code=404,
            detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {
    "message": "User deleted successfully"
}
        
   
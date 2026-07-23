from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models import User
from app.security import hash_password ,get_current_user,require_admin
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("", response_model=list[UserResponse])
def get_users(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return users


@router.post("", response_model=UserResponse)
def create_user(user: UserCreate , db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user is not None:
        raise HTTPException(
        status_code=400,
        detail="Email already registered")
    
    db_user = User(
    name=user.name,
    email=user.email,
    password=hash_password(user.password)
)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

    
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Admin can view any user
    if current_user.role == "admin":
        user = db.query(User).filter(User.id == user_id).first()

    # Normal user can view only their own profile
    else:
        user = db.query(User).filter(
            User.id == user_id,
            User.id == current_user.id
        ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    updated_user: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Admin can update any user
    if current_user.role == "admin":
        db_user = db.query(User).filter(User.id == user_id).first()

    # Normal user can update only their own profile
    else:
        db_user = db.query(User).filter(
            User.id == user_id,
            User.id == current_user.id
        ).first()

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_user = db.query(User).filter(
        User.email == updated_user.email
    ).first()

    if existing_user is not None and existing_user.id != user_id:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    db_user.name = updated_user.name
    db_user.email = updated_user.email
    db_user.password = hash_password(updated_user.password)

    db.commit()
    db.refresh(db_user)

    return db_user
        

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(db_user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }
        
   
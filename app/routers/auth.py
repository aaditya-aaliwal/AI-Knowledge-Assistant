from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models import User
from app.security import verify_password ,create_access_token ,get_current_user ,create_refresh_token ,verify_access_token
from app.schemas.auth import Token , RefreshTokenRequest
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserResponse


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login", response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.username).first()

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token(
    {
        "sub": str(db_user.id),
        "email": db_user.email,
        "type": "access"
    }
)

    refresh_token = create_refresh_token(
    {
        "sub": str(db_user.id),
        "email": db_user.email,
        "type": "refresh"
    }
)
    return {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer"
}


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh: RefreshTokenRequest
):
    payload = verify_access_token(
    refresh.refresh_token,
    token_type="refresh")

    user_id = payload.get("sub")
    email = payload.get("email")

    access_token = create_access_token(
        {
            "sub": user_id,
            "email": email,
            "type": "refresh"
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh.refresh_token,
        "token_type": "bearer"
    }
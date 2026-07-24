from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models import Chat,User
from app.schemas.chat import ChatCreate, ChatResponse
from app.security import get_current_user

router = APIRouter(
    prefix="/chats",
    tags=["Chats"]
)


@router.get("", response_model=list[ChatResponse])
def get_chats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chats = db.query(Chat).filter(Chat.user_id == current_user.id).all()
    return chats


@router.post("", response_model=ChatResponse)
def create_chat(
    chat: ChatCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_chat = Chat(
    title=chat.title,
    user_id=current_user.id
)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(chat_id: int , current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(
    Chat.id == chat_id,
    Chat.user_id == current_user.id).first()
    if chat is None:
        raise HTTPException(
        status_code=404,
        detail="Chat not found")
    return chat


@router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(
    chat_id: int,
    updated_chat: ChatCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()

    if db_chat is None:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    db_chat.title = updated_chat.title

    db.commit()
    db.refresh(db_chat)
    return db_chat


@router.delete("/{chat_id}")
def delete_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()

    if db_chat is None:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    db.delete(db_chat)
    db.commit()

    return {
        "message": "Chat deleted successfully"
    }
        
   
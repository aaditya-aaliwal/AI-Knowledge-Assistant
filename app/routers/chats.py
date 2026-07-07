from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models import Chat,User
from app.schemas.chat import ChatCreate, ChatResponse

router = APIRouter(
    prefix="/chats",
    tags=["Chats"]
)


@router.get("", response_model=list[ChatResponse])
def get_chats(db: Session = Depends(get_db)):
    chats = db.query(Chat).all()
    return chats


@router.post("", response_model=ChatResponse)
def create_chat(chat: ChatCreate , db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == chat.user_id).first()
    if user is None:
        raise HTTPException(
        status_code=404,
        detail="User not found")
    
    db_chat = Chat(
    title = chat.title,
    user_id=chat.user_id
)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(chat_id: int , db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(
        status_code=404,
        detail="Chat not found")
    return chat


@router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(chat_id: int ,updated_chat: ChatCreate, db: Session = Depends(get_db)):
    db_chat = db.query(Chat).filter(Chat.id == chat_id).first()
    db_user = db.query(User).filter(User.id == updated_chat.user_id).first()

    if db_chat is None:
        raise HTTPException(
        status_code=404,
        detail="Chat not found"
    )

    if db_user is None:
        raise HTTPException(
        status_code=404,
        detail="User not found")

    db_chat.title = updated_chat.title
    db_chat.user_id = updated_chat.user_id

    db.commit()
    db.refresh(db_chat)
    return db_chat


@router.delete("/{chat_id}")
def delete_chat(chat_id: int , db: Session = Depends(get_db)):
    db_chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if db_chat is None:
            raise HTTPException(
            status_code=404,
            detail="Chat not found")
    
    db.delete(db_chat)
    db.commit()
    return {
    "message": "Chat deleted successfully"
}
        
   
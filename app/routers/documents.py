from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models import Chat,Document
from app.schemas.document import DocumentCreate, DocumentResponse

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.get("", response_model=list[DocumentResponse])
def get_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return documents


@router.post("", response_model=DocumentResponse)
def create_document(document: DocumentCreate , db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == document.chat_id).first()
    if chat is None:
        raise HTTPException(
        status_code=404,
        detail="Chat not found")
    
    db_document = Document(
    filename = document.filename,
    content = document.content,
    chat_id=document.chat_id
)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int , db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        raise HTTPException(
        status_code=404,
        detail="Document not found")
    return document


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(document_id: int ,updated_document: DocumentCreate, db: Session = Depends(get_db)):
    db_document = db.query(Document).filter(Document.id == document_id).first()
    db_chat = db.query(Chat).filter(Chat.id == updated_document.chat_id).first()

    if db_document is None:
        raise HTTPException(
        status_code=404,
        detail="Document not found"
    )

    if db_chat is None:
        raise HTTPException(
        status_code=404,
        detail="Chat not found")

    db_document.filename = updated_document.filename
    db_document.content = updated_document.content
    db_document.chat_id = updated_document.chat_id

    db.commit()
    db.refresh(db_document)
    return db_document


@router.delete("/{document_id}")
def delete_document(document_id: int , db: Session = Depends(get_db)):
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if db_document is None:
            raise HTTPException(
            status_code=404,
            detail="Document not found")
    
    db.delete(db_document)
    db.commit()
    return {
    "message": "Document deleted successfully"
}
        
   
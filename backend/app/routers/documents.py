from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.database import get_db
from app.models import Chat,Document
from app.schemas.document import DocumentCreate, DocumentResponse
from app.security import get_current_user
from app.models import User

from pathlib import Path
import shutil
from app.logger import logger

from app.dependencies import get_document_ingestion_service
from app.services.document_ingestion_service import DocumentIngestionService

from app.messaging.producer import producer

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)



from app.logger import logger


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    document_ingestion_service: DocumentIngestionService = Depends(
        get_document_ingestion_service,
    ),
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    file_path = Path("uploads") / file.filename

    try:
        Path("uploads").mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        upload_chat = db.query(Chat).filter(
            Chat.user_id == current_user.id,
            Chat.title == "Uploads",
        ).first()
        if upload_chat is None:
            upload_chat = Chat(title="Uploads", user_id=current_user.id)
            db.add(upload_chat)
            db.flush()

        db_document = Document(
            filename=file.filename,
            content=str(file_path),
            filepath=str(file_path),
            uploaded_by=current_user.id,
            status="UPLOADING",
            chat_id=upload_chat.id,
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)

        logger.info("Publishing message to RabbitMQ...")

        producer.publish(
            {
                "file_path": str(file_path),
                "filename": file.filename,
                "document_id": db_document.id,
            }
        )
        db_document.status = "PROCESSING"
        db.commit()

        logger.info("RabbitMQ message published successfully.")

        logger.info(
            f"Successfully uploaded document: {file.filename}"
        )

        return {
            "message": "Document uploaded successfully.",
            "filename": file.filename,
            "document": DocumentResponse.model_validate(db_document).model_dump(mode="json"),
        }

    except Exception:
        db.rollback()
        logger.exception(
            f"Failed to upload document: {file.filename}"
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to upload document.",
        )

    finally:
        file.file.close()




@router.get("", response_model=list[DocumentResponse])
def get_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    documents = (
        db.query(Document)
        .outerjoin(Chat)
        .filter(or_(Document.uploaded_by == current_user.id, Chat.user_id == current_user.id))
        .order_by(Document.created_at.desc())
        .all()
    )

    return documents


@router.post("", response_model=DocumentResponse)
def create_document(
    document: DocumentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = db.query(Chat).filter(
        Chat.id == document.chat_id,
        Chat.user_id == current_user.id
    ).first()

    if chat is None:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    db_document = Document(
        filename=document.filename,
        content=document.content,
        chat_id=chat.id
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return db_document


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    document = (
        db.query(Document)
        .join(Chat)
        .filter(
            Document.id == document_id,
            Chat.user_id == current_user.id
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: int,
    updated_document: DocumentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_document = (
        db.query(Document)
        .join(Chat)
        .filter(
            Document.id == document_id,
            Chat.user_id == current_user.id
        )
        .first()
    )

    if db_document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    db_document.filename = updated_document.filename
    db_document.content = updated_document.content

    db.commit()
    db.refresh(db_document)

    return db_document


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_document = (
        db.query(Document)
        .join(Chat)
        .filter(
            Document.id == document_id,
            Chat.user_id == current_user.id
        )
        .first()
    )

    if db_document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    db.delete(db_document)
    db.commit()

    return {
        "message": "Document deleted successfully"
    }

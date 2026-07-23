from pathlib import Path

from pypdf import PdfReader

from app.logger import logger


class PDFService:

    def extract_text(
        self,
        file_path: Path
    ) -> str:

        try:
            pdf_reader = PdfReader(file_path)

            text = ""

            for page in pdf_reader.pages:
                page_text = page.extract_text()

                text += page_text or ""

            return text

        except Exception:
            logger.exception(
                f"Failed to extract text from PDF: {file_path}"
            )
            raise
from pathlib import Path

from app.utils.excel_reader import ExcelReader
from app.utils.pdf_reader import PdfReader
from app.utils.doc_reader import DocReader
from app.utils.text_reader import TextReader
from app.utils.excel_doc_reader import Excel_Doc_Reader

from app.core.logger import logger


class AttachmentService:

    def __init__(self):    
        self.pdf_reader = PdfReader()
        self.excel_reader = Excel_Doc_Reader()
        self.text_reader = TextReader()
        self.docx_reader = DocReader()

    def exctract(self, attachment_path: str) -> str:
        try:
            path = Path(attachment_path)
            print(path)

            if not path.exists():
                logger.warning("Attachment mention on excel not available on desired location")
                return ""

            extension = path.suffix.lower()
            print(extension)
            if extension == ".pdf":
                return self.pdf_reader.read(path)
            elif extension == ".xlsx":
                return self.excel_reader.read(path)
            elif extension == ".docx":
                return self.docx_reader.read(path)
            elif extension == ".txt":
                return self.text_reader.read(path)
            else:
                logger.error("Un Supported File Path Found.")
                return ""
        except Exception as exc:

            logger.error(
                f"Attachment extraction failed: {exc}"
            )

            return ""
from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.services.compliance_service import ComplianceService
from app.core.logger import logger

router = APIRouter(
    prefix="/upload",
    tags=["Upload Excel file"]
)

UPLOAD_DIR = Path("Uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post(
    "/emails",
    summary="Upload Emails in excel file."
)
async def upload_email_excel(
    file: UploadFile = File(...)
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No File Selected"
        )
    if not file.filename.lower().endswith(".xlsx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not uploaded xlsx file"
        )

    file_path = UPLOAD_DIR/file.filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        compliance_service = ComplianceService()
        logger.info(f"got some info in buffer {buffer}")
        result = compliance_service.process_excel(
            excel_path=file_path
        )
        # logger.info(f"Compliance :: {result}")
        return {
            "status": "success",
            "file_name": file.filename,
            "total_records": len(result),
            "results": result
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Got some issue {exc}"
        )

    finally:
        file.file.close()

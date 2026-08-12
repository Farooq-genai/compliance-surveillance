from pathlib import Path

from app.utils.excel_reader import ExcelReader
from app.utils.email_parser import EmailParser
from app.agents.compliance_agent import ComplianceAgent
from app.core.logger import logger
from app.services.risk_score_calculator import RiskScoreCalculator
from app.repositories.email_repository import EmailRepository
from app.repositories.compliance_repository import ComplianceRepository
from app.database.dependencies import SessionLocal
from app.services.attachment_service import AttachmentService


class ComplianceService:
    """
    Orchestrates the compliance analysis workflow.

    Workflow:
        Excel -> Email Parser -> AI Agent -> Results
    """

    def __init__(self):
        self.excel_reader = ExcelReader()
        self.email_parser = EmailParser()
        self.compliance_agent = ComplianceAgent()
        self.risk_score_calculator = RiskScoreCalculator()
        self.email_repository = EmailRepository()
        self.compliance_repository = ComplianceRepository()
        self.attachment_service = AttachmentService()


    def process_excel(self, excel_path: Path) -> list:
        """
        Process an uploaded Excel file.

        Args:
            excel_path: Path to uploaded Excel file.

        Returns:
            List of AI analysis results.
        """
        print("excel_path", excel_path)
        excel_rows = self.excel_reader.read(excel_path)
        # print("excel_rows", excel_rows)
        results = []
        db = SessionLocal()
        try:
            print(f"excel_rows :: {excel_rows}")
            for index, row in enumerate(excel_rows, start=1):
                print(f"index :: {index}")
                attachments_text = ""
                attachments = eval(row.get("attachments"))
                if attachments and type(attachments) == type(["list"]):
                    # print(f"/n/n Attachments ? /n {attachments}")
                    for attachment in attachments:
                        # print(f"attachment :: \n \n {attachment}")
                        doc_text = (self.attachment_service.exctract(attachment))
                        # print(f"doc_text :: {doc_text}")
                        attachments_text += doc_text

                if attachments_text:
                    print(f"attachments_text :: {attachments_text}")
                    
                email = self.email_parser.parse(row, attachments_text)
                # print(f"email :: {email}")
                saved_email = self.email_repository.create(db, email)
                # logger.info(f"Complienace Service : saved_email _id {saved_email.id}")
                analysis = self.compliance_agent.analyze(email)
                
                risk_result = self.risk_score_calculator.calculate(analysis)
                final_analysis = {
                    **analysis, **risk_result,
                }
                saved_results = self.compliance_repository.create(db, saved_email.id, final_analysis)
                print(f"Saved Compliance id: {saved_results.id}")
                row_data = {
                        "email_id": index,
                        "expected_category": row.get("category"),
                        "expected_classification": row.get("classification"),
                        "email": email,
                        "analysis": final_analysis,
                    }
                print(f"row_data :: {row_data}")
                results.append(
                    row_data
                )
                
        except Exception as exc:
            logger.info(f"Process_Excel :: {exc}")

        finally:
            db.close()
        return results
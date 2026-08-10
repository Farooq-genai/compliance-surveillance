from pathlib import Path

from app.utils.excel_reader import ExcelReader
from app.utils.email_parser import EmailParser
from app.agents.compliance_agent import ComplianceAgent
from app.core.logger import logger
from app.services.risk_score_calculator import RiskScoreCalculator


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
        try:

            for index, row in enumerate(excel_rows, start=1):
                print(index)
                print(row)
                email = self.email_parser.parse(row)
                print("email_data, ----------------->", email)
                analysis = self.compliance_agent.analyze(email)
                print("Analysis data ---------------->\n\n\n\n\n", analysis)
                print(row.get("category"))
                print(row.get("classification"))

                risk_result = self.risk_score_calculator.calculate(analysis)
                final_analysis = {
                    **analysis, **risk_result,
                }
                results.append(
                    {
                        "email_id": index,
                        "expected_category": row.get("category"),
                        "expected_classification": row.get("classification"),
                        "email": email,
                        "analysis": final_analysis,
                    }
                )

        except Exception as exc:
            logger.info(f"Process_Excel :: {exc}")
        return results
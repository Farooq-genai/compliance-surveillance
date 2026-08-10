import re
from app.core.logger import logger

class EmailParser:
    """
    Parses raw email text into a structured dictionary.
    """
    REQUIRED_FIELDS = [
        "from",
        "to",
        "subject",
        "body"
    ]

    OPTIONAL_FIELDS = [
        "bcc", "cc"
    ]

    

    def parse(self, row: str) -> dict:

        email_text = row['email_text']
        
        if not email_text:
            return {}

        if not isinstance(email_text, str) or not email_text.strip():
            raise ValueError(
                f"Sample {row.get('sample_id')}: Email sample is EMPTY"
            )

        self._validate_required_fields(
            self=self,
            email_text=email_text,
            sample_id=row.get("sample_id")
        )

        return {
            "sample_id": row['sample_id'],
            "metadata": {
                "from": self._extract_field(email_text, "From"),
                "to": self._extract_field(email_text, "To"),
                "cc": self._extract_field(email_text, "Cc"),
                "bcc": self._extract_field(email_text, "Bcc"),
                "subject": self._extract_field(email_text, "Subject"),
            },
            "body": self._extract_body(email_text),
            "raw_email": email_text,
            "ground_truths": {
                "category": row['category'],
                "classification": row["classification"],
            }
        }
    

    @staticmethod
    def _extract_field(email_text: str, field: str):
        """
        Extract a header value.

        Example:
            Subject : Confidential Report
        """

        pattern = rf"{field}\s*:\s*(.*)"

        match = re.search(
            pattern,
            email_text,
            re.IGNORECASE
        )

        return match.group(1).strip() if match else ""

    # @staticmethod
    # def _extract_body(email_text: str):
    #     """
    #     Extract everything after Subject line.
    #     """

    #     lines = email_text.splitlines()

    #     body_started = False

    #     body = []

    #     for line in lines:

    #         if body_started:
    #             body.append(line)

    #         if re.match(r"^\s*Subject\s*:", line, re.IGNORECASE):
    #             body_started = True

    #     return "\n".join(body).strip()

    @staticmethod
    def _extract_body(email_text: str) -> str:
        """
        Extract the email body after the Body: marker.
        """

        match = re.search(
            r"^\s*Body\s*:\s*(.*)$",
            email_text,
            re.IGNORECASE | re.MULTILINE | re.DOTALL,
        )

        if not match:
            return ""

        return match.group(1).strip()

    @staticmethod
    def _validate_required_fields(self, email_text: str, sample_id: None):
        """
        validate that all mandetory email fields exists
        """

        missing_fields = []
        for field in self.REQUIRED_FIELDS:
            pattern = rf"^\s*{re.escape(field)}\s*"

            if not re.search(
                pattern, 
                email_text,
                re.IGNORECASE | re.MULTILINE
            ):
                missing_fields.append(field)

        if missing_fields:
            logger.info(f"Email Parser :: Row {sample_id} : Required Fields {", ".join(missing_fields)} missing..")
            raise ValueError(
                f"Sample {sample_id}: Missing Required Fields :: {", ".join(missing_fields)}"
            )

        
import re


class EmailParser:
    """
    Parses raw email text into a structured dictionary.
    """

    def parse(self, row: str) -> dict:

        email_text = row['email_text']
        
        if not email_text:
            return {}

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
    def _extract_field(email_text: str, field: str) -> str:
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

    @staticmethod
    def _extract_body(email_text: str) -> str:
        """
        Extract everything after Subject line.
        """

        lines = email_text.splitlines()

        body_started = False

        body = []

        for line in lines:

            if body_started:
                body.append(line)

            if re.match(r"^\s*Subject\s*:", line, re.IGNORECASE):
                body_started = True

        return "\n".join(body).strip()
from sqlalchemy.orm import Session

from app.models.email import Email


class EmailRepository:
    """
    Handles email table operations.
    """

    def create(
        self,
        db: Session,
        email_data: dict,
    ) -> Email:
        """
        Store normalized email data.
        """

        email = Email(
            sample_id=email_data.get(
                "sample_id"
            ),

            sender=email_data["metadata"]["from"],

            recipients=email_data["metadata"]["to"],

            cc=email_data["metadata"].get(
                "cc"
            ),

            bcc=email_data["metadata"].get(
                "bcc"
            ),

            subject=email_data["metadata"]["subject"],

            body=email_data["body"],

            raw_email=email_data["raw_email"],

            expected_category=email_data
            .get(
                "ground_truths",
                {}
            )
            .get(
                "category"
            ),

            expected_classification=email_data
            .get(
                "ground_truths",
                {}
            )
            .get(
                "classification"
            ),
        )

        db.add(email)

        db.commit()

        db.refresh(email)

        return email
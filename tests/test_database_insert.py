from app.database.database import SessionLocal
from app.repositories.email_repository import EmailRepository
from app.repositories.compliance_repository import ComplianceRepository


def test_email_and_result_insert():

    db = SessionLocal()

    email_repository = EmailRepository()
    compliance_repository = ComplianceRepository()


    email_data = {

        "sample_id": 100,

        "metadata": {
            "from": "test@company.com",
            "to": "user@company.com",
            "cc": "",
            "bcc": "",
            "subject": "Test Email",
        },

        "body": "This is a test email",

        "raw_email": "From:test@company.com",

        "ground_truths": {
            "category": "Secrecy",
            "classification": "True Positive",
        },
    }


    email = email_repository.create(
        db,
        email_data,
    )


    analysis = {

        "Outside_Party_Involved": True,

        "Sender": "test@company.com",

        "Is_Non_Compliance": True,

        "Categories": [
            "Secrecy"
        ],

        "Evidence": [
            "Do not share this"
        ],

        "Evidence_Strength": [
            "Direct Statement"
        ],

        "Confidence": 95,

        "Risk_Score": 3.75,

        "Priority": "Low",

        "Review_Required": False,

        "Review_Status": "No Review Required",

        "Summary": "Test",

        "Reason_For_Flagging": "Test",

        "Category_Risk_Details": []
    }


    result = compliance_repository.create(
        db,
        email.id,
        analysis,
    )


    assert email.id is not None
    assert result.email_id == email.id


    db.close()
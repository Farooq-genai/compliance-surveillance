import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.compliance_repository import ComplianceRepository
from app.repositories.email_repository import EmailRepository
from app.models.email import Email
from app.models.compliance_result import ComplianceResult


router = APIRouter(
    prefix="/compliance",
    tags=["Compliance"]
)


repository = ComplianceRepository()


@router.get("/results")
def get_compliance_results(
    db: Session = Depends(get_db)
):

    records = (
        db.query(
            ComplianceResult,
            Email.body.label("email_body")
        )
        .outerjoin(
            Email,
            Email.sample_id == ComplianceResult.email_id
        )
        .all()
    )

    response = []

    for item, email_body in records:

        response.append(
            {
                "id": item.id,

                "email_id": item.email_id,

                "outside_party_involved":
                    item.outside_party_involved,

                "is_non_compliance":
                    item.is_non_compliance,

                "sender":
                    item.sender,

                "categories":
                    json.loads(item.categories)
                    if item.categories else [],

                "evidence":
                    json.loads(item.evidence)
                    if item.evidence else [],

                "evidence_strength":
                    json.loads(item.evidence_strength)
                    if item.evidence_strength else [],

                "confidence":
                    item.confidence,

                "risk_score":
                    item.risk_score,

                "priority":
                    item.priority,

                "review_required":
                    item.review_required,

                "review_status":
                    item.review_status,

                "summary":
                    item.summary,

                "reason_for_flagging":
                    item.reason_for_flagging,

                "category_risk_details":
                    json.loads(item.category_risk_details)
                    if item.category_risk_details else [],

                "body":
                    email_body or "",
            }
        )

    return {
        "total": len(response),
        "results": response
    }
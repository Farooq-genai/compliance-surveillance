import json

from sqlalchemy.orm import Session

from app.models.compliance_result import ComplianceResult


class ComplianceRepository:


    def get_all(
        self,
        db: Session
    ):

        return (
            db.query(ComplianceResult)
            .order_by(
                ComplianceResult.created_at.desc()
            )
            .all()
        )
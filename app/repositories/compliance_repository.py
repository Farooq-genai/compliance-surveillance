import json

from sqlalchemy.orm import Session

from app.models.compliance_result import ComplianceResult


class ComplianceRepository:
    """
    Handles compliance result database operations.
    """


    def create(
        self,
        db: Session,
        email_id: int,
        analysis: dict,
    ) -> ComplianceResult:
        """
        Store AI analysis and risk calculation result.
        """


        result = ComplianceResult(

            email_id=email_id,

            outside_party_involved=
                analysis.get(
                    "Outside_Party_Involved",
                    False
                ),

            is_non_compliance=
                analysis.get(
                    "Is_Non_Compliance",
                    False
                ),

            sender=
                analysis.get(
                    "Sender",
                    ""
                ),

            categories=json.dumps(
                analysis.get(
                    "Categories",
                    []
                )
            ),

            evidence=json.dumps(
                analysis.get(
                    "Evidence",
                    []
                )
            ),

            evidence_strength=json.dumps(
                analysis.get(
                    "Evidence_Strength",
                    []
                )
            ),

            confidence=
                analysis.get(
                    "Confidence",
                    0
                ),

            risk_matrix=json.dumps(
                analysis.get(
                    "Risk_Matrix",
                    {}
                )
            ),

            risk_score=
                analysis.get(
                    "Risk_Score",
                    0
                ),

            priority=
                analysis.get(
                    "Priority",
                    "Low"
                ),

            review_required=
                analysis.get(
                    "Review_Required",
                    False
                ),

            review_status=
                analysis.get(
                    "Review_Status",
                    "No Review Required"
                ),

            summary=
                analysis.get(
                    "Summary"
                ),

            reason_for_flagging=
                analysis.get(
                    "Reason_For_Flagging"
                ),

            category_risk_details=json.dumps(
                analysis.get(
                    "Category_Risk_Details",
                    []
                )
            ),
        )


        db.add(result)

        db.commit()

        db.refresh(result)

        return result



    def get_all(
        self,
        db: Session
    ):
        """
        Fetch all compliance results.
        """

        return (
            db.query(ComplianceResult)
            .order_by(
                ComplianceResult.created_at.desc()
            )
            .all()
        )
    
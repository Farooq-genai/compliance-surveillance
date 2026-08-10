import json
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ComplianceResult(Base):

    __tablename__ = "compliance_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    email_id: Mapped[int] = mapped_column(
        ForeignKey("emails.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    outside_party_involved: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_non_compliance: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    sender: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    categories: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]",
    )

    evidence: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]",
    )

    evidence_strength: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]",
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0,
    )

    risk_matrix: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="{}",
    )

    risk_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0,
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Low",
    )

    review_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    review_status: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="No Review Required",
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    reason_for_flagging: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    category_risk_details: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    email = relationship(
        "Email",
        back_populates="compliance_result",
    )

    # ---------------------------------------------------------
    # JSON helper methods
    # ---------------------------------------------------------

    def get_categories(self) -> list:
        return json.loads(self.categories)

    def get_evidence(self) -> list:
        return json.loads(self.evidence)

    def get_evidence_strength(self) -> list:
        return json.loads(self.evidence_strength)

    def get_risk_matrix(self) -> dict:
        return json.loads(self.risk_matrix)

    def get_category_risk_details(self) -> list:
        return json.loads(self.category_risk_details)

    
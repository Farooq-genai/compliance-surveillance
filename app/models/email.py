from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Email(Base):

    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    sample_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    sender: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    recipients: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    cc: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    bcc: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    subject: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    body: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    raw_email: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    expected_category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    expected_classification: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    attachments = relationship(
        "EmailAttachment",
        back_populates="email",
        cascade="all, delete-orphan",
    )

    compliance_result = relationship(
        "ComplianceResult",
        back_populates="email",
        uselist=False,
        cascade="all, delete-orphan",
    )
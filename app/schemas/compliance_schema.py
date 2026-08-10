from pydantic import BaseModel
from typing import List, Any


class ComplianceResultResponse(BaseModel):

    id: int

    email_id: int

    outside_party_involved: bool

    is_non_compliance: bool

    sender: str

    categories: List[str]

    evidence: List[str]

    evidence_strength: List[str]

    confidence: float

    risk_score: float

    priority: str

    review_required: bool

    review_status: str

    summary: str | None

    reason_for_flagging: str | None

    category_risk_details: Any

    
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.risk_matrix_service import RiskMatrixService


router = APIRouter(
    prefix="/risk-matrix",
    tags=["Risk Matrix"]
)


service = RiskMatrixService()


class RiskUpdate(BaseModel):
    score: int


@router.get("/")
def get_risk_matrix():

    return service.get_matrix()



@router.put("/{category}")
def update_risk_matrix(
    category: str,
    request: RiskUpdate
):

    try:

        return service.update_score(
            category,
            request.score
        )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )
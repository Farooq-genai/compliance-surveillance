from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from app.services.risk_matrix_service import RiskMatrixService


router = APIRouter(
    prefix="/risk-matrix",
    tags=["Risk Matrix"]
)


service = RiskMatrixService()


class RiskMatrixUpdate(BaseModel):
    risk_matrix: Dict[str, int]


@router.get("/")
def get_risk_matrix():

    return service.get_matrix()



@router.put("/")
def update_risk_matrix(
    request: RiskMatrixUpdate
):

    try:

        return service.update_matrix(
            request.risk_matrix
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )
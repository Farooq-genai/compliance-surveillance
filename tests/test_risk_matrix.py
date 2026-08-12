from app.services.risk_matrix_service import RiskMatrixService


def test_get_risk_matrix():

    service = RiskMatrixService()

    matrix = service.get_matrix()

    print(matrix)

    assert "Market Manipulation" in matrix



def test_update_risk_score():

    service = RiskMatrixService()

    result = service.update_score(
        "Market Manipulation",
        20
    )

    assert result["Market Manipulation"] == 20
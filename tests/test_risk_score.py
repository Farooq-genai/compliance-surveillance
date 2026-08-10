from app.services.risk_score_calculator import RiskScoreCalculator


def test_market_manipulation_critical_risk():

    ai_result = {
        "Outside_Party_Involved": True,
        "Sender": "umarfarooq@tcs.com",
        "Is_Non_Compliance": True,
        "Categories": [
            "Market Manipulation"
        ],
        "Evidence": [
            "Please execute before public release."
        ],
        "Evidence_Strength": [
            "Direct Statement"
        ],
        "Confidence": 95,
    }

    calculator = RiskScoreCalculator()

    result = calculator.calculate(ai_result)

    print(result)

    assert result["Risk_Score"] == 12.5
    assert result["Priority"] == "Critical"
    assert result["Review_Required"] is True
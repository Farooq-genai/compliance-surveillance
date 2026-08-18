from app.services.risk_score_calculator import RiskScoreCalculator


def test_market_manipulation_critical_risk():

    ai_result = {'Outside_Party_Involved': False, 'Sender': 'analyst@acmecorp.com', 'Is_Non_Compliance': True, 'Categories': ['Communication Change'], 'Evidence': ['Shell we meet outside and close this offline. I have very big information regarding Market Stocks'], 'Evidence_Strength': ['Strong Contextual Evidence'], 'Summary': 'The email suggests a potential attempt to move sensitive communication outside normal channels.', 'Reason_For_Flagging': "The phrase 'Shell we meet outside and close this offline' indicates a potential attempt to circumvent normal communication processes, which may require compliance attention.", 'Confidence': 85}
    calculator = RiskScoreCalculator()
    result = calculator.calculate(ai_result)
    print(result)

    assert result["Risk_Score"] == 12.5
    assert result["Priority"] == "Critical"
    assert result["Review_Required"] is True
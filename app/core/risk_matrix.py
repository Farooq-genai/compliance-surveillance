DEFAULT_RISK_MATRIX = {
    "Market Manipulation": 10,
    "Market Bribery": 8,
    "Employee Ethics": 6,
    "Complaints": 5,
    "Communication Change": 4,
    "Secrecy": 3,
}

CONFIDENCE_MULTIPLIERS = {
    "HIGH": 1.0,
    "CRITICAL": 0.9,
    "MEDIUM": 0.7,
    "LOW": 0.5,
}

EVIDENCE_MULTIPLIERS = {
    "DIRECT STATEMENT": 1.0,
    "STRONG CONTEXTUAL EVIDENCE": 0.8,
    "WEAK CONTEXTUAL EVIDENCE": 0.5,
}

EXTERNAL_PARTY_MULTIPLIER = 1.25
NO_EXTERNAL_PARTY_MULTIPLIER = 1.0


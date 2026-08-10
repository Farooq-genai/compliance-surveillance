from app.core.risk_matrix import RISK_MATRIX, CONFIDENCE_MULTIPLIERS, EVIDENCE_MULTIPLIERS, EXTERNAL_PARTY_MULTIPLIER, NO_EXTERNAL_PARTY_MULTIPLIER


class RiskScoreCalculator:
    def calculate(self, ai_result: dict):
        categories = ai_result.get("Categories", [])
        confidence = ai_result.get('Confidence', 0)
        evidance_strenghts = ai_result.get("Evidence_Strength", [])
        outside_party = ai_result.get("Outside_Party_Involved", False)

        category_risk_details = []

        for index, category in enumerate(categories):
            base_weight = RISK_MATRIX.get(category)
            if base_weight is None:
                continue

            evidence_strength = self._get_evidence_strength(evidance_strenghts, index)
            confidence_multiplier = self._get_confidence_score(confidence)
            evidance_multiplier = self._get_evidence_multiplier(evidence_strength)

            external_party_multiplier = EXTERNAL_PARTY_MULTIPLIER if outside_party else NO_EXTERNAL_PARTY_MULTIPLIER

            risk_score = (base_weight * confidence_multiplier * evidance_multiplier * external_party_multiplier)

            priority = self._get_priority(risk_score)

            category_risk_details.append(
                {
                    "category": category,
                    "base_weight": base_weight,
                    "Confidence": confidence,
                    "Confidence_multiplier": confidence_multiplier,
                    "Evidence_Strength": evidence_strength,
                    "Evidence_Multiplier": evidance_multiplier,
                    "External_Party_Multiplier": external_party_multiplier,
                    "Risk_Score": risk_score,
                    "Priority": priority
                }
            )

        overall_score = self._get_overall_score(category_risk_details)
        overall_priority = self._get_priority(overall_score)
        
        return {
        "Risk_Score": overall_score,
        "Priority": overall_priority,
        "Review_Required": overall_score >= 5,
        "Review_Status": (
            "Pending Compliance Review"
            if overall_score >= 5
            else "No Review Required"
        ),
        "Category_Risk_Details": category_risk_details,
    }


    @staticmethod
    def _get_confidence_score(confidence):
        if confidence > 90:
             return CONFIDENCE_MULTIPLIERS["HIGH"]

        if confidence >= 75:
            return CONFIDENCE_MULTIPLIERS['CRITICAL']

        if confidence >=60:
            return CONFIDENCE_MULTIPLIERS['MEDIUM']
        
        return CONFIDENCE_MULTIPLIERS['LOW']

    @staticmethod
    def _get_evidence_multiplier(
        evidence_strength: str | None,
    ) -> float:
        """
        Convert evidence strength to its configured multiplier.
        """

        if not evidence_strength:
            return 0.5

        normalized = str(evidence_strength).strip().upper()

        return EVIDENCE_MULTIPLIERS.get(
            normalized,
            0.5,
        )

    @staticmethod
    def _get_evidence_strength(
        evidence_strengths: list | None,
        index: int,
    ) -> str:
        """
        Get evidence strength corresponding to the category.

        Evidence_Strength is expected to be a list where the
        position corresponds to the position in Categories.
        """

        if not evidence_strengths:
            return "Weak Contextual Evidence"

        if index >= len(evidence_strengths):
            return "Weak Contextual Evidence"

        value = evidence_strengths[index]

        if value is None:
            return "Weak Contextual Evidence"

        value = str(value).strip()

        if not value:
            return "Weak Contextual Evidence"

        return value


    @staticmethod
    def _get_overall_score(category_risk_details):
        if not category_risk_details:
            return 0.0

        return max(item['Risk_Score'] for item in category_risk_details)

    @staticmethod
    def _get_priority(risk_score):
        if risk_score >= 10:
            return "Critical"

        if risk_score >= 8.5:
            return "High"

        if risk_score >= 5:
            return "Medium"

        return "Low"



        
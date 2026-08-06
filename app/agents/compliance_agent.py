import json
import re

from app.integrations.azure_openai import AzureOpenAIClient


class ComplianceAgent:

    def __init__(self):
        self.azure_client = AzureOpenAIClient()

    def analyze(self, email: dict) -> dict:
        prompt = self._build_prompt(email)
        response = self.azure_client.chat(prompt)
        return self._parse_response(response)

    def _build_prompt(self, email: dict) -> str:
        """
        Build the prompt for Azure Open AI
        """

        return f"""
You are an Enterprise Compliance Surveillance AI.

Your task is to analyze the email and identify potential compliance violations.

IMPORTANT RULES

1. Return ONLY valid JSON.
2. Do NOT return Markdown.
3. Do NOT wrap the JSON inside ```json.
4. Do NOT explain your answer.
5. Do NOT include any text before or after the JSON.
6. If no violation exists, still return the JSON with appropriate default values.
7. Only use the categories listed below.

Compliance Categories

- Secrecy
- Market Manipulation
- Market Bribery
- Employee Ethics
- Complaints
- Communication Change

Definitions

1. Outside_Party_Involved
Return TRUE if any sender or recipient appears to belong to an external organization.

2. Is_Non_Compliance
Return TRUE only if there is reasonable evidence of a compliance concern.

3. Categories
find the Categories on the email in below [Market Manipulation, Market Bribery, Secrecy, Employee Ethics, Complaints, Communication Change]

4. Evidence
show the evidance once you find the category or categories

5. Evidence_Strength

Use only one of:

- Direct Statement
- Strong Indicator
- Weak Indicator
- Contextual

6. Summary

Maximum 2 sentences.

7. Reason_For_Flagging

Explain why this email requires compliance review.

8. Confidence

Return a number between 0 and 100.

Output JSON Format

{{
    "Outside_Party_Involved": true,
    "Sender": "",
    "Is_Non_Compliance": false,
    "Categories": [],
    "Evidence": [],
    "Evidence_Strength": [],
    "Summary": "",
    "Reason_For_Flagging": "",
    "Confidence": 0
}}

EMAIL

From:
{email["metadata"]["from"]}

To:
{email["metadata"]["to"]}

CC:
{email["metadata"]["cc"]}

BCC:
{email["metadata"]["bcc"]}

Subject:
{email["metadata"]["subject"]}

Body:
{email["body"]}

Remember:

Return ONLY the JSON object.
"""

    def _parse_response(self, response: str) -> str:
        try:
            response = re.sub(r"^```json\s*", "", response.strip(), flags=re.IGNORECASE)
            response = re.sub(r"\s*```$", "", response.strip())
            resp = json.loads(response)
            return resp
        except json.JSONDecodeError:
            return {
                "status": "FAILED",
                "error": "Azure OpenAI returned invalid JSON.",
                "raw_response": response,
            }

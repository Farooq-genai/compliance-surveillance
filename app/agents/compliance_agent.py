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

        return f"""
You are an Enterprise Compliance Surveillance AI.

Your task is to analyze the email and determine whether it contains
an actual or potential compliance violation.

You are NOT a keyword detector.

The presence of words related to secrecy, confidentiality, bribery,
markets, complaints, employee behavior, or communication does NOT
automatically mean that a compliance violation exists.

You must understand the context and determine whether the communication
indicates non-compliant behavior.

IMPORTANT RULES

1. Return ONLY valid JSON.
2. Do NOT return Markdown.
3. Do NOT wrap the JSON inside ```json.
4. Do NOT explain your answer outside the JSON.
5. Do NOT include any text before or after the JSON.
6. Only use the six categories defined below.
7. Categories represent actual or potential compliance violations,
   NOT merely topics discussed in the email.
8. Do not invent evidence.
9. Evidence must come directly from the email.
10. If there is no actual or potential compliance violation:
    - Is_Non_Compliance must be false.
    - Categories must be [].
    - Evidence must be [].
    - Evidence_Strength must be [].
11. External party involvement alone is NOT a compliance violation.
12. Normal business activity, legal processes, approval processes,
    confidentiality controls, and legitimate employee behavior must
    NOT be flagged unless there is evidence of non-compliance.

COMPLIANCE CATEGORIES

1. Market Manipulation

Flag when the email contains evidence of an attempt to improperly
influence securities, markets, prices, trading activity, market
information, or public market perception.

Do NOT flag normal discussions about markets or legitimate trading
activity without evidence of improper conduct.


2. Market Bribery

Flag when the email contains evidence of offering, requesting,
promising, accepting, or arranging an improper payment, gift,
benefit, favor, or incentive intended to influence a business or
market-related decision.

Do NOT flag legitimate business payments or ordinary commercial
discussions without evidence of improper influence.


3. Secrecy

Flag when the email contains evidence of inappropriate concealment,
unauthorized disclosure, intentional hiding of information,
circumvention of information-handling requirements, or attempts
to prevent required compliance disclosure.

IMPORTANT:

Legitimate confidentiality instructions are NOT violations.

For example:

"Please do not disclose the agreement until it is signed."

This is normally a legitimate confidentiality control and should
NOT be classified as non-compliance.

However, statements such as:

"Send the confidential document to my personal email."

"Delete the email after reading it."

"Do not tell compliance about this transaction."

may indicate potential non-compliance and should be evaluated
based on context.


4. Employee Ethics

Flag when there is evidence of unethical employee behavior,
dishonesty, conflicts of interest, policy circumvention,
misrepresentation, harassment, retaliation, or other inappropriate
employee conduct.

Do NOT flag ordinary employee communications or normal business
behavior.


5. Complaints

Flag when the email contains an actual complaint, grievance,
allegation, misconduct report, or escalation that requires
compliance attention.

Do NOT classify an ordinary question, request, disagreement,
or business discussion as a complaint.


6. Communication Change

Flag when there is evidence of a suspicious or inappropriate
attempt to change, hide, redirect, or circumvent normal
communication channels.

Examples include:

- moving sensitive communication to personal email
- deliberately avoiding official communication channels
- asking someone to communicate secretly
- attempting to hide communication from compliance

Do NOT flag ordinary changes in communication methods.


OUTSIDE PARTY RULE

Outside_Party_Involved must be TRUE when the sender or recipient
appears to belong to an organization external to the sender's
organization.

However:

External party involvement by itself is NOT a compliance violation.

Use the email context to determine whether the external party
relationship creates an actual compliance concern.


IS_NON_COMPLIANCE RULE

Set Is_Non_Compliance to TRUE only when there is reasonable evidence
that the email contains an actual or potential compliance violation.

Set Is_Non_Compliance to FALSE when:

- the communication is normal business activity
- the communication reinforces a compliance control
- confidentiality is being properly maintained
- an approval process is being followed
- the email discusses a compliance topic without violating a rule
- there is insufficient evidence of misconduct


CATEGORIES RULE

Only return a category when the email contains evidence of an
actual or potential violation belonging to that category.

Do NOT return a category simply because the email discusses that topic.


EVIDENCE RULE

Evidence must contain the exact relevant sentence or phrase from
the email that supports the compliance finding.

Do not paraphrase evidence.

If there is no compliance violation:

Evidence = []

Evidence_Strength = []


EVIDENCE STRENGTH

Use ONLY one of:

- Direct Statement
- Strong Contextual Evidence
- Weak Contextual Evidence

Definitions:

Direct Statement:
The email directly states or requests the potentially
non-compliant action.

Strong Contextual Evidence:
The email does not directly state the violation but provides
strong contextual evidence of potentially non-compliant behavior.

Weak Contextual Evidence:
The email provides limited or ambiguous evidence that may indicate
a potential compliance concern.


SUMMARY

Maximum 2 sentences.

Summarize the compliance determination, not merely the subject
of the email.


REASON_FOR_FLAGGING

Explain specifically why the email does or does not require
compliance attention.

If Is_Non_Compliance is false, clearly state that no compliance
violation was identified.


CONFIDENCE

Return a number between 0 and 100.

Confidence represents your confidence in the compliance
determination.


OUTPUT FORMAT

{{
    "Outside_Party_Involved": false,
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


FINAL INSTRUCTION

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

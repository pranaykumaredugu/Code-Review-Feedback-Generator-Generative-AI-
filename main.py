# parser.py
# ---------------------------------------------------------------
# PURPOSE: The AI responds with a blob of text. This file
# "parses" (reads and validates) that text into a clean Python
# dictionary we can use safely in the rest of our app.
#
# Think of it like a customs officer checking that everything
# in a package is correct before letting it through.
# ---------------------------------------------------------------

import json
from typing import TypedDict


# ---------------------------------------------------------------
# OUTPUT SCHEMA — defines exactly what the review result looks like
# Using TypedDict so Python knows the expected structure
# ---------------------------------------------------------------
class ReviewResult(TypedDict):
    identified_issues: list[str]
    improvement_suggestions: list[str]
    code_quality_level: str
    review_summary: str


def parse_response(raw_text: str) -> ReviewResult:
    """
    Takes the raw text from the AI and converts it to a validated dictionary.
    
    Parameters:
        raw_text : The raw string response from the LLM (should be JSON)
    
    Returns:
        A ReviewResult dictionary with all required fields
    
    Raises:
        ValueError if the response is missing required fields or is invalid JSON
    """

    # Step 1: Strip any accidental markdown code fences like ```json ... ```
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        # Remove the first line (```json or ```) and the last line (```)
        lines = cleaned.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines)

    # Step 2: Parse the JSON string into a Python dictionary
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"The AI returned invalid JSON. Raw response was:\n{raw_text}\n\nError: {e}"
        )

    # Step 3: Validate all required fields are present
    required_fields = [
        "identified_issues",
        "improvement_suggestions",
        "code_quality_level",
        "review_summary",
    ]
    for field in required_fields:
        if field not in data:
            raise ValueError(
                f"Missing required field '{field}' in AI response. Got: {list(data.keys())}"
            )

    # Step 4: Validate types
    if not isinstance(data["identified_issues"], list):
        raise ValueError("'identified_issues' must be a list")
    if not isinstance(data["improvement_suggestions"], list):
        raise ValueError("'improvement_suggestions' must be a list")
    if data["code_quality_level"] not in ["Low", "Medium", "High"]:
        raise ValueError(
            f"'code_quality_level' must be Low/Medium/High, got: {data['code_quality_level']}"
        )

    return ReviewResult(
        identified_issues=data["identified_issues"],
        improvement_suggestions=data["improvement_suggestions"],
        code_quality_level=data["code_quality_level"],
        review_summary=data["review_summary"],
    )

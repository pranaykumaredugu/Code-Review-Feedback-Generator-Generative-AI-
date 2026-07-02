# main.py
# ---------------------------------------------------------------
# PURPOSE: This is the ENTRY POINT — the file you run to start
# the application. It connects all the pieces together:
#   prompt.py  →  builds the instruction
#   model.py   →  sends it to the AI
#   parser.py  →  validates the response
#
# This is like the conductor of an orchestra — it doesn't play
# any instrument itself, but it coordinates everyone else.
# ---------------------------------------------------------------

import os
from dotenv import load_dotenv

from app.prompt import build_prompt
from app.model import call_llm
from app.parser import parse_response

# Load environment variables from .env file
# This is where your API key lives (never hardcode keys in code!)
load_dotenv()


def review_code(code_snippet: str) -> dict:
    """
    The main function: takes a code snippet and returns structured review feedback.
    
    Parameters:
        code_snippet : Any code string the user wants reviewed
    
    Returns:
        A dictionary with issues, suggestions, quality level, and summary
    """
    # Retrieve the API key from environment
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not found. Make sure you have a .env file with your key."
        )

    # Step 1: Build the prompt
    print("🔧 Building prompt...")
    prompt = build_prompt(code_snippet)

    # Step 2: Call the LLM
    print("🤖 Calling AI model...")
    raw_response = call_llm(prompt, api_key)

    # Step 3: Parse and validate the response
    print("✅ Parsing response...")
    result = parse_response(raw_response)

    return result


def print_review(result: dict):
    """Pretty-prints the review result to the terminal."""
    quality = result["code_quality_level"]
    quality_emoji = {"Low": "🔴", "Medium": "🟡", "High": "🟢"}.get(quality, "⚪")

    print("\n" + "=" * 60)
    print(f"  CODE REVIEW RESULT  {quality_emoji} Quality: {quality}")
    print("=" * 60)

    print("\n📋 REVIEW SUMMARY:")
    print(f"   {result['review_summary']}")

    print("\n🐛 IDENTIFIED ISSUES:")
    if result["identified_issues"]:
        for i, issue in enumerate(result["identified_issues"], 1):
            print(f"   {i}. {issue}")
    else:
        print("   ✅ No issues found!")

    print("\n💡 IMPROVEMENT SUGGESTIONS:")
    if result["improvement_suggestions"]:
        for i, suggestion in enumerate(result["improvement_suggestions"], 1):
            print(f"   {i}. {suggestion}")
    else:
        print("   ✅ Code looks good — no suggestions!")

    print("\n" + "=" * 60)


# ---------------------------------------------------------------
# CLI Interface — runs when you execute: python main.py
# ---------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("  🔍 Code Review Feedback Generator")
    print("  Powered by Generative AI | Innomatics Research Labs")
    print("=" * 60)
    print("\nPaste your code below.")
    print("When done, type 'END' on a new line and press Enter:\n")

    # Collect multi-line code input from user
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    code_snippet = "\n".join(lines)

    if not code_snippet.strip():
        print("❌ No code entered. Exiting.")
    else:
        try:
            result = review_code(code_snippet)
            print_review(result)
        except Exception as e:
            print(f"\n❌ Error: {e}")

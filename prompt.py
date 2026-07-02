# model.py
# ---------------------------------------------------------------
# PURPOSE: This file talks to Groq AI (free, fast, works in India)
# Everything else in the project stays exactly the same.
# ---------------------------------------------------------------

import requests

# Groq API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Model to use — llama is free and very capable
MODEL = "llama-3.1-8b-instant"


def call_llm(prompt: str, api_key: str) -> str:
    """
    Sends the prompt to Groq and returns the raw text response.

    Parameters:
        prompt  : The full instruction + code we built in prompt.py
        api_key : Your Groq API key

    Returns:
        The AI's raw text response (should be JSON string)
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 1024,
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=body)

    # If something goes wrong, raise a clear error
    if response.status_code != 200:
        raise Exception(
            f"Groq API call failed with status {response.status_code}: {response.text}"
        )

    data = response.json()

    # Extract the text from Groq's response structure
    raw_text = data["choices"][0]["message"]["content"]
    return raw_text

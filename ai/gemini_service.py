
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing from the .env file."
    )

client = genai.Client(api_key=API_KEY)


def generate_ai_response(prompt: str) -> str:
    """
    Generate an AI response using Gemini Interactions API.
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    if len(prompt) > 30000:
        raise ValueError("Prompt exceeds the 30,000 character limit.")

    try:
        response = client.interactions.create(
            model=MODEL,
            input=prompt
        )

        result = response.output_text

        if not result:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return result

    except Exception as error:
        raise RuntimeError(
            f"Gemini API error: {error}"
        ) from error

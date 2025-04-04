import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
prompt = "Tell me about ways to mitigate overfishing."

def generate(prompt):
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(
        api_key=gemini_api_key,
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt + "Answer the above question in "
                "a maximum of 20 words."),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    result = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config
    ):
        result += chunk.text
    return result

if __name__ == "__main__":
    generate(prompt)

import os
from google import genai
from google.genai import types

def get_ai_response(prompt):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json")
    ).text

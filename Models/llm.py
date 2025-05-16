from dotenv import load_dotenv
import os
load_dotenv()
from google import genai
from google.genai import types


def llm_call(system_prompt, actual_prompt):
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt),
        contents=actual_prompt
    )
    return response.text
# Model/chat_llm.py
from dotenv import load_dotenv
import os
load_dotenv()

from google import genai
from google.genai import types

def chat_llm(history, new_user_input):
    # Initialize Gemini client
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

    # Convert history to Gemini's expected format
    formatted_history = [
        types.Content(role=msg["role"], parts=[types.Part(text=msg["content"])])
        for msg in history
    ]

    # Create the chat with existing history
    chat = client.chats.create(
        model="gemini-2.0-flash",
        history=formatted_history
    )

    # Send the new message
    response = chat.send_message(new_user_input)

    # Return full updated chat history
    return chat.get_history()

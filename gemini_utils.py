# gemini_utils.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def extract_items_from_transcript(transcript: str) -> list:
    prompt = f"""
You are a smart grocery list parser. The user will give you a transcription of a spoken grocery list. 

Your job is to:
1. Extract only grocery items with their quantities like "1 kg", "2 packets", "500 gm", "6 pieces", "1 litre", etc.
2. Return the result strictly in this format:
[
  {{ "item": "<item_name>", "quantity": "<quantity>" }},
  ...
]

Here is the transcription:
\"{transcript}\"
"""

    response = model.generate_content(prompt)
    return response.text

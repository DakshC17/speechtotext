# gemini_utils.py

import os
import re
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def extract_items_from_transcript(transcript: str) -> list:
    prompt = f"""
You are a smart grocery list parser.

The user will give you a transcription of a spoken grocery list.

Your task:
1. Identify each grocery item and its quantity.
2. Return **only** a valid JSON array — no explanations, no markdown, no extra text.
3. JSON format:
[
  {{ "item": "<item_name>", "quantity": "<quantity>" }},
  ...
]

Here is the transcription:
\"{transcript}\"

Output only valid JSON.
"""

    response = model.generate_content(prompt)
    raw_output = response.text.strip()

    # Try to extract JSON if Gemini adds extra formatting like ```json ... ```
    json_match = re.search(r"\[.*\]", raw_output, re.DOTALL)
    if json_match:
        raw_output = json_match.group(0)

    try:
        items = json.loads(raw_output)
    except json.JSONDecodeError:
        print("⚠️ Failed to parse JSON from Gemini output.")
        items = []

    return items

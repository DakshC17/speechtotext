from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import tempfile
import os
import httpx
import re

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()

# -----------------------------
# GROQ API: Transcribe MP3 Audio
# -----------------------------
async def transcribe_with_groq(audio_path: str) -> str:
    headers = {
        "Authorization": f"Bearer " + GROQ_API_KEY
    }

    with open(audio_path, "rb") as audio_file:
        files = {
            "file": ("audio.mp3", audio_file, "audio/mpeg"),
            "model": (None, "whisper-large-v3")
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/audio/transcriptions",
                    headers=headers,
                    files=files
                )
                response.raise_for_status()
                result = response.json()
                return result.get("text", "Unknown transcript")
        except httpx.HTTPStatusError as e:
            raise Exception(f"Groq API error {e.response.status_code}: {e.response.text}")
        except Exception as e:
            raise Exception(f"Transcription error: {str(e)}")

# -----------------------------
# Main Transcription Endpoint
# -----------------------------
@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp3"):
        return JSONResponse(status_code=400, content={"error": "Only .mp3 files are supported"})

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name
            content = await file.read()
            tmp.write(content)

        transcript = await transcribe_with_groq(audio_path)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    finally:
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)

    grocery_list = extract_items_and_quantities(transcript)

    return {
        "transcript": transcript,
        
    }

# -----------------------------
# Multilingual Grocery Extractor
# -----------------------------
def extract_items_and_quantities(text):
    text = text.lower()

    # Noise and filler words common across Indian languages
    fillers = ["جی", "गये", "गए", "गा", "గారు", "சார்", "साहेब", "ಅಯ್ಯಾ", "sir", "ma'am", "madam", "जी", "bhai", "bhayya"]
    for filler in fillers:
        text = text.replace(filler, "")

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    # Units across major Indian languages
    units = [
        "kg", "g", "gram", "grams", "ml", "l", "litre", "liter", "packet", "packets", "piece", "pieces", "dozen",
        "किलो", "ग्राम", "लीटर", "पैकेट", "टुकड़ा", "दरजन",                        # Hindi
        "କିଲୋ", "ଗ୍ରାମ", "ଲିଟର", "ପ୍ୟାକେଟ୍", "ଟୁକୁଡ଼ା", "ଡଜନ୍",                # Odia
        "কেজি", "গ্রাম", "লিটার", "প্যাকেট", "পিস", "ডজন",                         # Bengali
        "கிலோ", "கிராம்", "லிட்டர்", "பாக்கெட்", "துண்டு", "டஜன்",                # Tamil
        "కిలో", "గ్రాము", "లీటరు", "ప్యాకెట్", "ముక్క", "డజను",                  # Telugu
        "കിലോ", "ഗ്രാം", "ലിറ്റര്", "പാക്കറ്റ്", "തുണ്ട്", "ഡസൻ",                   # Malayalam
        "ಕಿಲೋ", "ಗ್ರಾಂ", "ಲೀಟರ್", "ಪ್ಯಾಕೆಟ್", "ತುಗುಡು", "ಡಜನ್",                # Kannada
        "किलो", "ग्रॅम", "लिटर", "पॅकेट", "तुकडा", "डझन"                        # Marathi
    ]
    units_regex = "|".join(map(re.escape, units))

    # Extract pattern with optional quantity, optional unit, and item
    pattern = re.compile(
        rf"(?:(\d+(?:[\.,]\d+)?|\d+/\d+)?\s*({units_regex})?\s+([\w\u0900-\u0D7F\-]+))",
        re.UNICODE
    )

    items = []
    for match in pattern.finditer(text):
        quantity = match.group(1) or ""
        unit = match.group(2) or ""
        item = match.group(3).strip()

        if item in units or not item:
            continue

        full_quantity = f"{quantity} {unit}".strip() if quantity or unit else "1 unit"

        items.append({
            "item": item,
            "quantity": full_quantity
        })

    return items

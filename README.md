# Speech to Text Transcriber

An AI-powered FastAPI service that transcribes audio recordings and intelligently extracts grocery items with quantities. Perfect for converting voice memos into structured shopping lists.

## Features

- **🎯 Audio Transcription**: High-accuracy speech-to-text using Groq's Whisper Large V3 Turbo model
- **🛒 Smart Grocery Extraction**: AI-powered parsing using Google's Gemini 2.0 Flash to identify items and quantities
- **🌍 Multilingual Support**: Handles multiple Indian languages (Hindi, Tamil, Telugu, Malayalam, Kannada, Bengali, Odia, Marathi) plus English
- **📦 Structured Output**: Returns both raw transcript and parsed JSON grocery list
- **🐳 Docker Ready**: Containerized for easy deployment to Cloud Run or any container platform
- **⚡ Fast & Async**: Built with FastAPI for high-performance async processing

## Architecture

```
┌─────────────┐
│   Client    │
│  (MP3 File) │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│      FastAPI Service            │
│  ┌──────────────────────────┐   │
│  │  /transcribe/ endpoint   │   │
│  └───────┬──────────────────┘   │
│          │                      │
│          ▼                      │
│  ┌──────────────────────────┐   │
│  │   Groq Whisper API       │   │
│  │   (Audio → Text)         │   │
│  └───────┬──────────────────┘   │
│          │                      │
│          ▼                      │
│  ┌──────────────────────────┐   │
│  │   Gemini 2.0 Flash       │   │
│  │   (Text → Grocery List)  │   │
│  └───────┬──────────────────┘   │
└──────────┼──────────────────────┘
           │
           ▼
    ┌──────────────┐
    │ JSON Response│
    │ - transcript │
    │ - items[]    │
    └──────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Groq API Key](https://console.groq.com/) (for Whisper transcription)
- [Google Gemini API Key](https://ai.google.dev/) (for grocery extraction)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd speechtotext
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`

## 📖 API Documentation

### `POST /transcribe/`

Transcribes an MP3 audio file and extracts grocery items.

**Request:**
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Body**: 
  - `file`: MP3 audio file (required)

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@grocery_list.mp3"
```

**Example using Python:**
```python
import requests

url = "http://localhost:8000/transcribe/"
files = {"file": open("grocery_list.mp3", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

**Success Response (200 OK):**
```json
{
  "transcript": "I need 2 kg tomatoes, 1 liter milk, and 500 grams paneer",
  "items": [
    {
      "item": "tomatoes",
      "quantity": "2 kg"
    },
    {
      "item": "milk",
      "quantity": "1 liter"
    },
    {
      "item": "paneer",
      "quantity": "500 grams"
    }
  ]
}
```

**Error Responses:**

- **400 Bad Request**: Invalid file format
  ```json
  {
    "error": "Only .mp3 files are supported"
  }
  ```

- **500 Internal Server Error**: Transcription or parsing failure
  ```json
  {
    "error": "Gemini parsing failed",
    "details": "Error message here"
  }
  ```

### Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🐳 Docker Deployment

### Build the Docker image

```bash
docker build -t speechtotext .
```

### Run locally with Docker

```bash
docker run -p 8080:8080 \
  -e GROQ_API_KEY=your_groq_api_key \
  -e GEMINI_API_KEY=your_gemini_api_key \
  speechtotext
```

### Deploy to Google Cloud Run

1. **Build and push to Google Container Registry**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/speechtotext
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy speechtotext \
     --image gcr.io/YOUR_PROJECT_ID/speechtotext \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GROQ_API_KEY=your_key,GEMINI_API_KEY=your_key
   ```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Web Framework** | FastAPI 0.111.0 | High-performance async API framework |
| **Server** | Uvicorn 0.30.1 | ASGI server for FastAPI |
| **HTTP Client** | httpx 0.27.0 | Async HTTP requests to external APIs |
| **Transcription** | Groq Whisper Large V3 Turbo | State-of-the-art speech recognition |
| **AI Parsing** | Google Gemini 2.0 Flash | Intelligent grocery item extraction |
| **Environment** | python-dotenv 1.0.1 | Environment variable management |
| **Validation** | Pydantic 2.8.1 | Data validation and settings |
| **Containerization** | Docker | Portable deployment |

## 📁 Project Structure

```
speechtotext/
├── main.py                 # FastAPI application & transcription endpoint
├── gemini_utils.py         # Gemini AI integration for grocery extraction
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── .dockerignore          # Docker build exclusions
├── .gitignore            # Git exclusions
├── .env                  # Environment variables (not in repo)
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | API key for Groq Whisper transcription | ✅ Yes |
| `GEMINI_API_KEY` | API key for Google Gemini AI | ✅ Yes |
| `PORT` | Server port (default: 8080 in Docker) | ❌ No |

### Supported Audio Format

- **Format**: MP3 (MPEG Audio Layer 3)
- **Encoding**: Any standard MP3 encoding
- **Recommended**: 16kHz or higher sample rate for best accuracy

## 🌍 Multilingual Support

The service intelligently handles grocery items in multiple languages:

- **English**: "2 kg tomatoes, 1 liter milk"
- **Hindi**: "2 किलो टमाटर, 1 लीटर दूध"
- **Tamil**: "2 கிலோ தக்காளி, 1 லிட்டர் பால்"
- **Telugu**: "2 కిలో టమోటాలు, 1 లీటరు పాలు"
- **Malayalam**: "2 കിലോ തക്കാളി, 1 ലിറ്റര് പാൽ"
- **Kannada**: "2 ಕಿಲೋ ಟೊಮೇಟೊ, 1 ಲೀಟರ್ ಹಾಲು"
- **Bengali**: "2 কেজি টমেটো, 1 লিটার দুধ"
- **Odia**: "2 କିଲୋ ଟମାଟୋ, 1 ଲିଟର ଦୁଧ"
- **Marathi**: "2 किलो टोमॅटो, 1 लिटर दूध"

## 🧪 Testing

### Manual Testing

1. Record a voice memo listing grocery items with quantities
2. Save as MP3 format
3. Use the API documentation UI at `/docs` to upload and test
4. Verify the returned JSON contains correct items and quantities

### Example Test Cases

**Test 1: English grocery list**
```
Audio: "I need 2 kilograms of tomatoes, 1 liter of milk, and 500 grams of paneer"
Expected: Items for tomatoes (2 kg), milk (1 liter), paneer (500 grams)
```

**Test 2: Mixed language**
```
Audio: "मुझे 2 किलो आलू और 1 packet bread चाहिए"
Expected: Items for potatoes (2 kg), bread (1 packet)
```

**Test 3: No quantities**
```
Audio: "I need tomatoes, onions, and garlic"
Expected: Items with default "1 unit" quantities
```

## 🚨 Error Handling

The service includes comprehensive error handling:

- ✅ **File validation**: Only MP3 files accepted
- ✅ **Temporary file cleanup**: Automatic cleanup even on errors
- ✅ **API error handling**: Graceful handling of Groq/Gemini API failures
- ✅ **JSON parsing**: Robust extraction even with malformed AI responses
- ✅ **Timeout protection**: 60-second timeout for transcription requests

## 📊 Performance Considerations

- **Async Processing**: All I/O operations are async for better concurrency
- **Temporary Files**: Audio files are stored temporarily and cleaned up immediately
- **API Timeouts**: 60-second timeout prevents hanging requests
- **Lightweight Container**: Uses `python:3.10-slim` for minimal image size

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Support for additional audio formats (WAV, M4A, OGG)
- [ ] Batch processing multiple files
- [ ] WebSocket support for real-time transcription
- [ ] Caching layer for repeated transcriptions
- [ ] Rate limiting and authentication
- [ ] Unit and integration tests

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Groq** for providing fast Whisper API access
- **Google** for the powerful Gemini AI model
- **FastAPI** for the excellent web framework

## 📧 Support

For issues, questions, or suggestions, please open an issue on the repository.

---

**Built using FastAPI, Groq Whisper, and Google Gemini**

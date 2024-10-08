# LocalWhisperAPIService
Whisper Speech Recognition API

This is an API service built on OpenAI's Whisper speech recognition model. It can convert uploaded audio files into text.

## Features

• Supports uploading of various common audio formats, including WAV, MP3, FLAC, OGG, M4A, WebM, AAC, WMA, AIFF, and CAF.
• Based on the Whisper model, supports recognition of multiple languages
• RESTful API interface, convenient for frontend integration
• Health check endpoint for monitoring service status

## Tech Stack

• Python 3.8+
• FastAPI Web framework
• Whisper speech recognition model
• (Other dependencies)

## Installation and Deployment

1. Clone the code repository
2. (Option A) Using virtual environment:
   a. Create a virtual environment:
      python3 -m venv myvenv
   b. Activate the virtual environment:
      - On Windows: `myvenv\Scripts\activate`
      - On macOS and Linux: `source myvenv/bin/activate`
   c. Before installing dependencies, open the `requirements.txt` file and modify the `tokenizers` line:
      - Find the line starting with `https://files.pythonhosted.org/packages/...`
      - Replace it with the appropriate wheel URL for your system. For example:
        - For Python 3.10 on Linux: use the existing URL
        - For other systems: visit https://pypi.org/project/tokenizers/#files, find the appropriate wheel for your system, and use its URL
   d. Install dependencies: `pip install -r requirements.txt`
   e. Start the API service: `uvicorn app.main:app --reload`
3. (Option B) Using Docker:
   a. Build the Docker image:
      `docker build -t localwhisperapi .`
   b. Run the Docker container:
      `docker run -d -p 8000:8000 localwhisperapi`
4. Visit http://localhost:8000/docs to view the API documentation

## Usage

1. Health Check:
   - GET request to the /ping endpoint
   - Returns a status indicating if the service is healthy

2. Transcription:
   - POST audio files to the /transcribe endpoint
   - Supported audio formats: WAV, MP3, FLAC, OGG, M4A, WebM, AAC, WMA, AIFF, CAF
   - The result returned is a JSON object containing the transcribed text content

Example using curl:

Contributing

Issues and Pull Requests are welcome!

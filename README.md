# LocalWhisperAPIService
Whisper Speech Recognition API

This is an API service built on OpenAI's Whisper speech recognition model. It can convert uploaded audio files (such as mp3, wav, etc.) into text.

Features

• Supports uploading of various common audio formats, including mp3, wav, flac, etc.
• Based on the Whisper model, supports recognition of multiple languages
• RESTful API interface, convenient for frontend integration
• Supports batch audio file processing
• Concurrency control and error handling
• (Other features)

Tech Stack

• Python 3.8+
• FastAPI or Flask Web framework
• Whisper speech recognition model
• (Other dependencies)

Installation and Deployment

1. Clone the code repository
2. (Option A) Using virtual environment:
   a. Create a virtual environment:
      python3 -m venv myvenv
   b. Activate the virtual environment:
      - On Windows: `myvenv\Scripts\activate`
      - On macOS and Linux: `source myvenv/bin/activate`
   c. Install dependencies: `pip install -r requirements.txt`
   d. Start the API service: `uvicorn app.main:app --reload`
3. (Option B) Using Docker:
   a. Build the Docker image:
      `docker build -t localwhisperapi .`
   b. Run the Docker container:
      `docker run -d -p 8000:8000 localwhisperapi`
4. Visit http://localhost:8000/docs to view the API documentation

Usage

1. POST audio files to the /recognize endpoint
2. The result returned is a JSON object containing the recognized text content

Contributing

Issues and Pull Requests are welcome!

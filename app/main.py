import torch
from fastapi import FastAPI, File, UploadFile, HTTPException
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import os

app = FastAPI(
    title="Whisper Speech Recognition API",
    description="API for transcribing audio files using the Whisper model",
    version="1.0.0",
)

# Set up device and dtype
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Load Whisper model and processor
model_id = "openai/whisper-small"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

# Create pipeline
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

@app.get("/ping")
async def ping():
    return {"status": "ok", "message": "Service is healthy"}

@app.post("/transcribe", summary="Transcribe audio file", description="Transcribe an audio file to text. Supports various audio formats including WAV, MP3, FLAC, OGG, M4A, WebM, AAC, WMA, AIFF, and CAF.")
async def transcribe_audio(audio: UploadFile = File(...)):
    supported_formats = ['.wav', '.mp3', '.flac', '.ogg', '.m4a', '.webm', '.aac', '.wma', '.aiff', '.aif', '.caf']
    file_extension = os.path.splitext(audio.filename)[1].lower()
    
    if file_extension not in supported_formats:
        raise HTTPException(status_code=400, detail=f"Unsupported file format. Supported formats are: {', '.join(supported_formats)}")
    
    # Read the uploaded file
    audio_content = await audio.read()
    
    # Process the audio using the pipeline
    try:
        result = pipe(
            audio_content,
            generate_kwargs={"language": "en"},  # Force English output
            return_timestamps=True  # This should implicitly set attention_mask
        )
        return {"transcription": result["text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

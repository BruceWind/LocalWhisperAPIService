import torch
from fastapi import FastAPI, File, UploadFile, HTTPException
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, WhisperProcessor
import os
import librosa
import io
import numpy as np

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

processor = WhisperProcessor.from_pretrained(model_id)

# Add this after the imports
WHISPER_LANGUAGES = {
    "en": "english", "zh": "chinese", "de": "german", "es": "spanish", "ru": "russian",
    "ko": "korean", "fr": "french", "ja": "japanese", "pt": "portuguese", "tr": "turkish",
    "pl": "polish", "ca": "catalan", "nl": "dutch", "ar": "arabic", "sv": "swedish",
    "it": "italian", "id": "indonesian", "hi": "hindi", "fi": "finnish", "vi": "vietnamese",
    "he": "hebrew", "uk": "ukrainian", "el": "greek", "ms": "malay", "cs": "czech",
    "ro": "romanian", "da": "danish", "hu": "hungarian", "ta": "tamil", "no": "norwegian",
    "th": "thai", "ur": "urdu", "hr": "croatian", "bg": "bulgarian", "lt": "lithuanian",
    "la": "latin", "mi": "maori", "ml": "malayalam", "cy": "welsh", "sk": "slovak",
    "te": "telugu", "fa": "persian", "lv": "latvian", "bn": "bengali", "sr": "serbian",
    "az": "azerbaijani", "sl": "slovenian", "kn": "kannada", "et": "estonian",
    "mk": "macedonian", "br": "breton", "eu": "basque", "is": "icelandic",
    "hy": "armenian", "ne": "nepali", "mn": "mongolian", "bs": "bosnian",
    "kk": "kazakh", "sq": "albanian", "sw": "swahili", "gl": "galician",
    "mr": "marathi", "pa": "punjabi", "si": "sinhala", "km": "khmer", "sn": "shona",
    "yo": "yoruba", "so": "somali", "af": "afrikaans", "oc": "occitan",
    "ka": "georgian", "be": "belarusian", "tg": "tajik", "sd": "sindhi",
    "gu": "gujarati", "am": "amharic", "yi": "yiddish", "lo": "lao", "uz": "uzbek",
    "fo": "faroese", "ht": "haitian creole", "ps": "pashto", "tk": "turkmen",
    "nn": "nynorsk", "mt": "maltese", "sa": "sanskrit", "lb": "luxembourgish",
    "my": "myanmar", "bo": "tibetan", "tl": "tagalog", "mg": "malagasy",
    "as": "assamese", "tt": "tatar", "haw": "hawaiian", "ln": "lingala",
    "ha": "hausa", "ba": "bashkir", "jw": "javanese", "su": "sundanese",
}

@app.get("/ping")
async def ping():
    return {"status": "ok", "message": "Service is healthy"}

@app.post("/transcribe", summary="Transcribe audio file", description="Transcribe an audio file to text. Supports various audio formats including WAV, MP3, FLAC, OGG, M4A, WebM, AAC, WMA, AIFF, and CAF.")
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: str = "en"
):
    if language not in WHISPER_LANGUAGES:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported language code. Supported languages are: {', '.join(WHISPER_LANGUAGES.keys())}"
        )

    supported_formats = ['.wav', '.mp3', '.flac', '.ogg', '.m4a', '.webm', '.aac', '.wma', '.aiff', '.aif', '.caf']
    file_extension = os.path.splitext(audio.filename)[1].lower()
    
    if file_extension not in supported_formats:
        raise HTTPException(status_code=400, detail=f"Unsupported file format. Supported formats are: {', '.join(supported_formats)}")
    
    # Read the uploaded file
    audio_content = await audio.read()
    
    try:
        # Convert audio bytes to numpy array using BytesIO
        audio_bytes = io.BytesIO(audio_content)
        audio_array, sampling_rate = librosa.load(
            audio_bytes, 
            sr=16000,
            duration=None
        )

        # Calculate chunk size (30 seconds * sample_rate)
        chunk_length = 30 * sampling_rate
        chunks = []
        
        # Split audio into 30-second chunks
        for i in range(0, len(audio_array), chunk_length):
            chunk = audio_array[i:i + chunk_length]
            # Pad last chunk if necessary
            if len(chunk) < chunk_length:
                chunk = np.pad(chunk, (0, chunk_length - len(chunk)))
            chunks.append(chunk)

        transcriptions = []
        
        # Process each chunk
        for chunk in chunks:
            # Process audio chunk with the processor
            input_features = processor(
                chunk, 
                sampling_rate=sampling_rate, 
                return_tensors="pt"
            ).input_features.to(device)

            # Force the decoder to use specified language
            forced_decoder_ids = processor.get_decoder_prompt_ids(
                language=WHISPER_LANGUAGES[language],
                task="transcribe"
            )
            model.config.forced_decoder_ids = forced_decoder_ids

            # Generate transcription
            predicted_ids = model.generate(
                input_features,
                max_length=448,
                num_beams=5,
                length_penalty=1.0,
                temperature=0.0
            )
            
            chunk_transcription = processor.batch_decode(
                predicted_ids, 
                skip_special_tokens=True
            )[0].strip()
            
            if chunk_transcription:  # Only add non-empty transcriptions
                transcriptions.append(chunk_transcription)

        # Combine all transcriptions
        full_transcription = " ".join(transcriptions)

        return {"transcription": full_transcription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, File, UploadFile
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torch

app = FastAPI()

# Load Whisper model and processor
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
processor = WhisperProcessor.from_pretrained("openai/whisper-base")

@app.post("/recognize")
async def recognize_speech(audio: UploadFile = File(...)):
    # Read the uploaded file
    audio_content = await audio.read()
    
    # Process the audio
    input_features = processor(audio_content, return_tensors="pt").input_features
    
    # Generate token ids
    predicted_ids = model.generate(input_features)
    
    # Decode token ids to text
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    
    return {"transcription": transcription[0]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
import torch
from fastapi import FastAPI, File, UploadFile
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

app = FastAPI()

# Set up device and dtype
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Load Whisper model and processor
model_id = "openai/whisper-large-v3"
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

@app.post("/recognize")
async def recognize_speech(audio: UploadFile = File(...)):
    # Read the uploaded file
    audio_content = await audio.read()
    
    # Process the audio using the pipeline
    result = pipe(audio_content)
    
    return {"transcription": result["text"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
import whisper

model = whisper.load_model("base")
result = model.transcribe("./data/audio.wav")
print(result["text"])

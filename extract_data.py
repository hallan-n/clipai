import whisper

# Caminho do vídeo
VIDEO_PATH = "C:/Users/Neves Sena/Documents/projects/clipai/videoplayback.mp4"

# Carrega modelo (tiny, small, medium, large)
# Quanto maior o modelo, melhor precisão mas mais pesado
model = whisper.load_model("small")  

# Transcreve o vídeo
result = model.transcribe(VIDEO_PATH, fp16=False)  # fp16=False se estiver usando CPU

# O resultado tem:
# - 'text': transcrição completa
# - 'segments': lista de trechos com start/end/text
print("=== Transcrição completa ===")
print(result["text"])

print("/n=== Segmentos com timestamps ===")
for seg in result["segments"]:
    print(f"{seg['start']:.2f} - {seg['end']:.2f}: {seg['text']}")

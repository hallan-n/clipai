import asyncio
import whisper
from sentence_transformers import SentenceTransformer, util
import json
from cache import get, add

MIN_SEGMENT = 300      # mínimo 5 min
THRESHOLD = 0.7        # sensibilidade média
BLOCK_SIZE = 750       # blocos de ~12,5 min



async def get_video_transcribe(video_path: str):
    transcribe = await get('video_transcribe')
    if transcribe:
        return json.loads(transcribe)
    
    model = whisper.load_model("small")
    result = model.transcribe(video_path, fp16=False) 

    await add('video_transcribe', json.dumps(result))
    return result

def get_highlights(transcribe: dict):
    texts = [d["text"] for d in transcribe]
    times = [(d["start"], d["end"]) for d in transcribe]

    model = SentenceTransformer("all-MiniLM-L6-v2")
      
    blocks = []
    current_text, current_start = "", times[0][0]

    for i, (start, end) in enumerate(times):
        current_text += " " + texts[i]
        if end - current_start >= BLOCK_SIZE:
            blocks.append((current_start, end, current_text.strip()))
            current_start = end
            current_text = ""

    # adiciona último bloco
    if current_text:
        blocks.append((current_start, times[-1][1], current_text.strip()))

    block_texts = [b[2] for b in blocks]
    embeddings = model.encode(block_texts, convert_to_tensor=True)

    similarities = [
        util.cos_sim(embeddings[i], embeddings[i + 1]).item()
        for i in range(len(embeddings) - 1)
    ]

    cuts = [
        blocks[i][1]
        for i, sim in enumerate(similarities)
        if sim < THRESHOLD
    ]

    segments = []
    start = 0.0
    for cut in cuts:
        if cut - start >= MIN_SEGMENT:
            segments.append((start, cut))
            start = cut

    if blocks and blocks[-1][1] - start >= 10:
        segments.append((start, blocks[-1][1]))

    return segments

async def main():
    video_path = 'C:/Users/Neves Sena/Documents/projects/clipai/videoplayback.mp4'
    transcribe = await get_video_transcribe(video_path)
    segments = get_highlights(transcribe['segments'])
    print(segments)

    previews = preview_summary(transcribe['segments'], segments, top_k=5)
    
    for p in previews:
        dur = (p['end'] - p['start']) / 60
        print(f"[{p['start']:.0f}s → {p['end']:.0f}s | {dur:.1f} min] → {p['preview']}")

        
asyncio.run(main())

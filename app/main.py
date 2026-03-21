import json
import re
from dataclasses import dataclass
from pathlib import Path

import uvicorn
from models import YouTubeVideo
from ask_llm import ask_gpt
from edit_video import cut_video
from fastapi import FastAPI, HTTPException
from logger import logger
from prompt import prompt
from youtube import (
    download_video,
    fetch_transcribe,
)


from datetime import datetime

def generate_schedule(start: datetime, end: datetime, slots: int) -> list[datetime]:
    if slots <= 0:
        raise ValueError("slots deve ser > 0")

    if end < start:
        raise ValueError("end deve ser >= start")

    if slots == 1:
        return [start]

    total = end - start
    step = total / (slots - 1)

    return [start + step * i for i in range(slots)]

t1 = datetime.now().replace(hour=0)
t2 = datetime.now().replace(hour=18)
print(generate_schedule(t1, t2, 5))

def process_cuts(video_url: str, main_theme: str, min_len: int, max_len: int) -> YouTubeVideo:
    video_id = video_url.split("v=")[-1]

    base_path = Path("temp") / video_id
    cuts_path = base_path / "cuts"
    raw_video = base_path / "raw.mp4"

    cuts_path.mkdir(parents=True, exist_ok=True)

    transcribe = fetch_transcribe(video_url)
    logger.info("Transcrevendo vídeo.")
    if not transcribe:
        logger.error(f"Transcrição não disponível para o vídeo: {video_url}")
        raise ValueError("Transcrição não disponível")

    if raw_video.exists():
        logger.info("Vídeo já baixado!")
        video_path = raw_video
    else:
        logger.info("Iniciando download do Vídeo")
        video_path = Path(download_video(video_url, str(raw_video)))

    existing_cuts = [f for f in cuts_path.iterdir() if f.is_file()]
    if existing_cuts:
        logger.info("Cortes já realizados")
        return existing_cuts

    response = ask_gpt(prompt, [main_theme, min_len, max_len, str(transcribe)])

    try:
        segments = json.loads(response)
    except json.JSONDecodeError:
        logger.error("Resposta inválida do GPT")
        raise

    cuts = []

    for segment in segments:
        cut_path = cuts_path / f"{segment['title'].upper()}.mp4"
        cut_video(video_path, segment["start"], segment["end"], cut_path)
        cuts.append(
            YouTubeVideo(
                video_id=video_id,
                title=segment['title'].upper(),
                description=segment['summary'],
                thumb_path=None,
                video_path=cut_path,
                published_at=None,
                status="public"
            )
        )
    logger.info(f"{len(cuts)} Cortes processados")
    return cuts


app = FastAPI()


@app.get("/")
def generate_cut(url: str):
    if not re.match(r"https:\/\/www\.youtube\.com\/watch\?v=\w+", url):
        raise HTTPException("URL no formato incorreto")
    
    videos = process_cuts(url, "política", 7, 30)
    



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

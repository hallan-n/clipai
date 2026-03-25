import json
import re
from pathlib import Path

import uvicorn
from models import YouTubeVideo
from ask_llm import ask_gpt
from edit_video import cut_video
from fastapi import FastAPI, HTTPException
from logger import logger
from prompt import prompt, description
from youtube import (
    download_video,
    fetch_transcribe,
    upload_video
)
from datetime import datetime, timezone



def generate_schedule(start: datetime, end: datetime, slots: int) -> list[datetime]:
    if slots <= 0:
        raise ValueError("slots deve ser > 0")

    if end < start:
        raise ValueError("end deve ser >= start")

    if slots == 1:
        return [start]

    total = end - start
    step = total / (slots - 1)
    logger.info(f"Gerando schedule para {slots} videos")
    return [start + step * i for i in range(slots)]


def process_cuts(video_url: str, main_theme: str, min_len: int, max_len: int) -> list[YouTubeVideo]:
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
                description=description.format(segment['summary'], video_url),
                thumb_path=None,
                video_path=cut_path,
                published_at=None,
                status="private"
            )
        )
    logger.info(f"{len(cuts)} Cortes processados")
    return cuts


def to_iso_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


app = FastAPI()

@app.get("/")
def generate_cut(url: str):
    if not re.match(r"https:\/\/www\.youtube\.com\/watch\?v=\w+", url):
        raise HTTPException("URL no formato incorreto")
    
    videos = process_cuts(url, "política", 7, 30)

    schedules = generate_schedule(
        datetime.now().replace(hour=14, tzinfo=timezone.utc),
        datetime.now().replace(hour=22, tzinfo=timezone.utc),
        len(videos)
    )

    for schedule, video in zip(schedules, videos):
        video.published_at = to_iso_utc(schedule)
        upload_video(video)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

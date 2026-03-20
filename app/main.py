import json
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path

import uvicorn
from ask_llm import ask_gpt
from edit_video import cut_video
from fastapi import FastAPI
from fastapi.responses import FileResponse
from logger import logger
from prompt import prompt
from youtube import (
    download_video,
    fetch_channel_info,
    fetch_transcribe,
    fetch_video_info,
    fetch_video_infos,
)


def process_cuts(video_url: str, main_theme: str, min_len: int, max_len: int):
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

        cuts.append(cut_path)
    logger.info(f"{len(cuts)} Cortes processados")
    return cuts


@dataclass
class Cut:
    url: str
    main_theme: str
    min_len: int
    max_len: int

    def __post_init__(self):
        if not re.match(r"https:\/\/www\.youtube\.com\/watch\?v=\w+", self.url):
            raise ValueError("URL no formato incorreto")


app = FastAPI()


@app.post("/")
def generate_cut(cut: Cut):
    zip_path = Path("temp") / "videos.zip"
    video_paths = process_cuts(cut.url, cut.main_theme, cut.min_len, cut.max_len)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file_str in video_paths:
            file_path = Path(file_str)
            if file_path.exists() and file_path.is_file():
                zipf.write(file_path, arcname=file_path.name)

    return FileResponse(
        path=zip_path, media_type="application/zip", filename="videos.zip"
    )


@app.get("/video")
def get_video(video_url: str):
    return fetch_video_info(video_url)


@app.get("/feed")
def get_feed(channel_id: str, limit: int = 15):
    return fetch_video_infos(channel_id, limit)


@app.get("/channel")
def get_channel(channel_url: str):
    return fetch_channel_info(channel_url)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

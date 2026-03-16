import json
from pathlib import Path

from ask_llm import ask_gpt
from edit_video import cut_video
from logger import logger
from prompt import prompt
from youtube import download_video, fetch_transcribe


def process_cuts(video_url: str, main_theme: str, min_len: int, max_len: int):
    video_id = video_url.split("v=")[-1]

    base_path = Path("temp") / video_id
    cuts_path = base_path / "cuts"
    raw_video = base_path / "raw.mp4"

    cuts_path.mkdir(parents=True, exist_ok=True)

    transcribe = fetch_transcribe(video_url)
    if not transcribe:
        logger.error(f"Transcrição não disponível para o vídeo: {video_url}")
        raise ValueError("Transcrição não disponível")

    if raw_video.exists():
        logger.info("Vídeo já baixado!")
        video_path = raw_video
    else:
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

        cut_video(
            video_path,
            segment["start"],
            segment["end"],
            cut_path
        )

        cuts.append(cut_path)

    return cuts

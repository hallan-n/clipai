from services.logger import logger
from youtube_transcript_api import YouTubeTranscriptApi


def _transcribe_youtube_api(video_id: str):
    try:
        segments = YouTubeTranscriptApi().fetch(video_id, languages=["pt", "pt-BR"])

        result = []

        for s in segments:
            start = float(s.start)
            duration = float(s.duration)
            end = start + duration

            result.append(
                {
                    "text": s.text,
                    "start": start,
                    "end": end,
                }
            )

        return result
    except:
        return None


def transcribe(url: str) -> list[dict]:
    if not url:
        logger.error("Parâmetro invalido")
        return None

    video_id = url.split("?v=")[-1]
    logger.info("Iniciando transcrição via Youtube API")
    return _transcribe_youtube_api(video_id)

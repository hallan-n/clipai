from faster_whisper import WhisperModel
from youtube import download_audio_chunks
from logger import logger
from youtube_transcript_api import YouTubeTranscriptApi

model = WhisperModel("tiny", device="cpu", compute_type="int8", cpu_threads=1)


def _identify_format(path: str) -> bool:
    AUDIO = {"aac", "flac", "m4a", "mp3", "ogg", "opus", "wav", "wma"}
    return path.split(".")[-1].lower() in AUDIO


def _transcribe_chunks(chunks: list[str]) -> list[dict]:
    results: list[dict] = []
    offset = 0.0

    total = len(chunks)

    for idx, chunk_path in enumerate(chunks, 1):
        if not _identify_format(chunk_path):
            logger.warning(f"Formato ignorado: {chunk_path}")
            continue

        logger.info(f"Transcrevendo chunk {idx}/{total}")

        segments, _ = model.transcribe(
            chunk_path,
            language="pt",
            beam_size=1,
            temperature=0.0,
            vad_filter=False,
            condition_on_previous_text=False,
            chunk_length=15,
            no_speech_threshold=0.8,
            log_prob_threshold=-2.0,
        )

        last_end = 0.0

        for seg in segments:
            text = seg.text.strip()
            if not text:
                continue

            start = seg.start + offset
            end = seg.end + offset

            results.append(
                {
                    "text": text,
                    "start": round(start, 2),
                    "end": round(end, 2),
                }
            )

            last_end = seg.end

        offset += last_end

    return results


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

    video_id = url.split('?v=')[-1]
    logger.info('Iniciando transcrição via Youtube API')
    transc = _transcribe_youtube_api(video_id)

    if not transc:
        logger.warning('Erro ao baixar transcrição via Youtube API')
        logger.info('Iniciando transcrição via Whisper')
        chunks = download_audio_chunks(url)
        transc = _transcribe_chunks(chunks)

    return transc


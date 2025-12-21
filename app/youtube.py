import os
import tempfile
from yt_dlp import YoutubeDL
from logger import logger

def download_audio_chunks(
    video_url: str,
    chunk_seconds: int = 300,
    audio_format: str = "wav"
) -> list[str]:

    temp_dir = tempfile.mkdtemp(prefix="audio_chunks_")

    output_template = os.path.join(
        temp_dir,
        "chunk_%03d." + audio_format
    )

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "outtmpl": os.path.join(temp_dir, "full.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
                "preferredquality": "192",
            }
        ],
        
        "postprocessor_args": [
            "-f", "segment",
            "-segment_time", str(chunk_seconds),
            "-reset_timestamps", "1",
            output_template,
        ],
        "prefer_ffmpeg": True,
    }

    try:
        logger.info(f"Baixando áudio em chunks de {chunk_seconds}s")
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        chunks = sorted(
            os.path.join(temp_dir, f)
            for f in os.listdir(temp_dir)
            if f.startswith("chunk_")
        )

        logger.info(f"Chunks gerados: {len(chunks)}")
        return chunks

    except Exception as e:
        logger.error(f"Erro ao baixar áudio segmentado: {e}")
        return []


def download_audio_temp(video_url: str, format: str = "mp3") -> str | None:
    suffix = f".{format.lower()}"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp_path = tmp.name

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": tmp_path.replace(suffix, ".%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": format.lower(),
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }

    try:
        logger.info(f"Iniciando download {format} do video {video_url}")
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        final_path = tmp_path.replace(suffix, f".{format.lower()}")
        logger.info(f"Download concluído: {final_path}")
        return final_path
    except Exception as e:
        logger.error("Erro ao baixar áudio:", str(e))
        return None

def fetch_video_info(video_url: str) -> dict:
    ydl_opts = {
        "skip_download": True,
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
    return {
        "video_id": info.get("id"),
        "title": info.get("title"),
        "description": info.get("description"),
        "published_at": info.get("upload_date"),
        "duration": info.get("duration"),
        "views": info.get("view_count"),
        "likes": info.get("like_count"),
        "comments": info.get("comment_count"),
        "channel_id": info.get("channel_id"),
        "channel_title": info.get("uploader"),
        "thumbnail": info.get('thumbnail')
    }


def download_video_temp(
    video_url: str,
    video_format: str = "mp4",
    resolution: str = "best"
) -> str | None:
    suffix = f".{video_format.lower()}"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp_path = tmp.name

    ydl_opts = {
        "format": resolution,
        "outtmpl": tmp_path.replace(suffix, ".%(ext)s"),
        "merge_output_format": video_format.lower(),
        "quiet": True,
        "prefer_ffmpeg": True,
    }

    try:
        logger.info(f"Iniciando download do vídeo {video_url}")
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        final_path = tmp_path.replace(suffix, f".{video_format.lower()}")
        logger.info(f"Download concluído: {final_path}")
        return final_path

    except Exception as e:
        logger.error(f"Erro ao baixar vídeo: {e}")
        return None

import tempfile
from yt_dlp import YoutubeDL
from logger import logger

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
        return final_path
    except Exception as e:
        logger.error("Erro ao baixar áudio:", str(e))
        return None


def fetch_video_ytdlp(video_url: str) -> dict:
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
        "source": "ytdlp",
    }

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
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": format.lower(),
            "preferredquality": "192",
        }],
        "quiet": True,
    }

    try:
        logger.info(f'Iniciando download {format} do video {video_url}')
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        final_path = tmp_path.replace(suffix, f".{format.lower()}")
        return final_path
    except Exception as e:
        logger.error("Erro ao baixar áudio:", str(e))
        return None

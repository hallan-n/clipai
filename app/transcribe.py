from faster_whisper import WhisperModel
import subprocess
import io
import soundfile as sf

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

def _identify_format(file: str) -> str | None:
    AUDIO_FORMATS = [
        "aac", "ac3", "eac3", "alac", "amr", "ape", "au",
        "caf", "dts", "flac", "m4a", "mka", "mp2", "mp3",
        "ogg", "opus", "pcm", "ra", "tta", "voc",
        "wav", "wma"
    ]

    VIDEO_FORMATS = [
        "3gp", "avi", "asf", "flv", "mkv", "mov",
        "mp4", "mpeg", "mpg", "m2ts", "mts", "ts",
        "webm", "wmv", "vob", "rm", "rmvb",
        "hls", "m3u8", "dash", "mpd"
    ]
    
    if file.split('.')[-1] in AUDIO_FORMATS:
        return 'audio'
    elif file.split('.')[-1] in VIDEO_FORMATS:
        return 'video'
    else:
        return None


def _get_transcribe_from_bytes(audio_bytes: bytes) -> list[dict]:
    audio, sr = sf.read(io.BytesIO(audio_bytes), dtype="float32")

    segments, _ = model.transcribe(
        audio,
        language="pt"
    )

    return [
        {
            "text": seg.text.strip(),
            "start": seg.start,
            "end": seg.end
        }
        for seg in segments
    ]

def _get_transcribre_from_path(file_path: str):
    segments, _ = model.transcribe(file_path, language="pt")
    return [
        {
            "text": seg.text.strip(),
            "start": seg.start,
            "end": seg.end
        }
        for seg in segments
    ]

def _extract_audio_pipe(video_path: str) -> bytes:
    cmd = [
        "ffmpeg",
        "-y",
        "-loglevel", "error",
        "-i", video_path,
        "-map", "a:0", 
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-c:a", "pcm_s16le",
        "-f", "wav",
        "pipe:1", 
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )

    audio_bytes = proc.stdout.read()
    proc.wait()
    return audio_bytes


def trancribe(path: str):
    file_type = _identify_format(path)
    if file_type == "video":
        audio_bytes = _extract_audio_pipe(path)
        return _get_transcribe_from_bytes(audio_bytes)

    elif file_type == "audio":
        return _get_transcribre_from_path(path)

    else:
        raise ValueError("Formato não suportado")
import json
print(json.dumps(trancribe('/home/neves/Documentos/clipai/video.mp4'), indent=4))
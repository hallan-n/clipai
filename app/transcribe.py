import os
import glob
import subprocess
from faster_whisper import WhisperModel


CHUNK_SECONDS = 180 
SAMPLE_RATE = 16000
CHANNELS = 1
AUDIO_CODEC = "pcm_s16le"
CHUNK_DIR = "audio_chunks"


model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8",
    cpu_threads=2           # NÃO use todos os cores
)

def identify_format(path: str) -> str | None:
    AUDIO = {
        "aac","flac","m4a","mp3","ogg","opus","wav","wma"
    }
    VIDEO = {
        "mp4","mkv","mov","avi","webm","ts","mpeg","mpg"
    }

    ext = path.split(".")[-1].lower()
    if ext in AUDIO:
        return "audio"
    if ext in VIDEO:
        return "video"
    return None


def run_ffmpeg(cmd: list[str]):
    subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

def extract_audio_chunks(
    video_path: str,
    chunk_seconds: int = CHUNK_SECONDS,
    out_dir: str = CHUNK_DIR
):
    os.makedirs(out_dir, exist_ok=True)

    # limpa chunks antigos
    for f in glob.glob(f"{out_dir}/*.wav"):
        os.remove(f)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-map", "a:0",
        "-vn",
        "-ac", str(CHANNELS),
        "-ar", str(SAMPLE_RATE),
        "-c:a", AUDIO_CODEC,
        "-f", "segment",
        "-segment_time", str(chunk_seconds),
        os.path.join(out_dir, "chunk_%03d.wav"),
    ]

    run_ffmpeg(cmd)


def transcribe_chunks(
    chunk_dir: str = CHUNK_DIR,
    chunk_seconds: int = CHUNK_SECONDS
) -> list[dict]:

    results: list[dict] = []
    offset = 0.0

    chunks = sorted(glob.glob(f"{chunk_dir}/*.wav"))

    for idx, chunk_path in enumerate(chunks, 1):
        print(f"🧠 Transcrevendo chunk {idx}/{len(chunks)}")

        segments, _ = model.transcribe(
            chunk_path,
            language="pt",
            vad_filter=True,
            beam_size=1,
            temperature=0.0,
            condition_on_previous_text=False
        )
        
        for seg in segments:
            results.append({
                "text": seg.text.strip(),
                "start": round(seg.start + offset, 2),
                "end": round(seg.end + offset, 2),
            })

        offset += chunk_seconds

    return results


def transcribe(path: str) -> list[dict]:
    file_type = identify_format(path)

    if not file_type:
        raise ValueError("Formato não suportado")

    if file_type == "video":
        print("🎬 Extraindo áudio em blocos...")
        extract_audio_chunks(path)
        return transcribe_chunks()

    if file_type == "audio":
        print("🎧 Transcrevendo áudio diretamente...")
        segments, _ = model.transcribe(
            path,
            language="pt",
            vad_filter=True
        )
        return [
            {
                "text": seg.text.strip(),
                "start": round(seg.start, 2),
                "end": round(seg.end, 2),
            }
            for seg in segments
        ]


print(transcribe('/home/neves/Documentos/clipai/downloads/WmnZB256B3w.mp4'))
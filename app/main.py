from faster_whisper import WhisperModel
import subprocess

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

def get_transcribe(path: str) -> list[dict]:
    segments, _ = model.transcribe(path, language="pt")

    return [
        {
            "text": seg.text.strip(),
            "start": seg.start,
            "end": seg.end
        }
        for seg in segments
    ]



def extract_audio(video_path: str, audio_path: str):
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vn",
            "-ac", "1",
            "-ar", "16000",
            audio_path
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )


if __name__ == "__main__":
    from datetime import datetime, timedelta

    start = datetime.now()
    extract_audio("./video.mp4", "./audio.wav")
    get_transcribe("./audio.wav")

    end = datetime.now()

    print((end - start).total_seconds())

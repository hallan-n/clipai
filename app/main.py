from youtube import download_video_temp, fetch_transcribe
from edit_video import cut_video
from ask_llm import ask_gpt
import json


def run_pipeline(video_url: str):
    transcribe = fetch_transcribe(video_url)
    video_path = download_video_temp(video_url)
    prompt = "Indentifique os principais cortes nesses segimentos: {}"

    response = ask_gpt(prompt, [transcribe])
    segments = json.loads(response)

    for segment in segments:
        cut_video(video_path, segment['start'], segment['end'], 'saida.mp4')
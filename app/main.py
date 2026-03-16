from youtube import download_video_temp, fetch_transcribe
from edit_video import cut_video, concat_videos
from ask_llm import ask_gpt
import json
from prompt import prompt
from logger import logger

def run_pipeline(video_url: str):
    # transcribe = fetch_transcribe(video_url)
    transcribe = open("segments.json", "r").read()

    # if not transcribe:
    #     logger.error(f"Transcrição não disponível para o vídeo: {video_url}")
    #     raise ValueError(f"Transcrição não disponível para o vídeo: {video_url}")
    
    # video_path = download_video_temp(video_url)
    video_path = "/tmp/video_cz2dfzz1/video.mp4"

    # response = ask_gpt(prompt, ["Política", str(transcribe)])
    
    response = open("saida.json", "r").read()
    
    segments = json.loads(response)
    for segment in segments:
        cut_video(video_path, segment['start'], segment['end'], f'{segment['title']}.mp4')


run_pipeline("https://www.youtube.com/watch?v=DqtwWGL1WHQ")
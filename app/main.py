from youtube import download_video_temp, fetch_transcribe
from edit_video import cut_video, concat_videos
from ask_llm import ask_gpt
import json


def run_pipeline(video_url: str):
    transcribe = fetch_transcribe(video_url)
    video_path = download_video_temp(video_url)
    prompt = "Indentifique os principais cortes nesses segimentos: {}"

    response = ask_gpt(prompt, [transcribe])
    # segments = json.loads(response)

    segments = [
        {'start': 1, 'end': 2},
        {'start': 3, 'end': 4},
        {'start': 5, 'end': 6}
    ]

    for index, segment in enumerate(segments):
        cut_video(video_path, segment['start'], segment['end'], f'{index}.mp4')
        concat_videos(['intro.mp4', 'cut.mp4', 'ending.mp4'], f'{index}.mp4')


segments = [
    {'start': 1, 'end': 2},
    {'start': 3, 'end': 4},
    {'start': 5, 'end': 6}
]

for index, segment in enumerate(segments):
    cut_video('video.mp4', segment['start'], segment['end'], f'{index}.mp4')
    concat_videos(['intro.mp4', f'{index}.mp4', 'ending.mp4'], f'final_{index}.mp4')
import subprocess

def cut_video(video_path: str, start: float, end: float, output_path: str):
    duration = end - start

    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        str(start),
        "-i",
        video_path,
        "-t",
        str(duration),
        "-c",
        "copy",
        output_path,
    ]

    subprocess.run(cmd, check=True)


def concat_videos(video_paths: list[str], output_path: str) -> str:
    inputs = []
    filter_parts = []

    for i, path in enumerate(video_paths):
        inputs += ["-i", path]
        filter_parts.append(f"[{i}:v:0][{i}:a:0]")

    filter_complex = (
        "".join(filter_parts) + f"concat=n={len(video_paths)}:v=1:a=1[v][a]"
    )

    cmd = [
        "ffmpeg",
        "-y",
        *inputs,
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-map",
        "[a]",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-c:a",
        "aac",
        output_path,
    ]

    subprocess.run(cmd, check=True)
    return output_path

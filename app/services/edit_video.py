import subprocess

from services.logger import logger


def cut_video(
    input_video: str, start_seconds: float, end_seconds: float, output_video: str
):
    logger.info("Iniciado corte do video")
    duration = end_seconds - start_seconds

    command = [
        "ffmpeg",
        "-y",
        "-ss",
        str(start_seconds),
        "-i",
        input_video,
        "-t",
        str(duration),
        "-c",
        "copy",
        output_video,
    ]

    subprocess.run(command, check=True)
    logger.info("Finalizado corte do video")

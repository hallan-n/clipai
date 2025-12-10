import subprocess
import os
import shutil
from logger import logger

def extract_audio(in_video_path: str) -> bool:
    """
    Extrai o áudio de um vídeo usando FFmpeg em container Docker.
    Retorna True se deu certo, False caso tenha falhado.
    """
    try:
        data_dir = os.path.abspath("./data")
        os.makedirs(data_dir, exist_ok=True)
        
        shutil.copy(in_video_path, data_dir)

        video_container_path = "/data/videoplayback.mp4"
        audio_container_path = "/data/audio.wav"

        logger.info(f'Iniciado extração de áudio para {audio_container_path}')
        subprocess.run([
            "docker", "compose", "exec", "ffmpeg",
            "ffmpeg",
            "-loglevel", "quiet",
            "-y",
            "-i", video_container_path,
            "-ac", "1",
            "-ar", "16000",
            audio_container_path
        ], check=True)
        logger.info('Sucesso na extração do Áudio')
        return True

    except Exception as e:
        logger.info(f"Erro ao extrair áudio: {e}")
        return False


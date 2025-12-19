import requests
from logger import logger

def ask_ollama(prompt: str, params: list) -> bool:
    logger.info('Executando prompt junto ao Ollama AI.')
    prompt = prompt.format(*params)
    
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature":  0,
                "num_predict": 200
            }
        }
    )
    
    if r.status_code != 200:
        logger.error(f'Erro ao comunicar com Ollama AI: {r.json()["response"]}')
        raise ValueError(f'Erro ao comunicar com Ollama AI: {r.json()["response"]}')
    
    logger.info('Processamento finalizado.')
    return r.json()["response"]
    
from fastapi.responses import FileResponse
from ask_llm import ask_gpt
from youtube import fetch_video_info
from transcribe import transcribe
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json


app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/video')
async def get_video_info(url: str):
    if not url.startswith('https://www.youtube.com/watch?v'):
        raise HTTPException(400, 'URL inválida')
    
    try:        
        return fetch_video_info(url)
    except Exception as e:
        raise HTTPException(400, f'Erro ao pegar informações do vídeo: {e}')


@app.get('/video/transcribe')
async def get_video_transcribe(url: str):
    if not url.startswith('https://www.youtube.com/watch?v'):
        raise HTTPException(400, 'URL inválida')
    
    try:
        return transcribe(url)
    except Exception as e:
        raise HTTPException(400, f'Erro ao transcrever vídeo: {e}')


@app.get('/video/cuts')
async def get_video_cuts(url: str):
    if not url.startswith('https://www.youtube.com/watch?v'):
        raise HTTPException(400, 'URL inválida')
    

    prompt = """
Você é um analista político, especialista em analisar longas lives e identificar as pautas e temas MAIS IMPORTANTES e/ou POLEMICOS tratados.

Tarefa:
Identificar cortes temáticos em uma transcrição política longa, com intuito de capturar o TEMA MAIS FORTE e/ou MAIS POLÊMICO.

Regras:
- Um corte começa quando uma nova pauta política substantiva e dominante fica claramente definida.
- Um corte termina imediatamente antes do início da próxima pauta política substantiva.
- NÃO crie cortes para vinhetas, aberturas ou cumprimentos.
- Consiga pelo menos 2 cortes, que respeitem o tempo de 10 a 45 minutos, onde o tema seja o MAIS FORTE e/ou MAIS POLÊMICO

Indicadores de mudança de tema:
- Mudança clara da pauta política central.
- Mudança do fato, caso, investigação ou evento político analisado.
- Mudança do objeto principal de crítica ou análise.

Regras do campo topic:
- O campo "topic" DEVE ser um resumo detalhado e informativo da pauta política do corte.
- Tamanho máximo: 400 caracteres.
- Descreva o assunto principal, as pessoas envolvidas e o ponto central da análise.
- Escreva em português do Brasil.
- Linguagem clara, explicativa e neutra.
- Sem clickbait, sem caixa alta, sem metacomentários.

Saída:
Retorne APENAS um array JSON minificado.
Cada item deve seguir exatamente esta estrutura: {{"start":number,"end":number,"topic":string}}

Regras para start/end:
"start" deve ser exatamente o valor inicial do primeiro segmento incluído no corte.
"end" deve ser exatamente o valor final do último segmento incluído no corte.

NÃO estime, arredonde ou invente tempos.
Sem explicações.
Sem markdown.
Sem texto extra.

ENTRADA:
{0}
"""
    try:
        transc = transcribe(url)
        response = ask_gpt(prompt,  [json.dumps(transc, separators=(',', ':'))])
        return json.loads(response)
    except Exception as e:
        raise HTTPException(400, f'Erro ao transcrever vídeo: {e}')

@app.get('/video_full')
def main(url: str):
    if not url.startswith('https://www.youtube.com/watch?v'):
        raise HTTPException(400, 'URL inválida')
    
    return FileResponse(
        path='/home/neves/Documentos/clipai/cut.mp4',
        media_type="video/mp4",
        filename='TESTANDOOO'
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)
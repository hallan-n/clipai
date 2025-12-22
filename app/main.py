from fastapi.responses import FileResponse
from ask_llm import ask_gpt
from youtube import download_video_temp, fetch_video_info
from transcribe import transcribe
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from edit_video import cut_video
import json
import os

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

prompt_titles = """
Você é um especialista em copywriting político para YouTube, focado no estilo das lives do MBL (Renan Santos, Arthur do Val, Kim Kataguiri).

A entrada será um JSON onde cada chave representa um trecho resumido (cerca de 400 linhas) de um vídeo retirado de uma live, correspondente a um recorte entre 10 e 45 minutos.

Exemplo de entrada:
{{"1": "resumo do trecho", "2": "resumo do trecho"}}

Tarefa:
Para cada item do JSON:
- Leia todo o resumo
- Identifique o tema, embate ou fato político DOMINANTE desse trecho
- Gere APENAS 1 título polêmico, direto e altamente clicável, fiel exclusivamente ao conteúdo do resumo

Regras:
- Não use contexto fora do resumo
- Um único tema dominante por título
- Ignore digressões e comentários secundários
- Não invente fatos ou falas
- Não use perguntas
- Não use emojis (exceto 🚨 se houver urgência real)

Estilo do título:
- Entre 6 e 14 palavras
- Nomes próprios em CAIXA ALTA
- Verbos fortes como: REAGE, DETONA, RESPONDE, EXPÕE, ANALISA, IMPLODE, MANDA A REAL
- Pode usar termos como: ESCÂNDALO, TRETA, EXPOSED, FRACASSO, PRISÃO, GUERRA

Saída:
Retorne APENAS um JSON, mantendo as mesmas chaves da entrada, no formato:

{{"1": "titulo gerado", "2": "titulo gerado"}}

INPUT:
{0}

"""

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
    video_id = url.split('?v=')[-1]
    transc = transcribe(url)
    response = ask_gpt(prompt,  [json.dumps(transc, separators=(',', ':'))])
    cuts = json.loads(response)
    response = ask_gpt(prompt_titles,  [json.dumps(cuts, separators=(',', ':'))])
    titles = json.loads(response)

    video_path = download_video_temp(url)

    videos = []
    
    os.makedirs("cuts", exist_ok=True)

    for index, cut in enumerate(cuts, start=1):
        output_path = f"cuts/{video_id}_{index}.mp4"

        cut_video(
            input_video=video_path,
            start_seconds=cut['start'],
            end_seconds=cut['end'],
            output_video=output_path
        )

        videos.append(
            FileResponse(
                path=output_path,
                media_type="video/mp4",
                filename=titles[str(index)] + ".mp4"
            )
        )

    return videos

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)

from services.ask_llm import ask_gpt
from services.youtube import download_video_temp, get_channel_id, get_last_video_id
from services.transcribe import transcribe
from services.edit_video import cut_video
import json
import os
from services.logger import logger
from services.mongo import find_last

prompt_cuts = """
Você é um analista político, especialista em analisar longas lives e identificar as pautas e temas MAIS IMPORTANTES e/ou POLEMICOS tratados.

Tarefa:
Identificar cortes temáticos em uma transcrição política longa, com intuito de capturar o TEMA MAIS FORTE e/ou MAIS POLÊMICO.

Regras gerais:
- Um corte começa quando uma nova pauta política substantiva e dominante fica claramente definida.
- Um corte termina imediatamente antes do início da próxima pauta política substantiva.
- NÃO crie cortes para vinhetas, aberturas ou cumprimentos.
- Gere pelo menos 2 cortes.
- Cada corte deve ter duração entre 10 e 45 minutos.
- Priorize pautas politicamente relevantes, controversas ou com alto potencial de repercussão.

Indicadores de mudança de tema:
- Mudança clara da pauta política central.
- Mudança do fato, caso, investigação ou evento político analisado.
- Mudança do objeto principal de crítica, comentário ou análise.

Regras do campo "topic":
- O campo "topic" DEVE ser um resumo detalhado, informativo e NEUTRO da pauta política do corte.
- O resumo DEVE obrigatoriamente explicitar:
  • quem está falando ou comentando na live (ator principal do trecho)
  • o assunto político central
  • as pessoas, grupos ou instituições citadas
  • o ponto central da análise ou comentário
- NÃO inicie o resumo com expressões impessoais como:
  "Análise de", "Discussão sobre", "Detalhamento de", "Comentário sobre".
- Linguagem clara, explicativa e neutra.
- Sem caixa alta.
- Sem clickbait.
- Sem metacomentários.
- Tamanho máximo: 400 caracteres.
- Escreva em português do Brasil.

Saída:
Retorne APENAS um array JSON minificado.
Cada item deve seguir exatamente esta estrutura:
{{"start":number,"end":number,"topic":string}}

Regras para start/end:
- "start" deve ser exatamente o valor inicial do primeiro segmento incluído no corte.
- "end" deve ser exatamente o valor final do último segmento incluído no corte.
- NÃO estime, arredonde ou invente tempos.

Sem explicações.
Sem markdown.
Sem texto extra.

ENTRADA:
{0}

"""

prompt_titles = """
Você é um copywriter político agressivo para YouTube, especializado no estilo dos cortes das lives do MBL
(Renan Santos, Arthur do Val, Kim Kataguiri).

A entrada será um JSON onde cada chave representa um trecho resumido de um vídeo retirado de uma live,
correspondente a um recorte entre 10 e 45 minutos.

Exemplo de entrada:
{{"1": "resumo do trecho", "2": "resumo do trecho"}}

Tarefa:
Para cada item do JSON:
- Leia TODO o resumo
- Identifique o GANCHO POLÍTICO mais polêmico e explorável do trecho
- Identifique claramente:
  • quem faz a crítica, análise ou exposição (PROTAGONISTA)
  • quem é o alvo da crítica ou denúncia (ALVO)
- Gere APENAS 1 título altamente clicável no estilo MBL

Regras obrigatórias:
- O título DEVE começar com o PROTAGONISTA (pessoa ou grupo que critica ou expõe)
- NUNCA use como sujeito do título pessoas, partidos ou empresas que sejam ALVO de denúncia,
  suspeita ou irregularidade
- Se houver dúvida sobre o protagonista, utilize quem está comentando na live
- Um único conflito ou tese central por título
- Ignore digressões e detalhes técnicos
- NÃO use contexto fora do resumo
- NÃO invente fatos ou falas
- NÃO use perguntas
- NÃO use emojis (exceto 🚨 se houver urgência real)

Enquadramento:
- É permitido enquadramento agressivo e retórico
  (ESCÂNDALO, TRETA, EXPOSED, FRACASSO, GUERRA),
  desde que coerente com o conteúdo do resumo
- O título pode ser mais forte que o tom do resumo, sem criar fatos novos

Estilo do título:
- NÃO há limite rígido de palavras
- Linguagem direta, emocional e polarizadora
- Nomes próprios sempre em CAIXA ALTA
- Use verbos fortes como:
  REAGE, DETONA, RESPONDE, EXPÕE, IMPLODE, MANDA A REAL, ANALISA

Saída:
Retorne APENAS um JSON, mantendo exatamente as mesmas chaves da entrada, no formato:

{{"1": "titulo gerado", "2": "titulo gerado"}}

INPUT:
{0}

"""


def main(channel_url: str):
    if not channel_url.startswith('https://www.youtube.com/'):
        raise ValueError(f'URL inválida: {channel_url}')
    
    channel_id = get_channel_id(channel_url)

    last_video_id = get_last_video_id(channel_id)

    last_video_mongo = find_last('youtube', channel_id)

    if last_video_id == last_video_mongo:
        logger.info("Nenhum vídeo novo encontrado.")
        return
    

    url = f'https://www.youtube.com/watch?v={last_video_id}'
    transc = transcribe(url)

    response_cuts = ask_gpt(prompt_cuts, [json.dumps(transc, separators=(',', ':'))])

    cuts = json.loads(response_cuts)

    topics = {str(i): item['topic'] for i, item in enumerate(cuts, start=1)}
    
    response_titles = ask_gpt(prompt_titles, [json.dumps(topics, separators=(',', ':'))])

    titles = json.loads(response_titles)

    video_path = download_video_temp(url)

    cuts_dir = "cuts"
    os.makedirs(cuts_dir, exist_ok=True)

    cut_paths = []

    for index, cut in enumerate(cuts, start=1):
        output_path = f"{cuts_dir}/{last_video_id}_{index}.mp4"

        cut_video(
            input_video=video_path,
            start_seconds=cut["start"],
            end_seconds=cut["end"],
            output_video=output_path
        )

        cut_paths.append((output_path, titles[str(index)] + ".mp4"))


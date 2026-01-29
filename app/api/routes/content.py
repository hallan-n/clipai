from datetime import datetime
import re

from services.ask_llm import ask_gpt
import json
from api.schemas.content import ContentResponse, GetContentsResponse
from api.schemas.source import SourceResponse
from api.security import decode_token
from api.utils import get_current_user
from db.models import Content, Cut
from crud.crud_cut import CutRepository
from crud.crud_content import ContentRepository
from crud.crud_source import SourceRepository
from fastapi import APIRouter, Depends, HTTPException
from services.youtube import fetch_transcribe, fetch_video_info, fetch_video_infos

route = APIRouter(prefix="/content", tags=["Conteúdos"])
content_repo = ContentRepository()
source_repo = SourceRepository()
cut_repo = CutRepository()

@route.get(
    "",
    summary="Listar os conteúdos dos canais do YouTube",
    description="Lista todos os conteúdos dos canais do YouTube adicionados como fontes para o usuário autenticado.",
    response_model=GetContentsResponse | list[GetContentsResponse],
)
def get_contents(
    source_id: int = None, content_limit: int = 5, token: dict = Depends(decode_token)
):
    current_user = get_current_user(token)
    if source_id:
        source = source_repo.select_by_id(source_id)
        if not source or source.login_id != current_user.id:
            raise HTTPException(404, "Canal não encontrado.")

        video_infos = fetch_video_infos(source.url.split("/")[-1], content_limit)
        return GetContentsResponse(
            source=SourceResponse(**source.model_dump()),
            contents=[ContentResponse(**video_info) for video_info in video_infos],
        )

    sources = source_repo.select_all_by_login_id(current_user.id)

    if not sources:
        raise HTTPException(404, "Nenhum canal encontrado.")
    videos = []
    for source in sources:
        video_infos = fetch_video_infos(source.url.split("/")[-1], content_limit)
        videos.append(
            GetContentsResponse(
                source=SourceResponse(**source.model_dump()),
                contents=[ContentResponse(**video_info) for video_info in video_infos],
            )
        )

    return videos













prompt = """
Você é um analista de transcrição de videos, lives e podcasts.

Tarefa:
Identificar cortes temáticos com intuito de capturar o TEMA MAIS FORTE e/ou MAIS POLÊMICO.

Descrição do canal onde você analisará o conteúdo:
{1} é um canal que produz vídeos sobre {2},
com foco em {3},
apresentando {4},
e público-alvo {5}.
Lança conteúdos {6}, buscando {7}.

Regras:
- Um corte começa quando uma novo assunto se inicia.
- Um corte termina imediatamente antes do início do próximo assunto.
- NÃO crie cortes para vinhetas, aberturas ou cumprimentos.
- Consiga 2 cortes ou mais corte que respeitem o tempo de 10 a 45 minutos, onde o tema seja o MAIS FORTE e/ou MAIS POLÊMICO

Indicadores de mudança de tema:
- Mudança clara da pauta.
- Mudança do fato, caso, investigação ou evento analisado.
- Mudança do objeto principal.

Saída:
Retorne APENAS um array JSON minificado.
Cada item deve seguir exatamente esta estrutura: {{"start":number,"end":number,"topic":string}}

Regras do campo topic:
- O campo "topic" DEVE ser um resumo detalhado e informativo do corte com no máximo 400 caracteres.
- Descreva o assunto principal, as pessoas envolvidas e o ponto central da análise.
- Escreva em português do Brasil com linguagem clara, explicativa e neutra.
- Sem clickbait, sem caixa alta, sem metacomentários.


Regras para start e end:
"start" deve ser exatamente o valor inicial do primeiro segmento incluído no corte.
"end" deve ser exatamente o valor final do último segmento incluído no corte.

NÃO estime, arredonde ou invente tempos.
Sem explicações.
Sem markdown.
Sem texto extra.

ENTRADA:
{0}
"""
@route.get(
    "/process",
    summary="Processa um vídeo do YouTube",
    description="Processa um vídeo do YouTube e retorna as informações do conteúdo.",
)
def process_content(video_url: str, token: dict = Depends(decode_token)):
    if not video_url.startswith("https://www.youtube.com"):
        raise HTTPException(400, "URL inválida.")

    if not "watch?v" in video_url:
        raise HTTPException(400, "URL inválida.")

    if not re.match(r"^https:\/\/www\.youtube\.com\/watch\?v=.*$", video_url):
        raise HTTPException(400, "URL inválida.")

    current_user = get_current_user(token)
    video_info = fetch_video_info(video_url)

    current_source = source_repo.select_by_url_and_login_id(video_info['channel_url'], current_user.id)
    if not current_source:
        raise HTTPException(404, "O conteúdo é de uma fonte não registrada.")
    
    current_content = content_repo.select_by_url_and_login_id(video_info["url"], current_user.id)
    if current_content:
        return cut_repo.select_all_by_content_id(current_content.id)

    current_content = content_repo.insert(
        Content(
            url=video_info["url"],
            title=video_info["title"],
            description=video_info["description"],
            published_at=datetime.strptime(video_info["published_at"], "%Y%m%d"),
            thumbnail=video_info["thumbnail"],
            duration=video_info["duration"],
            source_id=current_source.id
        )
    )

    name = current_source.name
    main_topics = current_source.main_topics
    content_focus = current_source.content_focus
    content_format = current_source.content_format
    target_audience = current_source.target_audience
    upload_frequency = current_source.upload_frequency
    viewer_benefit = current_source.viewer_benefit
    
    transc = fetch_transcribe(video_info["video_id"])
    
    
    
    raw_cuts = json.loads(ask_gpt(prompt, [transc,name,main_topics,content_focus,content_format,target_audience,upload_frequency,viewer_benefit]))
    processed_cuts = []
    for raw_cut in raw_cuts:
        cut = cut_repo.insert(Cut(
            title="",
            start=raw_cut["start"],
            end=raw_cut["end"],
            total_duration=raw_cut["end"] - raw_cut["start"],
            describe=raw_cut['topic'],
            content_id=current_content.id
        ))
        processed_cuts.append(cut)

    return processed_cuts

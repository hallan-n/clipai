from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class SourceRequest(BaseModel):
    url: str | None = Field(
        default=None,
        description="URL do canal do YouTube (ex: https://www.youtube.com/@canal)",
        example="https://www.youtube.com/@canal",
    )

    main_topics: str | None = Field(
        default=None,
        description="Principais temas abordados pelo canal",
        example="política, economia, análise de eventos",
    )

    content_focus: str | None = Field(
        default=None,
        description="Foco central do conteúdo produzido",
        example="análise política e debates",
    )

    content_format: str | None = Field(
        default=None,
        description="Formato predominante dos vídeos",
        example="transmissões ao vivo, entrevistas, vlogs",
    )

    target_audience: str | None = Field(
        default=None,
        description="Público-alvo do canal",
        example="pessoas interessadas em política e atualidades",
    )

    upload_frequency: str | None = Field(
        default=None,
        description="Frequência média de publicação de vídeos",
        example="diariamente",
    )

    viewer_benefit: str | None = Field(
        default=None,
        description="Principal benefício para quem assiste o canal",
        example="informação atualizada e análise crítica dos fatos",
    )


class SourceResponse(BaseModel):
    id: int | None
    custom_id: str | None
    name: str | None
    subscribe: str | None
    thumbnail: str | None
    avatar: str | None
    url: str | None
    custom_url: str | None
    last_video: str | None
    main_topics: str | None
    content_focus: str | None
    content_format: str | None
    target_audience: str | None
    upload_frequency: str | None
    viewer_benefit: str | None

    created_at: datetime | None
    updated_at: datetime | None


class RemoveSourceResponse(BaseModel):
    success: bool | None
    detail: str | None

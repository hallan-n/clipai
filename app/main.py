import uvicorn
from api.routes.content import route as content
from api.routes.login import route as login
from api.routes.source import route as source
from fastapi import FastAPI

app = FastAPI()


app.include_router(login)
app.include_router(source)
app.include_router(content)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# channel_name = "MBLiveTV"
# main_topics = "política, análise de eventos e debates"
# content_focus = "análise política e debates"
# content_format = "transmissões ao vivo, entrevistas, vlogs"
# target_audience = "público interessado em política e análise política"
# upload_frequency = "diariamente"
# viewer_benefit = "informação atualizada sobre eventos políticos e debates"


# print(
# f"""{channel_name} é um canal que produz vídeos sobre {main_topics},
# com foco em {content_focus},
# apresentando {content_format},
# e público-alvo {target_audience}.
# Lança conteúdos {upload_frequency}, buscando {viewer_benefit}.""")

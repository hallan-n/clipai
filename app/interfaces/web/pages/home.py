from nicegui import ui
from services.youtube_dl import fetch_video_ytdlp

@ui.page("/")
async def index():

    def fetch_video(url: str):
        response = fetch_video_ytdlp(url)
        pub_at = response['published_at']
        video_id.content = f'**VIDEO ID:** {response['video_id']}'
        title.content = f'**TÍTULO:** {response['title'][:30]}'
        published_at.content = f'**PUBLICADO EM:** {pub_at[6:8]}/{pub_at[4:6]}/{pub_at[:4]}'
        channel_title.content = f'**CANAL:** {response['channel_title']}'
        thumbnail.source = response['thumbnail']


    with ui.element("div").classes('w-full'):
        with ui.element('div').classes(
            'rounded-lg border-zinc-300 border-2 p-4 flex gap-8 items-center'
        ):

            with ui.element("div").classes('flex gap-2 max-h-12'):
                url_input = ui.input(label='URL do vídeo')
                ui.button(
                    'Carregar',
                    icon='upload',
                    on_click=lambda: fetch_video(url_input.value)
                )
            
            with ui.element("div").classes('flex gap-3 justify-between items-center'):
                with ui.element("div").classes('flex flex-col m-0'):
                    video_id = ui.markdown().classes('m-0 p-0')
                    title = ui.markdown().classes('m-0 p-0')
                    published_at = ui.markdown().classes('m-0 p-0')
                    channel_title = ui.markdown().classes('m-0 p-0')
                thumbnail = ui.image('').classes('rounded-lg overflow-hidden border-zinc-400 h-full w-96')

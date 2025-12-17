from nicegui import ui
from datetime import datetime

# =============================
# MOCK CUTS ONLY
# =============================
MOCK_CUTS = [
    {
        'start': 0,
        'end': 42,
        'text': 'In this introduction, we discuss the rapid evolution of artificial intelligence and why it matters.'
    },
    {
        'start': 42,
        'end': 95,
        'text': 'Here we move into practical examples of how AI tools are already impacting daily development workflows.'
    },
    {
        'start': 95,
        'end': 150,
        'text': 'This segment focuses on the risks, limitations, and common misconceptions surrounding AI adoption.'
    },
]


from services.youtube_dl import fetch_video_ytdlp

@ui.page('/')
def index():
    ui.dark_mode().enable()


    with ui.column().classes('w-full max-w-6xl mx-auto gap-6 p-6'):
        ui.label('YouTube Smart Cutter (Dark Mode)').classes('text-3xl font-bold')
        ui.label('Send a YouTube link and let the AI split it into meaningful segments').classes('text-gray-500')

        # =============================
        # INPUT CARD
        # =============================
        with ui.card().classes('w-full p-4'):
            with ui.row().classes('w-full items-end gap-4'):
                url_input = ui.input(
                    label='YouTube Video URL',
                    placeholder='https://www.youtube.com/watch?v=...'
                ).classes('flex-1')

                def load_video():
                    response = fetch_video_ytdlp(url_input.value)

                    pub_at = response['published_at']
                    video_id.content = f"**ID:** {response['video_id']}"
                    title.content = f"**Title:** {response['title']}"
                    published_at.content = f"**Published:** {pub_at[6:8]}/{pub_at[4:6]}/{pub_at[:4]}"
                    channel_title.content = f"**Channel:** {response['channel_title']}"
                    thumbnail.source = response['thumbnail']

                    cuts_container.clear()
                    render_cuts()

                ui.button('Analyze Video', icon='smart_toy', on_click=load_video)

        # =============================
        # VIDEO INFO
        # =============================
        with ui.card().classes('w-full p-4'):
            with ui.row().classes('w-full gap-6'):
                with ui.column().classes('flex-1 gap-1'):
                    video_id = ui.markdown()
                    title = ui.markdown()
                    published_at = ui.markdown()
                    channel_title = ui.markdown()
                thumbnail = ui.image('').classes('rounded-lg w-96')

        # =============================
        # CUTS
        # =============================
        ui.label('Detected Cuts').classes('text-xl font-semibold mt-4')

        cuts_container = ui.column().classes('w-full gap-4')

        def render_cuts():
            for idx, cut in enumerate(MOCK_CUTS, start=1):
                with cuts_container:
                    with ui.card().classes('w-full p-4 hover:shadow-lg transition'):
                        with ui.row().classes('justify-between items-center'):
                            ui.label(f'Cut #{idx}').classes('font-semibold')
                            ui.badge(f"{cut['start']}s → {cut['end']}s", color='blue')
                        ui.separator()
                        ui.label(cut['text']).classes('text-gray-700 leading-relaxed')


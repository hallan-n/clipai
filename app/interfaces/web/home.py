from nicegui import ui

@ui.page("/")
async def index():

    with ui.element("div"):
        with ui.element("div").classes(
            "relative w-screen h-screen "
            "bg-[url('https://raw.githubusercontent.com/hallan-n/cdn-free/main/prewedding/29.jpg')] "
            "bg-cover bg-no-repeat "
            "bg-[length:160%] bg-[position:20%_40%] "
            "lg:bg-[url('assets/mask2.png')] "
            "lg:bg-contain lg:bg-left lg:bg-[length:auto] lg:bg-[position:left_center]"
        ):
            ui.button('clikca ai')
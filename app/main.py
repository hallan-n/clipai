# from services.youtube_dl import fetch_video_ytdlp, download_audio_temp
# from transcribe import trancribe
# from segmentation import segmentation
# import os
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['http://localhost', 'http://127.0.0.1:5500'],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/video")
# async def get_video_info(url: str):
#     return fetch_video_ytdlp(url)


# @app.get("/video")
# async def generate_cuts(url: str):
#     tmp_path = download_audio_temp(url)

#     try:
#         transc = trancribe(tmp_path)
#     except Exception as e:
#         raise HTTPException(400, str(e))

#     finally:
#         os.remove(tmp_path)
#     return segmentation(transc)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)



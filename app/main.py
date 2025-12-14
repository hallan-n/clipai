from fastapi import FastAPI, UploadFile, File, HTTPException
import tempfile
import os
from transcribe import identify_format, extract_audio_pipe, get_transcribe_from_bytes, get_transcribre_from_path


app = FastAPI()

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    file_type = identify_format(tmp_path)
    try:
        if file_type == "video":
            audio_bytes = extract_audio_pipe(tmp_path)
            result = get_transcribe_from_bytes(audio_bytes)

        elif file_type == "audio":
            return get_transcribre_from_path(tmp_path)

        else:
            raise HTTPException(400, "Formato não suportado")

        return {"segments": result}

    finally:
        os.remove(tmp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)
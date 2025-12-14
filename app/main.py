from fastapi import FastAPI, UploadFile, File, HTTPException
import tempfile
import os
from transcribe import trancribe


app = FastAPI()

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
        
    try:
        import json
        transc = trancribe(tmp_path)
        with open("./saida.json", 'w', encoding='utf-8') as doc:
            doc.write(json.dumps(transc, indent=4))
        return {"segments": transc}
    except Exception as e:
        raise HTTPException(400, str(e))

    finally:
        os.remove(tmp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)